# Reasoning Trace

This file keeps a short human-agent decision log for the COMP90024 assignment work in this folder.

## Entry 001

- Date: 2026-04-15
- Decision: Start with local exploration on the `small` and `medium` datasets before using SPARTAN.
- Reason: The SPARTAN account is still pending, and the assignment instructions explicitly allow local development on `small` and `medium` while reserving `large` for final analysis and benchmarking.
- Evidence: The assignment brief allows local development on smaller files, and the four local `.ndjson` files are already present in this folder.
- Next Step: Confirm the language counting rules and build a reliable local serial baseline.

## Entry 002

- Date: 2026-04-15
- Decision: Use a project-local `.venv` together with `JupyterLab` for exploration, while keeping reusable logic in Python scripts.
- Reason: The notebook is convenient for inspecting NDJSON structure and recording observations, but the final assignment still needs a runnable single program that can later move to SPARTAN, MPI, and SLURM.
- Evidence: The local environment is set up, `explore_data.ipynb` can be opened in JupyterLab, and `inspect_data.py` already runs on the local sample files.
- Next Step: Turn the agreed rules into a clearer local serial analyzer for the `small` and `medium` datasets.

## Entry 003

- Date: 2026-04-15
- Decision: Use `Mastodon -> doc.language` and `BlueSky -> record.langs` as the current local extraction paths.
- Reason: These are the fields that consistently contain the language values in the local `small` and `medium` datasets.
- Evidence: The current notebook and command-line inspection both report `doc.language` for Mastodon and `record.langs` for BlueSky.
- Next Step: Implement counting rules for `str`, `list`, and missing values using these paths.

## Entry 004

- Date: 2026-04-15
- Decision: Adopt the local serial counting rules before building the larger assignment baseline.
- Reason: We need a stable and explainable rule set before moving on to MPI and SPARTAN execution.
- Evidence: The agreed rules are: `str` counts as one language, `list` counts each language item, `None/null/empty list/empty string` are skipped and recorded as missing, and all codes are normalized to lowercase.
- Next Step: Keep suspicious non-standard codes such as `zh-cn` or `en-us` unchanged for now and report them separately.

## Entry 005

- Date: 2026-04-15
- Decision: Keep the current local baseline conservative and preserve suspicious codes in the raw counts.
- Reason: The local runs already show codes like `zh-cn`, `zh-tw`, and `en-us`, so forcing an early mapping would hide original data values before we decide how to treat them in the final assignment output.
- Evidence: The full local runs on `small` and `medium` completed without invalid JSON, while still surfacing a small set of suspicious non-standard codes.
- Next Step: Use these baseline results as the reference point for the next serial assignment program.

## Entry 006

- Date: 2026-04-15
- Decision: Add `serial_language_counter.py` as the local assignment-style single-program entry point.
- Reason: The assignment requires one program to process both Mastodon and BlueSky, so the local workflow now needs a paired-input serial script instead of only per-file inspection utilities.
- Evidence: The script now runs one Mastodon file and one BlueSky file together, measures elapsed time, prints both result tables, and saves JSON summaries for `small` and `medium`.
- Next Step: Reuse this serial structure when moving toward the final assignment program and later MPI adaptation.

## Entry 007

- Date: 2026-04-15
- Decision: Refactor the serial baseline into a clearer final-style structure with `main.py` plus a shared `comp90024_a1` package.
- Reason: The final submission will be easier to explain, maintain, and later extend to MPI if the counting logic, reporting logic, and CLI entry are already separated.
- Evidence: The project now has `main.py` as the formal serial entry, `comp90024_a1/analysis.py` for counting, and `comp90024_a1/reporting.py` for output and JSON serialization.
- Next Step: Keep using `main.py` as the reference serial program before adding parallel execution.

## Entry 008

- Date: 2026-04-16
- Decision: Make run metadata and usage rules explicit through automatic JSONL logging and a dedicated `RUN_RECORD_RULES.md` file.
- Reason: One teammate will later write the report, and both humans and agents need a stable way to recover timing results, run configurations, and authoritative output files.
- Evidence: `main.py` now records timing, command, working directory, Python version, local serial resource settings, input file sizes, and artifact paths, and appends each formal run to `results/run_log.jsonl`.
- Next Step: Use labeled formal runs such as `small_serial_v1` and `medium_serial_v1` as the current report-ready local baseline.

## Entry 009

- Date: 2026-04-16
- Decision: Synchronize the successful Spartan serial baseline results back into the local repository and maintain a fuller benchmark summary file.
- Reason: The report will need the exact Spartan timings, configuration details, and artifact paths later, so the local repository should keep a clean copy of the current authoritative serial baseline.
- Evidence: The local `results/` folder now includes `spartan_small_serial_v3`, `spartan_medium_serial_v3`, and `spartan_large_serial_v2`, and `BENCHMARK_SUMMARY.md` consolidates their run labels, timings, configurations, and result highlights.
- Next Step: Use the synchronized Spartan serial baseline as the reference point for MPI benchmarking.

## Entry 010

- Date: 2026-04-16
- Decision: Implement the first MPI version by reusing the shared counting logic and splitting each NDJSON file by byte range across MPI ranks.
- Reason: This keeps one program handling both Mastodon and BlueSky while avoiding a second, unrelated parsing code path, and it gives a practical first benchmarkable MPI design for Spartan.
- Evidence: The new `mpi_main.py` and `comp90024_a1/mpi_cli.py` use the shared analysis layer, load-balanced byte ranges, and root-rank aggregation to produce the same style of saved outputs as the serial program.
- Next Step: Validate the MPI version on Spartan with `small` or `medium`, then run the required `1 node 8 cores` and `2 nodes 8 cores` large-file benchmarks.

## Entry 011

- Date: 2026-04-16
- Decision: Validate the MPI implementation on Spartan with `small` and `medium` before launching the large MPI benchmarks.
- Reason: The assignment expects large-file benchmarking on shared HPC resources, so it is safer to confirm correctness and multi-node execution on cheaper test runs first.
- Evidence: `spartan_small_mpi_1node8cores_v1`, `spartan_small_mpi_2nodes8cores_v1`, and `spartan_medium_mpi_1node8cores_v1` all completed successfully on Spartan, and their counted records and language tables match the serial baseline.
- Next Step: Use the validated MPI path to launch the final large-file MPI benchmarks for `1 node 8 cores` and `2 nodes 8 cores`.

## Template

- Date:
- Decision:
- Reason:
- Evidence:
- Next Step:
