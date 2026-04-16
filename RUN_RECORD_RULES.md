# Run Record Rules

This file defines the authoritative run-record rules for the local COMP90024 Assignment 1 workflow.

## 1. Purpose

These rules exist so that:

- one teammate can run the program and another teammate can write the report later
- humans and agents can both find the correct timing and configuration records
- local and Spartan benchmark runs stay traceable as the project moves toward MPI

## 2. Authoritative Files

For any formal run, treat the following files as authoritative:

- `results/<label>_output.txt`
- `results/<label>_summary.json`
- `results/run_log.jsonl`

Do not treat notebook output or terminal scrollback as the final record.

## 3. Formal Run Rules

1. Use `main.py` for formal serial runs and `mpi_main.py` for formal MPI runs.
2. Always provide an explicit `--label`.
3. Use labels that are stable and descriptive, for example:
   - `small_serial_v1`
   - `medium_serial_v1`
   - `spartan_large_serial_v2`
   - `large_mpi_1node8cores_v1`
4. Do not manually edit old JSON summaries or old `run_log.jsonl` entries.
5. Every formal run must produce:
   - one text output file
   - one single-run JSON summary
   - one appended JSONL run-log entry
6. If a run should not be cited later, use `inspect_data.py` instead of `main.py`.

## 4. Naming Rules

Labels must use only:

- letters
- numbers
- dot `.`
- underscore `_`
- hyphen `-`

Recommended pattern:

- `<dataset_scope>_<mode>_v<version>`

Examples:

- `small_serial_v1`
- `medium_serial_v1`

## 5. Standard Usage

Activate the virtual environment first for local runs:

```bash
source .venv/bin/activate
```

Run the `small` pair:

```bash
python main.py \
  --label small_serial_v1 \
  --mastodon mastodon-small.ndjson \
  --bluesky bluesky-small.ndjson \
  --output-dir results
```

Run the `medium` pair:

```bash
python main.py \
  --label medium_serial_v1 \
  --mastodon mastodon-medium.ndjson \
  --bluesky bluesky-medium.ndjson \
  --output-dir results
```

On Spartan, serial and MPI runs should still save into the same `results/` directory, but MPI runs must first load the MPI modules:

```bash
module load GCC/13.3.0 OpenMPI/5.0.3 mpi4py/4.0.1
```

## 6. What Gets Recorded

Each formal run records:

- `label`
- `run_started_at`
- `run_finished_at`
- `elapsed_seconds`
- `entry_script`
- `command`
- `cwd`
- `mode`
- `nodes`
- `processes`
- `cpus_per_process`
- `python_version`
- `python_executable`
- `hostname`
- `platform`
- input file paths
- input file sizes
- per-dataset counts and skip reasons
- per-dataset language frequency tables
- suspicious non-standard language codes
- artifact paths for the saved text output, summary JSON, and run log

## 7. Which File To Use

Use these sources in this order:

1. For a full single run: `results/<label>_summary.json`
2. For comparing many runs quickly: `results/run_log.jsonl`
3. For human-readable output tables: `results/<label>_output.txt`

## 8. Guidance For Report Writing

When writing the report:

- use `elapsed_seconds` from the JSON summary or JSONL log
- use `mode`, `nodes`, `processes`, and `cpus_per_process` as the run configuration
- use the per-dataset `language_counts` tables for result tables
- use `suspicious_codes` if you need to discuss non-standard codes

## 9. Guidance For Human-Agent Collaboration

When continuing work with an agent:

1. read `RUN_RECORD_RULES.md` first
2. read `results/run_log.jsonl` to find the run of interest
3. open the referenced `results/<label>_summary.json`
4. only then use the text output file if a human-readable table is needed

## 10. Current Scope

These rules currently cover:

- local serial runs
- Spartan serial runs
- Spartan MPI validation and benchmark runs

When adding more formal MPI benchmark runs, extend the recorded fields instead of replacing them. Add fields such as:

- `job_id`
- `tasks`
- `cpus_per_task`
- `nodes`
- `launcher_command`
- `slurm_script`
