# COMP90024 Assignment 1 Local Setup

This folder is set up for local data exploration and a serial baseline before moving the final program to SPARTAN.

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

## 4. What the baseline reports

- Total lines
- Successfully parsed JSON records
- Skipped records and skip reasons
- Detected language field paths
- Language value types such as `str` or `list`
- Full language frequency table
- Suspicious non-standard codes kept in raw form

## 5. Current local observations

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


## 6. Suggested next step

Use these local baseline results as the reference point for the actual assignment program, then move the reusable parsing logic into a cleaner serial script that can later be adapted for MPI and SLURM.
