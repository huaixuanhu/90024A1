"""CLI entry point for the MPI version of COMP90024 Assignment 1."""

from __future__ import annotations

import argparse
import os
import re
import socket
import sys
import time
from pathlib import Path
from shlex import join as shlex_join

from comp90024_a1.analysis import (
    build_run_summary,
    compute_byte_range,
    inspect_file_range,
    merge_file_summaries,
    timestamp_to_datetime,
)
from comp90024_a1.reporting import (
    append_jsonl,
    format_run_summary,
    print_run_summary,
    run_summary_to_dict,
    write_json,
)


LABEL_PATTERN = re.compile(r"[A-Za-z0-9_.-]+$")


def build_mpi_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Process one Mastodon NDJSON file and one BlueSky NDJSON file in a single "
            "MPI program run."
        )
    )
    parser.add_argument("--mastodon", required=True, help="Path to the Mastodon NDJSON file.")
    parser.add_argument("--bluesky", required=True, help="Path to the BlueSky NDJSON file.")
    parser.add_argument(
        "--label",
        required=True,
        help="Run label used in saved filenames, for example large_mpi_1node8cores_v1.",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=None,
        help="Only print the top N language codes. Default: print all.",
    )
    parser.add_argument(
        "--output-dir",
        default="results",
        help="Directory where the text output, summary JSON, and run log are saved.",
    )
    return parser


def main() -> None:
    try:
        from mpi4py import MPI
    except ImportError as exc:  # pragma: no cover - depends on runtime environment
        raise SystemExit(
            "mpi4py is required for mpi_main.py. On Spartan load the MPI modules first, "
            "for example: module load GCC/13.3.0 OpenMPI/5.0.3 mpi4py/4.0.1"
        ) from exc

    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    args = build_mpi_parser().parse_args()
    if not LABEL_PATTERN.fullmatch(args.label):
        raise SystemExit(
            "Invalid label. Use only letters, numbers, dot, underscore, or hyphen."
        )

    mastodon_path = Path(args.mastodon)
    bluesky_path = Path(args.bluesky)
    output_dir = Path(args.output_dir)
    text_output_path = output_dir / f"{args.label}_output.txt"
    summary_output_path = output_dir / f"{args.label}_summary.json"
    run_log_path = output_dir / "run_log.jsonl"

    comm.Barrier()
    local_started_ts = time.time()

    mastodon_start, mastodon_end = compute_byte_range(
        mastodon_path.stat().st_size, rank, size
    )
    bluesky_start, bluesky_end = compute_byte_range(
        bluesky_path.stat().st_size, rank, size
    )

    mastodon_partial = inspect_file_range(mastodon_path, mastodon_start, mastodon_end)
    bluesky_partial = inspect_file_range(bluesky_path, bluesky_start, bluesky_end)

    local_finished_ts = time.time()
    hostnames = comm.gather(socket.gethostname(), root=0)
    started_timestamps = comm.gather(local_started_ts, root=0)
    finished_timestamps = comm.gather(local_finished_ts, root=0)
    mastodon_partials = comm.gather(mastodon_partial, root=0)
    bluesky_partials = comm.gather(bluesky_partial, root=0)

    if rank != 0:
        return

    mastodon_summary = merge_file_summaries(mastodon_partials)
    bluesky_summary = merge_file_summaries(bluesky_partials)
    started_at = timestamp_to_datetime(min(started_timestamps))
    finished_at = timestamp_to_datetime(max(finished_timestamps))

    run_summary = build_run_summary(
        label=args.label,
        mastodon_path=mastodon_path,
        bluesky_path=bluesky_path,
        entry_script=Path(sys.argv[0]).name,
        command=f"{sys.executable} {shlex_join(sys.argv)}",
        cwd=str(Path.cwd()),
        mode="mpi",
        nodes=int(os.environ.get("SLURM_JOB_NUM_NODES", str(len(set(hostnames))))),
        processes=size,
        cpus_per_process=int(os.environ.get("SLURM_CPUS_PER_TASK", "1")),
        started_at=started_at,
        finished_at=finished_at,
        mastodon_summary=mastodon_summary,
        bluesky_summary=bluesky_summary,
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
    summary_record["runtime_distribution"] = {
        "hostnames": sorted(set(hostnames)),
        "ranks": size,
    }

    write_json(summary_output_path, summary_record)
    append_jsonl(run_log_path, summary_record)

    print_run_summary(run_summary, top_n=args.top)
    print(f"Saved text output to: {text_output_path}")
    print(f"Saved JSON summary to: {summary_output_path}")
    print(f"Appended run log entry to: {run_log_path}")
