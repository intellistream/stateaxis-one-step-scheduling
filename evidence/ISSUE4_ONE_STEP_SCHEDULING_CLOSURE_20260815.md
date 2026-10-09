# Issue #4 one-step scheduling closure — 2026-08-15

> **Point-in-time closure report, not current repository status.** The canonical
> current classification remains [`NATIVE_ENGINE_STATUS.md`](../../NATIVE_ENGINE_STATUS.md).

## Decision

Close the current one-step-ahead scheduler direction as a measured negative and
keep it disabled. The repository does not claim that every possible async
scheduler has been exhausted; it records that the specified Qwen2.5-14B,
single-NPU mechanism cannot meet its own 5% throughput target.

No new NPU run was needed for this final feasibility decision. R10 reads twelve
already-frozen, real-NPU Qwen2.5-14B runs (c=16/32, o=32/128, three fresh
lifecycles per cell), verifies exactness and source hashes, and recomputes the
complete retained batch timeline. It optimistically removes *every* interval
from one executor finish to the next adjacent enqueue. That interval contains
completion, state publication, commit, requeue, timing and scheduling work;
one-step CPU planning can hide only part of it.

| concurrency | output tokens | median ideal all-gap removal | maximum run |
|---:|---:|---:|---:|
| 16 | 32 | 2.6324% | 2.6575% |
| 16 | 128 | 1.4028% | 1.4559% |
| 32 | 32 | 2.9199% | 2.9798% |
| 32 | 128 | 1.8329% | 1.8901% |

Even the maximum impossible ceiling is 2.9798%, below the preregistered 5%
target before reservation, validation, rollback, cancellation and stale-plan
costs. The prior R8 real-NPU matched 3+3 candidate result independently found
only a 1.0047x median throughput ratio, two positive paired signs out of three,
and no significant difference. Its 234 authority applications, exact outputs
and zero fallback/mismatch demonstrate bounded mechanism correctness, but the
source audit confirms that authority was proposed and consumed in the same
scheduling turn rather than overlapping executor work.

Therefore a production placeholder/reservation state machine is not justified
for this frozen model and acceptance target. The unused candidate remains
default-off; no speedup, vLLM superiority or universal impossibility claim is
made. Full R10 calculation and source custody are under
`results/issue4-one-step-upper-bound-20260815-r10/`; the R8 matched evidence is
under `results/issue4-forward-authority-20260813-r8/`.

## Digest root-cause repair

The final patch also fixes the independent 17/4/4 startup regression that had
made Issue #4 appear unable to run. The old request path retained aggregate
digest `90c08887...` after the compiled-plan leaf changed from `587a400f...` to
`3e7c55ee...`; the worker correctly expected `c3eaa7bc...`. The launcher now
derives the aggregate from all six canonical leaves with the same Rust helper
used by the runtime, passes that exact value to the request client, and writes
an atomic sidecar. Missing or noncanonical leaves fail closed.

Regression coverage includes old-plan-to-new-plan aggregate change,
launcher/request single-source binding, missing/noncanonical leaf rejection,
replacement allocator semantics, shell syntax and Rust digest/runtime tests.
NPU admission additionally requires AICore=0 and conservative available HBM at
least the frozen resident-plan requirement; device exclusivity is not assumed.

## Preserved follow-up boundary

A materially different mechanism may open a new issue only with a new profile
showing at least 5% removable time or another explicit user-facing objective.
It must use a new identity and must not inherit R8/R10 as positive evidence.
