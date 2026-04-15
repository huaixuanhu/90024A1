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

## Template

- Date:
- Decision:
- Reason:
- Evidence:
- Next Step:
