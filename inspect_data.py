#!/usr/bin/env python3
"""Run a local serial baseline over COMP90024 NDJSON samples."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run a local serial language-count baseline over NDJSON files."
    )
    parser.add_argument(
        "paths",
        nargs="*",
        help=(
            "Files to inspect. If omitted, the script inspects all local small "
            "and medium samples in the current directory."
        ),
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Only inspect the first N lines of each file.",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=None,
        help="Show only the top N language codes per file. Default: show all.",
    )
    return parser


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


def sorted_counts(counter: Counter[str], top_n: int | None = None) -> list[tuple[str, int]]:
    ordered = counter.most_common()
    if top_n is None:
        return ordered
    return ordered[:top_n]


def print_counter_table(
    title: str, counts: Counter[str], top_n: int | None = None, empty_label: str = "None"
) -> None:
    ordered = sorted_counts(counts, top_n=top_n)
    print(title)
    if not ordered:
        print(f"  {empty_label}")
        return

    print("  Rank  Code/Reason        Count")
    for index, (key, value) in enumerate(ordered, start=1):
        print(f"  {index:>4}  {key:<15}  {value:>5}")


def print_summary(summary: FileSummary, top_n: int | None = None) -> None:
    print("=" * 72)
    print(f"File: {summary.path}")
    print(f"Dataset type: {summary.dataset_type}")
    print(f"Total lines: {summary.total_lines}")
    print(f"Successfully parsed JSON: {summary.parsed_json_lines}")
    print(f"Skipped records: {summary.skipped_records}")
    print(f"Counted records: {summary.counted_records}")
    print(f"Counted language assignments: {summary.counted_language_assignments}")
    print(f"Invalid JSON lines: {summary.invalid_json}")
    print(
        "Detected language paths:",
        dict(summary.language_path_hits) or "No matching language path detected",
    )
    print("Language value types:", dict(summary.language_value_types))
    print_counter_table("Skip reasons:", summary.skip_reasons)
    print_counter_table("Language frequency table:", summary.language_counts, top_n=top_n)
    print_counter_table(
        "Suspicious non-standard codes:",
        summary.suspicious_codes,
        empty_label="None detected",
    )
    print()


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    paths = [Path(path) for path in args.paths] if args.paths else default_paths()
    if not paths:
        parser.error("No NDJSON files found. Run this from the assignment folder or pass paths.")

    for path in paths:
        if not path.exists():
            print(f"Skipping missing file: {path}")
            continue
        summary = inspect_file(path, limit=args.limit)
        print_summary(summary, top_n=args.top)


if __name__ == "__main__":
    main()
