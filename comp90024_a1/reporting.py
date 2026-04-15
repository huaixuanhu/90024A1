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
    print(format_counter_table(title, counts, top_n=top_n, empty_label=empty_label), end="")


def print_file_summary(summary: FileSummary, top_n: int | None = None) -> None:
    print(format_file_summary(summary, top_n=top_n), end="")


def print_run_summary(summary: RunSummary, top_n: int | None = None) -> None:
    print(format_run_summary(summary, top_n=top_n), end="")


def format_counter_table(
    title: str, counts: Counter[str], top_n: int | None = None, empty_label: str = "None"
) -> str:
    ordered = sorted_counts(counts, top_n=top_n)
    lines = [f"{title}\n"]
    if not ordered:
        lines.append(f"  {empty_label}\n")
        return "".join(lines)

    lines.append("  Rank  Code/Reason        Count\n")
    for index, (key, value) in enumerate(ordered, start=1):
        lines.append(f"  {index:>4}  {key:<15}  {value:>5}\n")
    return "".join(lines)


def format_file_summary(summary: FileSummary, top_n: int | None = None) -> str:
    lines = [
        "=" * 72 + "\n",
        f"File: {summary.path}\n",
        f"Dataset type: {summary.dataset_type}\n",
        f"Total lines: {summary.total_lines}\n",
        f"Successfully parsed JSON: {summary.parsed_json_lines}\n",
        f"Skipped records: {summary.skipped_records}\n",
        f"Counted records: {summary.counted_records}\n",
        f"Counted language assignments: {summary.counted_language_assignments}\n",
        f"Invalid JSON lines: {summary.invalid_json}\n",
        "Detected language paths: "
        + str(dict(summary.language_path_hits) or "No matching language path detected")
        + "\n",
        f"Language value types: {dict(summary.language_value_types)}\n",
        format_counter_table("Skip reasons:", summary.skip_reasons),
        format_counter_table("Language frequency table:", summary.language_counts, top_n=top_n),
        format_counter_table(
            "Suspicious non-standard codes:",
            summary.suspicious_codes,
            empty_label="None detected",
        ),
        "\n",
    ]
    return "".join(lines)


def format_run_summary(summary: RunSummary, top_n: int | None = None) -> str:
    lines = [
        "#" * 72 + "\n",
        f"Run label: {summary.label}\n",
        f"Entry script: {summary.entry_script}\n",
        f"Command: {summary.command}\n",
        f"Working directory: {summary.cwd}\n",
        f"Run started at: {summary.run_started_at}\n",
        f"Run finished at: {summary.run_finished_at}\n",
        f"Elapsed seconds: {summary.elapsed_seconds:.6f}\n",
        f"Mode: {summary.mode}\n",
        f"Nodes: {summary.nodes}\n",
        f"Processes: {summary.processes}\n",
        f"CPUs per process: {summary.cpus_per_process}\n",
        f"Python version: {summary.python_version}\n",
        f"Python executable: {summary.python_executable}\n",
        f"Hostname: {summary.hostname}\n",
        f"Platform: {summary.platform_name}\n",
        f"Mastodon input: {summary.mastodon_path}\n",
        f"Mastodon size bytes: {summary.mastodon_size_bytes}\n",
        f"BlueSky input: {summary.bluesky_path}\n",
        f"BlueSky size bytes: {summary.bluesky_size_bytes}\n",
        f"Language table mode: {'top ' + str(top_n) if top_n is not None else 'full'}\n",
        "#" * 72 + "\n\n",
        format_file_summary(summary.mastodon, top_n=top_n),
        format_file_summary(summary.bluesky, top_n=top_n),
    ]
    return "".join(lines)


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
        "language_counts": dict(sorted_counts(summary.language_counts, top_n=None)),
        "suspicious_codes": dict(summary.suspicious_codes),
    }


def run_summary_to_dict(summary: RunSummary, top_n: int | None = None) -> dict[str, Any]:
    return {
        "label": summary.label,
        "run_metadata": {
            "entry_script": summary.entry_script,
            "command": summary.command,
            "cwd": summary.cwd,
            "run_started_at": summary.run_started_at,
            "run_finished_at": summary.run_finished_at,
            "elapsed_seconds": round(summary.elapsed_seconds, 6),
            "top_n_display": top_n,
            "mode": summary.mode,
            "nodes": summary.nodes,
            "processes": summary.processes,
            "cpus_per_process": summary.cpus_per_process,
            "python_version": summary.python_version,
            "python_executable": summary.python_executable,
            "hostname": summary.hostname,
            "platform": summary.platform_name,
        },
        "elapsed_seconds": round(summary.elapsed_seconds, 6),
        "inputs": {
            "mastodon": str(summary.mastodon_path),
            "bluesky": str(summary.bluesky_path),
            "mastodon_size_bytes": summary.mastodon_size_bytes,
            "bluesky_size_bytes": summary.bluesky_size_bytes,
        },
        "results": {
            "mastodon": file_summary_to_dict(summary.mastodon, top_n=top_n),
            "bluesky": file_summary_to_dict(summary.bluesky, top_n=top_n),
        },
    }


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def append_jsonl(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(data, ensure_ascii=False) + "\n")
