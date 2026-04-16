"""CLI entry points for the COMP90024 Assignment 1 local serial program."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from shlex import join as shlex_join

from comp90024_a1.analysis import run_serial_pair
from comp90024_a1.reporting import (
    append_jsonl,
    format_run_summary,
    print_run_summary,
    run_summary_to_dict,
    write_json,
)


LABEL_PATTERN = re.compile(r"[A-Za-z0-9_.-]+$")

# The CLI is designed to be user-friendly and robust, with clear argument parsing, validation, and structured output management. It ensures that all outputs are saved in a consistent manner, and that the run summary is both human-readable and machine-readable for further analysis or reporting.
def build_main_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Process one Mastodon NDJSON file and one BlueSky NDJSON file in a single "
            "serial program run."
        )
    )
    parser.add_argument(
        "--mastodon",
        required=True,
        help="Path to the Mastodon NDJSON file.",
    )
    parser.add_argument(
        "--bluesky",
        required=True,
        help="Path to the BlueSky NDJSON file.",
    )
    parser.add_argument(
        "--label",
        required=True,
        help="Run label used in saved filenames, for example small_serial_v1.",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=None,
        help="Only print the top N language codes. Default: print all.",
    )
    parser.add_argument(
        "--output-json",
        help="Legacy option. Prefer --output-dir and let the program manage filenames.",
    )
    parser.add_argument(
        "--output-dir",
        default="results",
        help="Directory where the text output, summary JSON, and run log are saved.",
    )
    return parser

#main function
def main() -> None:
    args = build_main_parser().parse_args()
    if not LABEL_PATTERN.fullmatch(args.label):
        raise SystemExit(
            "Invalid label. Use only letters, numbers, dot, underscore, or hyphen."
        )

    output_dir = Path(args.output_dir)
    text_output_path = output_dir / f"{args.label}_output.txt"
    summary_output_path = (
        Path(args.output_json)
        if args.output_json
        else output_dir / f"{args.label}_summary.json"
    )
    run_log_path = output_dir / "run_log.jsonl"

    run_summary = run_serial_pair(
        mastodon_path=Path(args.mastodon),
        bluesky_path=Path(args.bluesky),
        label=args.label,
        entry_script=Path(sys.argv[0]).name,
        command=f"{sys.executable} {shlex_join(sys.argv)}",
        cwd=str(Path.cwd()),
    )

    text_output = format_run_summary(run_summary, top_n=args.top)
    output_dir.mkdir(parents=True, exist_ok=True)
    text_output_path.write_text(text_output, encoding="utf-8")

    summary_record = run_summary_to_dict(run_summary, top_n=args.top)
    summary_record["artifacts"] = {
        "text_output_path": str(text_output_path),
        "summary_json_path": str(summary_output_path),
        "run_log_path": str(run_log_path),
    }

    write_json(summary_output_path, summary_record)
    append_jsonl(run_log_path, summary_record)

    print_run_summary(run_summary, top_n=args.top)
    print(f"Saved text output to: {text_output_path}")
    print(f"Saved JSON summary to: {summary_output_path}")
    print(f"Appended run log entry to: {run_log_path}")
