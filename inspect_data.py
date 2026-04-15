#!/usr/bin/env python3
"""Inspect local COMP90024 NDJSON samples with the shared core logic."""

from __future__ import annotations

import argparse
from pathlib import Path

from comp90024_a1.analysis import default_paths, inspect_file
from comp90024_a1.reporting import file_summary_to_dict, print_file_summary

print_summary = print_file_summary
summary_to_dict = file_summary_to_dict


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
    parser.add_argument(
        "--output-json",
        help="Optional path for saving the inspected summaries as JSON.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()

    paths = [Path(path) for path in args.paths] if args.paths else default_paths()
    if not paths:
        raise SystemExit("No NDJSON files found. Run this from the assignment folder or pass paths.")

    all_summaries = []
    for path in paths:
        if not path.exists():
            print(f"Skipping missing file: {path}")
            continue
        summary = inspect_file(path, limit=args.limit)
        print_file_summary(summary, top_n=args.top)
        all_summaries.append(file_summary_to_dict(summary, top_n=args.top))

    if args.output_json:
        import json

        output_path = Path(args.output_json)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            json.dumps({"files": all_summaries}, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        print(f"Saved JSON summary to: {output_path}")


if __name__ == "__main__":
    main()
