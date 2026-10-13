# stateaxis-one-step-scheduling

Extension ID: `org.vllm-hust.stateaxis-one-step-scheduling`

This active experimental MOD is the independently reviewable scheduling
contract for StateAxis issue
[#4](https://github.com/Qixin-Gaoke/stateaxis/issues/4). Shuhao Zhang (Tony) is
directly responsible; no advisor is declared.

The v0.2 mechanism creates, validates and consumes an exact control-plan
proposal in the same scheduling turn. Authority is granted only when request
order, state-slot budget and KV-block budget match. Proposals are single-use;
stale state, mismatch or executor error rolls back to the control path and the
contract fails closed.

This revision does **not** schedule one batch ahead and does **not** overlap CPU
planning with executor work. `proposal_horizon_batches` is zero and
`executor_overlap` is false. The name records the original research direction;
the manifest records the narrower mechanism that actually exists.

## Activation

Activation is default-off and must go through vLLM-HUST Extension Manager/ECPA:

```bash
python -m pip install .
VLLM_HUST_EXT_CONFIG=evidence/ecpa-contract-20261011/manager-config.json \
  vllm-hust-ext extension check \
  org.vllm-hust.stateaxis-one-step-scheduling
VLLM_HUST_EXT_CONFIG=evidence/ecpa-contract-20261011/manager-config.json \
  vllm-hust-ext extension plan \
  org.vllm-hust.stateaxis-one-step-scheduling
```

StateAxis accepts only version `0.2.0` and the exact research-manifest SHA-256.
Legacy environment-variable activation is rejected. Rollback is to disable or
forget the extension, which restores the unchanged control scheduler.

## Evidence boundary

The retained Qwen2.5-14B real-NPU 3+3 matched result measured a `1.0047x`
median throughput ratio, only two positive paired signs, and no significant
difference. Its 234 authority applications were exact with zero fallback or
mismatch. A later upper-bound analysis found a maximum impossible all-gap
removal ceiling of `2.9798%`, below the preregistered `5%` threshold.
The complete R8 and R10 evidence bundles are vendored under `evidence/` with
repo-local SHA-256 manifests.

Current Manifest 0.3 Manager, managed assembly, matched runtime exactness,
effect-counter, rollback and lifecycle checks pass. These results do not turn
the historical negative into a speedup claim and do not establish executor
overlap. See [EVIDENCE.md](EVIDENCE.md).

## Validate

```bash
python -m pip install -e '.[test]'
ruff check .
ruff format --check .
pytest -q
python -m build
```
