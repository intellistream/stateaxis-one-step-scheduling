# Issue #4 forward authority — real NPU 3+3

Correctness: **PASS**. Performance conclusion: **no_significant_difference**.

- Median successful-request throughput control/candidate: `7.994/8.031 req/s` (ratio `1.0047x`)
- Throughput CV control/candidate: `0.0045/0.0124`
- Paired candidate-faster signs: `2/3`
- Candidate authority/fallback: `234/0`
- HBM peak median control/candidate: `52686.56/52686.25 MiB`

The feature remains default-off. Request latency excludes process startup. All six raw runs are retained.
