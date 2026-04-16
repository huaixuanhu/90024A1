"""Core serial and MPI-ready processing logic for COMP90024 Assignment 1."""

from __future__ import annotations

import json
import math
import os
import re
import socket
import sys
import time
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from platform import platform
from typing import Any


LANGUAGE_PATHS: dict[str, list[tuple[str, ...]]] = {
    "mastodon": [
        ("doc", "language"),
        ("language",),
        ("doc", "langs"),
        ("langs",),
    ],
    "bluesky": [
        ("record", "langs"),
        ("langs",),
        ("record", "language"),
        ("language",),
    ],
}

STANDARD_CODE_PATTERN = re.compile(r"[a-z]{2,3}$")


@dataclass
class FileSummary:
    path: Path
    dataset_type: str
    total_lines: int = 0
    parsed_json_lines: int = 0
    skipped_records: int = 0
    counted_records: int = 0
    counted_language_assignments: int = 0
    invalid_json: int = 0
    skip_reasons: Counter[str] = field(default_factory=Counter)
    language_path_hits: Counter[str] = field(default_factory=Counter)
    language_value_types: Counter[str] = field(default_factory=Counter)
    language_counts: Counter[str] = field(default_factory=Counter)
    suspicious_codes: Counter[str] = field(default_factory=Counter)


@dataclass
class RunSummary:
    label: str
    mastodon_path: Path
    bluesky_path: Path
    mastodon_size_bytes: int
    bluesky_size_bytes: int
    run_started_at: str
    run_finished_at: str
    elapsed_seconds: float
    entry_script: str
    command: str
    cwd: str
    mode: str
    nodes: int
    processes: int
    cpus_per_process: int
    python_version: str
    python_executable: str
    hostname: str
    platform_name: str
    mastodon: FileSummary
    bluesky: FileSummary


def default_paths() -> list[Path]:
    names = [
        "mastodon-small.ndjson",
        "bluesky-small.ndjson",
        "mastodon-medium.ndjson",
        "bluesky-medium.ndjson",
    ]
    return [Path(name) for name in names if Path(name).exists()]


def infer_dataset_type(path: Path) -> str:
    lowered = path.name.lower()
    if "mastodon" in lowered:
        return "mastodon"
    if "bluesky" in lowered:
        return "bluesky"
    return "unknown"


def nested_lookup(obj: dict[str, Any], path: tuple[str, ...]) -> tuple[bool, Any]:
    current: Any = obj
    for key in path:
        if not isinstance(current, dict) or key not in current:
            return False, None
        current = current[key]
    return True, current


def detect_language_value(
    obj: dict[str, Any], dataset_type: str
) -> tuple[str | None, Any]:
    for path in LANGUAGE_PATHS.get(dataset_type, []):
        found, value = nested_lookup(obj, path)
        if found:
            return ".".join(path), value
    return None, None


