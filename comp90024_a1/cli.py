"""CLI entry points for the COMP90024 Assignment 1 local serial program."""

from __future__ import annotations

import argparse
from pathlib import Path

from comp90024_a1.analysis import run_serial_pair
from comp90024_a1.reporting import print_run_summary, run_summary_to_dict, write_json


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
        default="run",
        help="Short label for the run, for example small or medium.",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=None,
        help="Only print the top N language codes. Default: print all.",
    )
    parser.add_argument(
        "--output-json",
        help="Optional path for saving the run summary as JSON.",
    )
    return parser


def main() -> None:
    args = build_main_parser().parse_args()

    run_summary = run_serial_pair(
        mastodon_path=Path(args.mastodon),
        bluesky_path=Path(args.bluesky),
        label=args.label,
    )

    print_run_summary(run_summary, top_n=args.top)

    if args.output_json:
        output_path = Path(args.output_json)
        write_json(output_path, run_summary_to_dict(run_summary, top_n=args.top))
        print(f"Saved JSON summary to: {output_path}")

