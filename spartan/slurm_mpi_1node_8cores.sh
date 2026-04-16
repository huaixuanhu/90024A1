#!/bin/bash
#SBATCH --job-name=comp90024_mpi_1n8c
#SBATCH --nodes=1
#SBATCH --ntasks=8
#SBATCH --cpus-per-task=1
#SBATCH --time=02:00:00
#SBATCH --output=results/%x_%j.out

set -euo pipefail

LABEL="${1:?Usage: sbatch $0 <label> [mastodon_path] [bluesky_path] }"
MASTODON_PATH="${2:-mastodon-large.ndjson}"
BLUESKY_PATH="${3:-bluesky-large.ndjson}"

cd "$HOME/90024A1"

module load GCC/13.3.0 OpenMPI/5.0.3 mpi4py/4.0.1

srun python3 mpi_main.py \
  --mastodon "$MASTODON_PATH" \
  --bluesky "$BLUESKY_PATH" \
  --label "$LABEL" \
  --output-dir results
