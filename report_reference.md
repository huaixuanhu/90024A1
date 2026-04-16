## Results

The final application was evaluated on the COMP90024 large Mastodon and BlueSky datasets using the three configurations required in the assignment: `1 node, 1 core`, `1 node, 8 cores`, and `2 nodes, 8 cores (4 cores per node)`. The serial baseline run, `spartan_large_serial_v2`, completed in `1909.675178` seconds. The MPI run on `1 node, 8 cores`, `spartan_large_mpi_1node8cores_v1`, completed in `202.737180` seconds. The MPI run on `2 nodes, 8 cores`, `spartan_large_mpi_2nodes8cores_v1`, completed in `200.984948` seconds. Relative to the serial baseline, the observed speedups were `9.4195x` for `1 node, 8 cores` and `9.5016x` for `2 nodes, 8 cores`.

Table 1. Execution time comparison on the large datasets.

| Configuration | Run label | Elapsed time (s) | Elapsed time (min) | Speedup vs serial |
| --- | --- | ---: | ---: | ---: |
| 1 node, 1 core | `spartan_large_serial_v2` | 1909.675178 | 31.8280 | 1.0000x |
| 1 node, 8 cores | `spartan_large_mpi_1node8cores_v1` | 202.737180 | 3.3790 | 9.4195x |
| 2 nodes, 8 cores | `spartan_large_mpi_2nodes8cores_v1` | 200.984948 | 3.3497 | 9.5016x |

The language-counting results were identical across the serial and MPI runs. For Mastodon, the large file contained `27,228,181` lines, of which `26,583,380` records were counted and `644,801` records were skipped; no invalid JSON lines were observed. For BlueSky, the large file contained `77,833,047` lines, with `77,191,325` counted records and `641,722` skipped records; again, no invalid JSON lines were observed. This consistency indicates that the MPI implementation preserved correctness while reducing runtime.

Table 2. Large dataset processing summary.

| Dataset | Total lines | Counted records | Counted language assignments | Skipped records | Invalid JSON |
| --- | ---: | ---: | ---: | ---: | ---: |
| Mastodon | 27,228,181 | 26,583,380 | 26,583,380 | 644,801 | 0 |
| BlueSky | 77,833,047 | 77,191,325 | 77,830,013 | 641,722 | 0 |

In the final large-file output, English was by far the dominant language on both platforms. For Mastodon, the most frequent codes were `en` (`22,492,294`), `de` (`1,635,575`), `es` (`385,703`), `fr` (`383,728`), and `zh` (`289,853`). For BlueSky, the most frequent codes were `en` (`72,772,745`), `de` (`2,103,551`), `es` (`635,915`), `fr` (`482,958`), and `pt` (`269,539`).

Table 3. Top language codes in the large datasets.

| Rank | Mastodon | Frequency | BlueSky | Frequency |
| --- | --- | ---: | --- | ---: |
| 1 | `en` | 22,492,294 | `en` | 72,772,745 |
| 2 | `de` | 1,635,575 | `de` | 2,103,551 |
| 3 | `es` | 385,703 | `es` | 635,915 |
| 4 | `fr` | 383,728 | `fr` | 482,958 |
| 5 | `zh` | 289,853 | `pt` | 269,539 |

A number of non-standard or region-specific codes were also preserved in the output rather than being forcibly remapped. Examples include `zh-cn` and `en-us` in Mastodon, and `en-au`, `en-us`, and `angika` in BlueSky. These values were retained in raw form so that the benchmark results reflected the original dataset content.

## Discussion

The main result of the benchmark is that moving from the serial baseline to the MPI implementation produced a substantial reduction in runtime. The serial run took about `31.8` minutes, while both MPI runs completed in about `3.35-3.38` minutes. This shows that the application benefits strongly from parallel execution, which is reasonable because the core workload consists of repeatedly reading NDJSON records, extracting language fields, normalizing codes, and updating frequency counts across very large files.

At the same time, the difference between the two MPI configurations was very small. The `1 node, 8 cores` run took `202.737180` seconds, while the `2 nodes, 8 cores` run took `200.984948` seconds. In other words, doubling the number of nodes while keeping the total number of processes fixed produced only a marginal improvement. This suggests that after the move from `1 core` to `8 processes`, the dominant bottleneck was no longer pure computation. Instead, the workload appears to be limited by factors such as file I/O, startup overhead, synchronization, and the final reduction of partial results on the root process.

This behavior is consistent with Amdahl’s Law. A large fraction of the application is parallelizable because different ranks can process different byte ranges of the input files independently. However, not every part of the program can be parallelized. The application still contains serial components, including program startup, argument parsing, file partition setup, communication, and final aggregation of counters. Once the parallel portion has already been accelerated significantly, the remaining serial fraction becomes more visible, which limits the additional gain from spreading the same total number of processes across more than one node.

The observed speedups are slightly greater than `8x` relative to the serial baseline. This should be interpreted carefully. In theory, an 8-process run would not normally be expected to achieve perfect efficiency greater than `100%`. In this case, the measured result is best treated as an observed benchmark outcome on a shared HPC system, not as evidence of ideal scaling. Several practical factors may contribute to this effect, including differences in Python runtime versions between the serial and MPI environments, filesystem caching effects, different node characteristics, and the fact that the assignment measures whole-job execution time on a real shared platform rather than a controlled microbenchmark. For that reason, the MPI runs should be discussed as clearly faster in practice, while avoiding claims of perfect or superlinear scalability in the theoretical sense.

From a data perspective, the results also show that both platforms are dominated by English-language posts, with German clearly the second-largest language in both datasets. At the same time, the retained non-standard codes highlight that real-world social media data does not always follow a strict ISO-639 pattern. Preserving these values during counting was useful because it kept the benchmark faithful to the original data and made it possible to discuss data-quality issues explicitly rather than hiding them through early normalization.

Overall, the benchmarking exercise shows that the application is correct across serial and MPI executions, scales well from `1 core` to `8 processes`, and gains little additional benefit from distributing the same 8 processes across two nodes. This is a useful practical outcome for HPC analysis: adding more hardware does not automatically produce proportionally better performance, especially when the workload includes non-parallel overheads and large-scale file I/O.
