"""Formatting and serialization helpers for COMP90024 Assignment 1."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

from comp90024_a1.analysis import FileSummary, RunSummary


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


def print_file_summary(summary: FileSummary, top_n: int | None = None) -> None:
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


def print_run_summary(summary: RunSummary, top_n: int | None = None) -> None:
    print("#" * 72)
    print(f"Run label: {summary.label}")
    print(f"Mastodon input: {summary.mastodon_path}")
    print(f"BlueSky input: {summary.bluesky_path}")
    print(f"Elapsed seconds: {summary.elapsed_seconds:.6f}")
    print(f"Language table mode: {'top ' + str(top_n) if top_n is not None else 'full'}")
    print("#" * 72)
    print()
    print_file_summary(summary.mastodon, top_n=top_n)
    print_file_summary(summary.bluesky, top_n=top_n)


def file_summary_to_dict(summary: FileSummary, top_n: int | None = None) -> dict[str, Any]:
    return {
        "path": str(summary.path),
        "dataset_type": summary.dataset_type,
        "total_lines": summary.total_lines,
        "parsed_json_lines": summary.parsed_json_lines,
        "skipped_records": summary.skipped_records,
        "counted_records": summary.counted_records,
        "counted_language_assignments": summary.counted_language_assignments,
        "invalid_json": summary.invalid_json,
        "language_path_hits": dict(summary.language_path_hits),
        "language_value_types": dict(summary.language_value_types),
        "skip_reasons": dict(summary.skip_reasons),
        "language_counts": dict(sorted_counts(summary.language_counts, top_n=top_n)),
        "suspicious_codes": dict(summary.suspicious_codes),
    }


def run_summary_to_dict(summary: RunSummary, top_n: int | None = None) -> dict[str, Any]:
    return {
        "label": summary.label,
        "elapsed_seconds": round(summary.elapsed_seconds, 6),
        "inputs": {
            "mastodon": str(summary.mastodon_path),
            "bluesky": str(summary.bluesky_path),
        },
        "results": {
            "mastodon": file_summary_to_dict(summary.mastodon, top_n=top_n),
            "bluesky": file_summary_to_dict(summary.bluesky, top_n=top_n),
        },
    }


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

