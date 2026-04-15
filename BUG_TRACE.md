# Bug Trace

## 2026-04-16 - Spartan serial sbatch argument mismatch

- Context: Re-submitting Spartan serial jobs for `small`, `medium`, and `large`.
- Symptom: The jobs exited in about 1 second with `main.py: error: the following arguments are required: --mastodon, --bluesky`.
- Root cause: The submission command still used the old positional style:
  `python3 main.py mastodon-small.ndjson bluesky-small.ndjson --label ...`
  but the current CLI requires explicit named arguments:
  `python3 main.py --mastodon ... --bluesky ... --label ...`
- Impact: Three trial jobs failed immediately before any real processing started.
- Fix applied: Re-submitted the jobs with the current CLI format and new labels:
  - `spartan_small_serial_v3`
  - `spartan_medium_serial_v3`
  - `spartan_large_serial_v2`
- Prevention rule:
  - Before writing or reusing any `sbatch` command, verify the current CLI with:
    `python3 main.py -h`
  - Treat `main.py` help output as the authority if old notes or old scripts disagree.
  - When a failed attempt is caused by command format only, use a new label for the corrected run so formal records stay clean.
