"""Core serial processing logic for COMP90024 Assignment 1."""

from __future__ import annotations

import json
import re
import socket
import sys
import time
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime
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


def inspect_file(path: Path, limit: int | None = None) -> FileSummary:
    summary = FileSummary(path=path, dataset_type=infer_dataset_type(path))

    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if limit is not None and line_number > limit:
                break

            summary.total_lines += 1

            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                summary.invalid_json += 1
                summary.skipped_records += 1
                summary.skip_reasons["invalid_json"] += 1
                continue

            summary.parsed_json_lines += 1

            if not isinstance(obj, dict):
                summary.skipped_records += 1
                summary.skip_reasons["top_level_non_object"] += 1
                continue

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
                continue

            summary.counted_records += 1

            for code in languages:
                summary.language_counts[code] += 1
                summary.counted_language_assignments += 1
                if not STANDARD_CODE_PATTERN.fullmatch(code):
                    summary.suspicious_codes[code] += 1

    return summary


def run_serial_pair(
    mastodon_path: Path,
    bluesky_path: Path,
    label: str,
    entry_script: str,
    command: str,
    cwd: str,
) -> RunSummary:
    started_at = datetime.now().astimezone()
    start = time.perf_counter()
    mastodon_summary = inspect_file(mastodon_path)
    bluesky_summary = inspect_file(bluesky_path)
    elapsed_seconds = time.perf_counter() - start
    finished_at = datetime.now().astimezone()

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
        mode="serial",
        nodes=1,
        processes=1,
        cpus_per_process=1,
        python_version=sys.version.split()[0],
        python_executable=sys.executable,
        hostname=socket.gethostname(),
        platform_name=platform(),
        mastodon=mastodon_summary,
        bluesky=bluesky_summary,
    )
