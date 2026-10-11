"""One-step scheduling bounded activation contract."""

from __future__ import annotations

from dataclasses import asdict, dataclass

MOD_ID = "org.vllm-hust.stateaxis-one-step-scheduling"


@dataclass(frozen=True, slots=True)
class OneStepSchedulingConfig:
    """Exact same-turn forward-authority scaffold; no executor overlap."""

    enabled: bool = True
    shadow_enabled: bool = True
    authority_enabled: bool = True
    scope: str = "exact-control-plan-same-turn"
    proposal_horizon_batches: int = 0
    executor_overlap: bool = False
    exact_request_order: bool = True
    exact_state_slot_budget: bool = True
    exact_kv_block_budget: bool = True
    single_use_proposal: bool = True
    stale_or_mismatch_rollback: bool = True
    executor_error_rollback: bool = True
    fallback_to_control: bool = True
    fail_closed: bool = True

    def __post_init__(self) -> None:
        expected = {
            "enabled": True,
            "shadow_enabled": True,
            "authority_enabled": True,
            "scope": "exact-control-plan-same-turn",
            "proposal_horizon_batches": 0,
            "executor_overlap": False,
            "exact_request_order": True,
            "exact_state_slot_budget": True,
            "exact_kv_block_budget": True,
            "single_use_proposal": True,
            "stale_or_mismatch_rollback": True,
            "executor_error_rollback": True,
            "fallback_to_control": True,
            "fail_closed": True,
        }
        if asdict(self) != expected:
            raise ValueError("one-step scheduling requires the reviewed contract")


def one_step_scheduling() -> OneStepSchedulingConfig:
    return OneStepSchedulingConfig()


__all__ = ["MOD_ID", "OneStepSchedulingConfig", "one_step_scheduling"]
