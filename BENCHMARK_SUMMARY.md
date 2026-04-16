# Benchmark Summary

## Scope

This file collects the currently relevant serial benchmark records for local development and Spartan execution. It is intended as a report-writing helper and as a compact context file for later human-agent collaboration.

The authoritative detailed records are still the JSON summaries in `results/` and the combined formal run log in `results/run_log.jsonl`.

## Current authoritative serial runs

### Local laptop serial verification

| Label | Platform | Config | Start | Finish | Elapsed |
| --- | --- | --- | --- | --- | --- |
| `small_serial_v1` | macOS, Python 3.14.2 | 1 node, 1 process, 1 CPU | 2026-04-16T01:25:59.603+10:00 | 2026-04-16T01:25:59.623+10:00 | 0.019436 s |
| `medium_serial_v1` | macOS, Python 3.14.2 | 1 node, 1 process, 1 CPU | 2026-04-16T01:25:59.603+10:00 | 2026-04-16T01:25:59.777+10:00 | 0.174313 s |

Artifacts:
- `results/small_serial_v1_output.txt`
- `results/small_serial_v1_summary.json`
- `results/medium_serial_v1_output.txt`
- `results/medium_serial_v1_summary.json`

### Spartan serial verification and baseline

| Label | Platform | Config | Start | Finish | Elapsed |
| --- | --- | --- | --- | --- | --- |
| `spartan_small_serial_v3` | Spartan, Python 3.9.21, host `spartan-bm028` | 1 node, 1 process, 1 CPU | 2026-04-16T02:12:46.672+10:00 | 2026-04-16T02:12:46.726+10:00 | 0.053888 s |
| `spartan_medium_serial_v3` | Spartan, Python 3.9.21, host `spartan-bm046` | 1 node, 1 process, 1 CPU | 2026-04-16T02:12:46.540+10:00 | 2026-04-16T02:12:47.051+10:00 | 0.510746 s |
| `spartan_large_serial_v2` | Spartan, Python 3.9.21, host `spartan-bm010` | 1 node, 1 process, 1 CPU | 2026-04-16T02:12:52.445+10:00 | 2026-04-16T02:44:42.120+10:00 | 1909.675178 s |

Artifacts:
- `results/spartan_small_serial_v3_output.txt`
- `results/spartan_small_serial_v3_summary.json`
- `results/spartan_medium_serial_v3_output.txt`
- `results/spartan_medium_serial_v3_summary.json`
- `results/spartan_large_serial_v2_output.txt`
- `results/spartan_large_serial_v2_summary.json`
- `results/slurm_large_serial_v2_23970581.out`

## MPI validation runs completed on Spartan

These are development-validation runs used to confirm that the new MPI program produces the same counts as the serial baseline before launching the final large MPI benchmarks.

| Label | Platform | Config | Start | Finish | Elapsed |
| --- | --- | --- | --- | --- | --- |
| `spartan_small_mpi_1node8cores_v1` | Spartan, Python 3.12.3, host `spartan-bm153` | 1 node, 8 processes, 1 CPU per process | 2026-04-16T15:21:27.678+10:00 | 2026-04-16T15:21:27.686+10:00 | 0.007840 s |
| `spartan_small_mpi_2nodes8cores_v1` | Spartan, Python 3.12.3, hosts `spartan-bm153`, `spartan-bm154` | 2 nodes, 8 processes, 1 CPU per process | 2026-04-16T15:21:27.583+10:00 | 2026-04-16T15:21:27.601+10:00 | 0.018184 s |
| `spartan_medium_mpi_1node8cores_v1` | Spartan, Python 3.12.3, host `spartan-bm153` | 1 node, 8 processes, 1 CPU per process | 2026-04-16T15:21:35.157+10:00 | 2026-04-16T15:21:35.239+10:00 | 0.081629 s |

Artifacts:
- `results/spartan_small_mpi_1node8cores_v1_output.txt`
- `results/spartan_small_mpi_1node8cores_v1_summary.json`
- `results/spartan_small_mpi_2nodes8cores_v1_output.txt`
- `results/spartan_small_mpi_2nodes8cores_v1_summary.json`
- `results/spartan_medium_mpi_1node8cores_v1_output.txt`
- `results/spartan_medium_mpi_1node8cores_v1_summary.json`
- `results/comp90024_mpi_1n8c_23992173.out`
- `results/comp90024_mpi_1n8c_23992174.out`
- `results/comp90024_mpi_2n8c_23992175.out`

## Dataset sizes used in the formal serial runs

| Dataset pair | Mastodon bytes | BlueSky bytes |
| --- | --- | --- |
| `small` | 4,136,412 | 1,550,329 |
| `medium` | 38,281,445 | 18,097,777 |
| `large` | 105,221,465,642 | 129,852,005,630 |

## Result highlights

### `small`

| Source | Total lines | Counted records | Counted language assignments | Skipped records | Invalid JSON |
| --- | --- | --- | --- | --- | --- |
| Mastodon | 1,061 | 1,019 | 1,019 | 42 | 0 |
| BlueSky | 941 | 914 | 917 | 27 | 0 |

Top language counts:
- Mastodon: `en=875`, `es=50`, `de=39`
- BlueSky: `en=867`, `de=22`, `ja=9`

Suspicious non-standard codes:
- Mastodon: `zh-cn=4`
- BlueSky: none detected

### `medium`

| Source | Total lines | Counted records | Counted language assignments | Skipped records | Invalid JSON |
| --- | --- | --- | --- | --- | --- |
| Mastodon | 9,738 | 9,291 | 9,291 | 447 | 0 |
| BlueSky | 10,886 | 10,781 | 10,826 | 105 | 0 |

Top language counts:
- Mastodon: `en=8201`, `es=289`, `de=223`
- BlueSky: `en=10280`, `de=179`, `ja=114`

Suspicious non-standard codes:
- Mastodon: `zh-cn=50`, `zh-tw=5`
- BlueSky: `en-us=1`

### `large`

| Source | Total lines | Counted records | Counted language assignments | Skipped records | Invalid JSON |
| --- | --- | --- | --- | --- | --- |
| Mastodon | 27,228,181 | 26,583,380 | 26,583,380 | 644,801 | 0 |
| BlueSky | 77,833,047 | 77,191,325 | 77,830,013 | 641,722 | 0 |

Top language counts:
- Mastodon: `en=22492294`, `de=1635575`, `es=385703`
- BlueSky: `en=72772745`, `de=2103551`, `es=635915`

Selected suspicious non-standard codes:
- Mastodon: `zh-cn=33258`, `en-us=28446`, `zh-tw=4720`, `zh-hk=1025`
- BlueSky: `en-au=120529`, `en-us=6553`, `angika=3547`, `en-gb=1854`

## Notes for later report writing

- For the assignment's final benchmark comparison, the current serial baseline to cite on Spartan is `spartan_large_serial_v2`.
- `small` and `medium` were also re-run successfully on Spartan so there is a clean verification path from laptop development to cluster execution.
- The current MPI implementation has already been validated on Spartan against the `small` and `medium` datasets, and the result counts match the serial baseline for those datasets.
- The local `results/run_log.jsonl` now contains both local serial runs and the synchronized Spartan serial runs.
- Earlier Spartan labels `spartan_small_serial_v1` and `spartan_medium_serial_v1` still exist remotely, but the cleaner current verification set is `v3` for `small` and `medium`, plus `v2` for `large`.
- The large MPI benchmark runs required by the assignment are still pending. The remaining formal targets are:
  - `large`, `1 node`, `8 cores`
  - `large`, `2 nodes`, `8 cores` with `4 cores per node`
