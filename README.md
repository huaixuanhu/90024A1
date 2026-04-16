# COMP90024 Assignment 1 Local Setup

This folder is set up for local data exploration, the serial baseline, and the first MPI-ready version before moving the full benchmark workflow to SPARTAN.

## Project structure

- `main.py`: the current assignment-style serial single-program entry
- `mpi_main.py`: the MPI entry that still processes Mastodon and BlueSky in one program
- `comp90024_a1/analysis.py`: shared language extraction and counting logic
- `comp90024_a1/reporting.py`: terminal output and JSON summary helpers
- `inspect_data.py`: local inspection helper for exploratory work
- `serial_language_counter.py`: compatibility wrapper that calls `main.py`
- `RUN_RECORD_RULES.md`: authoritative rules for formal run recording and report use
- `BENCHMARK_SUMMARY.md`: fuller summary of the current local and Spartan serial benchmark records
- `spartan/`: prepared SLURM scripts for serial and MPI runs on Spartan
- `results/`: saved local outputs for the `small` and `medium` runs

## Run Records First

Before doing any formal run, read `RUN_RECORD_RULES.md`.

That file defines:

- which command counts as a formal run
- how labels should be named
- which files are authoritative for report writing
- how humans and agents should retrieve prior run records

## 1. Activate the virtual environment

```bash
source .venv/bin/activate
```

## 2. Start JupyterLab

```bash
jupyter lab
```

Open `explore_data.ipynb` in the browser. That notebook mirrors the command-line baseline output.

## 3. Run the command-line baseline

Run the full local serial baseline over all small and medium files:

```bash
python inspect_data.py
```

Show only the top 10 language codes per file:

```bash
python inspect_data.py --top 10
```

Inspect only the first 200 lines of the small files:

```bash
python inspect_data.py --limit 200 mastodon-small.ndjson bluesky-small.ndjson
```

## 4. Run the assignment-style serial single program

Run one Mastodon file and one BlueSky file in a single program invocation:

```bash
python main.py \
  --label small_serial_v1 \
  --mastodon mastodon-small.ndjson \
  --bluesky bluesky-small.ndjson \
  --output-dir results
```

Run the medium files:

```bash
python main.py \
  --label medium_serial_v1 \
  --mastodon mastodon-medium.ndjson \
  --bluesky bluesky-medium.ndjson \
  --output-dir results
```

For formal runs, `main.py` now saves all three artifacts automatically:

- `results/<label>_output.txt`
- `results/<label>_summary.json`
- `results/run_log.jsonl`

If you already used the old command, `serial_language_counter.py` still works as a wrapper, but `main.py` is the preferred formal entry.

Current authoritative local runs already saved these files:

- `results/small_serial_v1_output.txt`
- `results/small_serial_v1_summary.json`
- `results/medium_serial_v1_output.txt`
- `results/medium_serial_v1_summary.json`
- `results/run_log.jsonl`

## 5. Benchmark summary helper

Use `BENCHMARK_SUMMARY.md` as the first quick reference when you need:

- exact elapsed times
- formal run labels
- input sizes
- artifact paths
- top language counts and skip totals

The authoritative machine-readable records are still the JSON summary files in `results/` and the combined `results/run_log.jsonl`.

## 6. What the baseline reports

- Total lines
- Successfully parsed JSON records
- Skipped records and skip reasons
- Detected language field paths
- Language value types such as `str` or `list`
- Explicit run metadata and configuration
- Full language frequency table
- Suspicious non-standard codes kept in raw form

## 7. Current local observations

- `mastodon` currently stores the language value under `doc.language`
- `bluesky` currently stores language values under `record.langs`
- These observations are based on the local `small` and `medium` files in this folder

## Initial observations from local `small` and `medium` files

The local `small` and `medium` datasets were used only for early inspection and testing before moving to SPARTAN.

Current observations from local exploration:

- The two datasets do not store language information in the same place.
- In the local Mastodon files, the language field is currently observed at `doc.language`.
- In the local BlueSky files, the language field is currently observed at `record.langs`.
- Mastodon language values currently appear mainly as a single string value.
- BlueSky language values currently appear mainly as a list of language codes.
- Missing or empty language values can occur, so the parser should handle them safely.
- Initial inspection did not show obvious malformed JSON in the local sample files, but the final program should still be robust to invalid records.
- English (`en`) appears to be the dominant language in both local samples.
- Some language codes may include variants such as region-specific forms, so normalization rules may be needed later.

These are preliminary observations only and are based on the local `small` and `medium` files, not the final `large` files on SPARTAN.


## 8. MPI program

The project now includes an MPI entry for Spartan:

```bash
module load GCC/13.3.0 OpenMPI/5.0.3 mpi4py/4.0.1

srun python3 mpi_main.py \
  --mastodon mastodon-medium.ndjson \
  --bluesky bluesky-medium.ndjson \
  --label medium_mpi_dev_v1 \
  --output-dir results
```

The MPI program uses one combined run to process both files and splits each NDJSON file by byte range across ranks before merging the partial summaries on rank 0.

## 9. Prepared Spartan scripts

Prepared job scripts:

- `spartan/slurm_serial_1node_1core.sh`
- `spartan/slurm_mpi_1node_8cores.sh`
- `spartan/slurm_mpi_2nodes_8cores.sh`

Example usage on Spartan:

```bash
sbatch spartan/slurm_serial_1node_1core.sh spartan_large_serial_v3
sbatch spartan/slurm_mpi_1node_8cores.sh large_mpi_1node8cores_v1
sbatch spartan/slurm_mpi_2nodes_8cores.sh large_mpi_2nodes8cores_v1
```

## 10. Suggested next step

Use the serial baseline records as the reference point for the assignment benchmarks, then run the MPI version on Spartan for the `1 node, 8 cores` and `2 nodes, 8 cores` configurations required by the PDF.