def normalize_code(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    cleaned = value.strip().lower()
    return cleaned or None


def extract_languages(value: Any) -> tuple[list[str], str | None]:
    if value is None:
        return [], "missing_value"

    if isinstance(value, str):
        cleaned = normalize_code(value)
        if cleaned is None:
            return [], "empty_string"
        return [cleaned], None

    if isinstance(value, list):
        if not value:
            return [], "empty_list"

        cleaned_values = [normalize_code(item) for item in value]
        languages = [code for code in cleaned_values if code is not None]
        if languages:
            return languages, None
        return [], "empty_or_non_string_list"

    return [], f"unexpected_type:{type(value).__name__}"


def process_json_line(summary: FileSummary, line: str) -> None:
    summary.total_lines += 1

    try:
        obj = json.loads(line)
    except json.JSONDecodeError:
        summary.invalid_json += 1
        summary.skipped_records += 1
        summary.skip_reasons["invalid_json"] += 1
        return

    summary.parsed_json_lines += 1

    if not isinstance(obj, dict):
        summary.skipped_records += 1
        summary.skip_reasons["top_level_non_object"] += 1
        return

    language_path, language_value = detect_language_value(obj, summary.dataset_type)
    if language_path is not None:
        summary.language_path_hits[language_path] += 1

    value_type = type(language_value).__name__ if language_value is not None else "None"
    summary.language_value_types[value_type] += 1

    languages, skip_reason = extract_languages(language_value)
    if not languages:
        summary.skipped_records += 1
        if skip_reason is not None:
            summary.skip_reasons[skip_reason] += 1
        return

    summary.counted_records += 1

    for code in languages:
        summary.language_counts[code] += 1
        summary.counted_language_assignments += 1
        if not STANDARD_CODE_PATTERN.fullmatch(code):
            summary.suspicious_codes[code] += 1


def inspect_file(path: Path, limit: int | None = None) -> FileSummary:
    summary = FileSummary(path=path, dataset_type=infer_dataset_type(path))

    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if limit is not None and line_number > limit:
                break
            process_json_line(summary, line)

    return summary


def compute_byte_range(file_size: int, part_index: int, part_count: int) -> tuple[int, int]:
    if part_count <= 0:
        raise ValueError("part_count must be positive")
    if file_size <= 0:
        return 0, -1

    start = math.floor(file_size * part_index / part_count)
    end = math.floor(file_size * (part_index + 1) / part_count) - 1
    return start, end


def inspect_file_range(path: Path, start_byte: int, end_byte: int) -> FileSummary:
    summary = FileSummary(path=path, dataset_type=infer_dataset_type(path))
    if end_byte < start_byte:
        return summary

    with path.open("rb") as handle:
        handle.seek(start_byte)
        if start_byte > 0:
            handle.readline()

        while True:
            line_start = handle.tell()
            if line_start > end_byte:
                break

            raw_line = handle.readline()
            if not raw_line:
                break

            try:
                decoded_line = raw_line.decode("utf-8")
            except UnicodeDecodeError:
                summary.total_lines += 1
                summary.invalid_json += 1
                summary.skipped_records += 1
                summary.skip_reasons["invalid_utf8"] += 1
                continue

            process_json_line(summary, decoded_line)


    return summary


def merge_file_summaries(partials: list[FileSummary]) -> FileSummary:
    if not partials:
        raise ValueError("partials must not be empty")

    merged = FileSummary(
        path=partials[0].path,
        dataset_type=partials[0].dataset_type,
    )

    for partial in partials:
        merged.total_lines += partial.total_lines
        merged.parsed_json_lines += partial.parsed_json_lines
        merged.skipped_records += partial.skipped_records
        merged.counted_records += partial.counted_records
        merged.counted_language_assignments += partial.counted_language_assignments
        merged.invalid_json += partial.invalid_json
        merged.skip_reasons.update(partial.skip_reasons)
        merged.language_path_hits.update(partial.language_path_hits)
        merged.language_value_types.update(partial.language_value_types)
        merged.language_counts.update(partial.language_counts)
        merged.suspicious_codes.update(partial.suspicious_codes)

    return merged


def build_run_summary(
    *,
    label: str,
    mastodon_path: Path,
    bluesky_path: Path,
    entry_script: str,
    command: str,
    cwd: str,
    mode: str,
    nodes: int,
    processes: int,
    cpus_per_process: int,
    started_at: datetime,
    finished_at: datetime,
    mastodon_summary: FileSummary,
    bluesky_summary: FileSummary,
) -> RunSummary:
    elapsed_seconds = finished_at.timestamp() - started_at.timestamp()
    return RunSummary(
        label=label,
        mastodon_path=mastodon_path,
        bluesky_path=bluesky_path,
        mastodon_size_bytes=mastodon_path.stat().st_size,
        bluesky_size_bytes=bluesky_path.stat().st_size,
        run_started_at=started_at.isoformat(timespec="milliseconds"),
        run_finished_at=finished_at.isoformat(timespec="milliseconds"),
        elapsed_seconds=elapsed_seconds,
        entry_script=entry_script,
        command=command,
        cwd=cwd,
        mode=mode,
        nodes=nodes,
        processes=processes,
        cpus_per_process=cpus_per_process,
        python_version=sys.version.split()[0],
        python_executable=sys.executable,
        hostname=socket.gethostname(),
        platform_name=platform(),
        mastodon=mastodon_summary,
        bluesky=bluesky_summary,
    )


def timestamp_to_datetime(unix_timestamp: float) -> datetime:
    return datetime.fromtimestamp(unix_timestamp, tz=timezone.utc).astimezone()


def run_serial_pair(
    mastodon_path: Path,
    bluesky_path: Path,
    label: str,
    entry_script: str,
    command: str,
    cwd: str,
) -> RunSummary:
    started_at = datetime.now().astimezone()
    mastodon_summary = inspect_file(mastodon_path)
    bluesky_summary = inspect_file(bluesky_path)
    finished_at = datetime.now().astimezone()

    return build_run_summary(
        label=label,
        mastodon_path=mastodon_path,
        bluesky_path=bluesky_path,
        entry_script=entry_script,
        command=command,
        cwd=cwd,
        mode="serial",
        nodes=int(os.environ.get("SLURM_JOB_NUM_NODES", "1")),
        processes=1,
        cpus_per_process=int(os.environ.get("SLURM_CPUS_PER_TASK", "1")),
        started_at=started_at,
        finished_at=finished_at,
        mastodon_summary=mastodon_summary,
        bluesky_summary=bluesky_summary,
    )
