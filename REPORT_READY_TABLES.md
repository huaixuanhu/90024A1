# Report-Ready Tables

This file collects report-ready tables based on the current authoritative large-file benchmark runs on Spartan.

Primary source files:

- `results/spartan_large_serial_v2_summary.json`
- `results/spartan_large_mpi_1node8cores_v1_summary.json`
- `results/spartan_large_mpi_2nodes8cores_v1_summary.json`
- `results/run_log.jsonl`

## 1. Large Benchmark Configuration Table

| Run label | Mode | Nodes | Processes | CPUs per process | Python | Host / hosts | Start time | Finish time |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `spartan_large_serial_v2` | serial | 1 | 1 | 1 | 3.9.21 | `spartan-bm010` | 2026-04-16 02:12:52 | 2026-04-16 02:44:42 |
| `spartan_large_mpi_1node8cores_v1` | mpi | 1 | 8 | 1 | 3.12.3 | `spartan-bm210` | 2026-04-16 17:41:29 | 2026-04-16 17:44:52 |
| `spartan_large_mpi_2nodes8cores_v1` | mpi | 2 | 8 | 1 | 3.12.3 | `spartan-bm074`, `spartan-bm210` | 2026-04-16 17:41:31 | 2026-04-16 17:44:52 |

## 2. Large Benchmark Time Comparison Table

| Run label | Configuration | Elapsed seconds | Elapsed minutes | Speedup vs serial | Time reduction vs serial |
| --- | --- | --- | --- | --- | --- |
| `spartan_large_serial_v2` | 1 node, 1 core | 1909.675178 | 31.8280 | 1.0000x | 0.0000% |
| `spartan_large_mpi_1node8cores_v1` | 1 node, 8 cores | 202.737180 | 3.3790 | 9.4195x | 89.3837% |
| `spartan_large_mpi_2nodes8cores_v1` | 2 nodes, 8 cores | 200.984948 | 3.3497 | 9.5016x | 89.4754% |

Suggested sentence:

`The large-file serial baseline on Spartan took 1909.675178 seconds, while the MPI version took 202.737180 seconds on 1 node with 8 cores and 200.984948 seconds on 2 nodes with 8 cores.`

## 3. Large Dataset Processing Summary Table

### Mastodon

| Metric | Value |
| --- | --- |
| Input file | `mastodon-large.ndjson` |
| Size in bytes | 105,221,465,642 |
| Total lines | 27,228,181 |
| Parsed JSON lines | 27,228,181 |
| Counted records | 26,583,380 |
| Counted language assignments | 26,583,380 |
| Skipped records | 644,801 |
| Invalid JSON lines | 0 |
| Main language path | `doc.language` |

### BlueSky

| Metric | Value |
| --- | --- |
| Input file | `bluesky-large.ndjson` |
| Size in bytes | 129,852,005,630 |
| Total lines | 77,833,047 |
| Parsed JSON lines | 77,833,047 |
| Counted records | 77,191,325 |
| Counted language assignments | 77,830,013 |
| Skipped records | 641,722 |
| Invalid JSON lines | 0 |
| Main language path | `record.langs` |

Suggested sentence:

`No invalid JSON lines were observed in the final large-file benchmark runs. The Mastodon large file contained 27,228,181 lines and the BlueSky large file contained 77,833,047 lines.`

## 4. Large Result Table: Mastodon Top 15 Language Codes

| Rank | Language code | Frequency |
| --- | --- | --- |
| 1 | `en` | 22,492,294 |
| 2 | `de` | 1,635,575 |
| 3 | `es` | 385,703 |
| 4 | `fr` | 383,728 |
| 5 | `zh` | 289,853 |
| 6 | `nl` | 221,422 |
| 7 | `ru` | 189,917 |
| 8 | `ja` | 178,651 |
| 9 | `it` | 157,979 |
| 10 | `fi` | 131,992 |
| 11 | `pt` | 97,310 |
| 12 | `sv` | 47,574 |
| 13 | `ca` | 37,845 |
| 14 | `uk` | 35,212 |
| 15 | `zh-cn` | 33,258 |

## 5. Large Result Table: BlueSky Top 15 Language Codes

| Rank | Language code | Frequency |
| --- | --- | --- |
| 1 | `en` | 72,772,745 |
| 2 | `de` | 2,103,551 |
| 3 | `es` | 635,915 |
| 4 | `fr` | 482,958 |
| 5 | `pt` | 269,539 |
| 6 | `pl` | 228,583 |
| 7 | `ja` | 227,321 |
| 8 | `fi` | 143,567 |
| 9 | `en-au` | 120,529 |
| 10 | `nl` | 109,243 |
| 11 | `it` | 80,743 |
| 12 | `sv` | 70,383 |
| 13 | `tr` | 65,374 |
| 14 | `sq` | 34,802 |
| 15 | `ak` | 33,013 |

## 6. Selected Non-standard Language Codes Observed in the Large Data

### Mastodon

| Code | Frequency |
| --- | --- |
| `zh-cn` | 33,258 |
| `en-us` | 28,446 |
| `zh-tw` | 4,720 |
| `en-gb` | 1,593 |
| `zh-hk` | 1,025 |
| `zhcn` | 681 |
| `startrek_it` | 453 |
| `ptpt` | 133 |
| `pt-br` | 131 |
| `squeak` | 75 |

### BlueSky

| Code | Frequency |
| --- | --- |
| `en-au` | 120,529 |
| `en-us` | 6,553 |
| `angika` | 3,547 |
| `en-gb` | 1,854 |
| `ja-jp` | 647 |
| `en-ca` | 189 |
| `fa-ir` | 148 |
| `de-de` | 72 |
| `pt-br` | 69 |
| `fr-fr` | 33 |

Suggested sentence:

`Non-standard or region-specific codes were preserved in raw form during counting, for example zh-cn and en-us in Mastodon, and en-au and angika in BlueSky.`

## 7. Notes You Can Reuse in the Report

- The final application is a single program that processes both the Mastodon and BlueSky files together.
- The serial and MPI large-file runs produced matching totals, skip counts, and language frequency tables.
- The MPI implementation was first validated on the `small` and `medium` datasets before the final `large` benchmarks were launched.
- The observed speedup is greater than 8x relative to the serial baseline. This should be discussed carefully as an observed benchmark result on a shared HPC system rather than treated as a clean theoretical efficiency result.

## 8. Recommended Citation Order

When writing the report, use these files in this order:

1. `REPORT_READY_TABLES.md` for the first draft of tables and sentences.
2. `BENCHMARK_SUMMARY.md` for fuller benchmark context and artifact paths.
3. `results/<label>_summary.json` when you need exact machine-readable values.
4. `results/run_log.jsonl` when comparing many runs quickly.
