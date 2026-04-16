#!/bin/bash
#SBATCH --job-name=comp90024_serial_1n1c
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --time=08:00:00
#SBATCH --output=results/%x_%j.out

set -euo pipefail

LABEL="${1:?Usage: sbatch $0 <label> [mastodon_path] [bluesky_path] }"
MASTODON_PATH="${2:-mastodon-large.ndjson}"
BLUESKY_PATH="${3:-bluesky-large.ndjson}"

cd "$HOME/90024A1"

python3 main.py \
  --mastodon "$MASTODON_PATH" \
  --bluesky "$BLUESKY_PATH" \
  --label "$LABEL" \
  --output-dir results
