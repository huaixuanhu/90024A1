#!/usr/bin/env python3
"""Serial single-program baseline for COMP90024 local small/medium runs."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any

from inspect_data import inspect_file, print_summary, summary_to_dict


def build_parser() -> argparse.ArgumentParser:
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

def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    args = build_parser().parse_args()

    mastodon_path = Path(args.mastodon)
    bluesky_path = Path(args.bluesky)

    start = time.perf_counter()
    mastodon_summary = inspect_file(mastodon_path)
    bluesky_summary = inspect_file(bluesky_path)
    elapsed_seconds = time.perf_counter() - start

    run_summary = {
        "label": args.label,
        "elapsed_seconds": round(elapsed_seconds, 6),
        "inputs": {
            "mastodon": str(mastodon_path),
            "bluesky": str(bluesky_path),
        },
        "results": {
            "mastodon": summary_to_dict(mastodon_summary, top_n=args.top),
            "bluesky": summary_to_dict(bluesky_summary, top_n=args.top),
        },
    }

    print("#" * 72)
    print(f"Run label: {args.label}")
    print(f"Mastodon input: {mastodon_path}")
    print(f"BlueSky input: {bluesky_path}")
    print(f"Elapsed seconds: {elapsed_seconds:.6f}")
    print(f"Language table mode: {'top ' + str(args.top) if args.top is not None else 'full'}")
    print("#" * 72)
    print()
    print_summary(mastodon_summary, top_n=args.top)
    print_summary(bluesky_summary, top_n=args.top)

    if args.output_json:
        output_path = Path(args.output_json)
        write_json(output_path, run_summary)
        print(f"Saved JSON summary to: {output_path}")


if __name__ == "__main__":
    main()
