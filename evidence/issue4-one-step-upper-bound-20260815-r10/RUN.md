# Issue #4 real-NPU one-step feasibility upper bound

Correctness custody: **12/12 source runs exact**. Candidate execution: **no**.
Decision: **stop; optimistic upper bound is below the 5% target**.

`result.json` was generated deterministically with:

```text
python3 benchmarks/audit_issue4_one_step_upper_bound.py \
  --source-root /home/shuhao/statecentric-ascend-engine/.benchmarks \
  --output results/issue4-one-step-upper-bound-20260815-r10/result.json
```

The source manifest binds every append-only raw result. The calculation removes
the whole executor-finish-to-next-enqueue interval, so it is intentionally more
optimistic than any realizable one-step CPU planning implementation.
