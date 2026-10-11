import hashlib
import json
from pathlib import Path

import pytest
from vllm_hust_ext.manifest import activation_blocker, load_manifest

import stateaxis_one_step_scheduling
from stateaxis_one_step_scheduling import OneStepSchedulingConfig, one_step_scheduling


def test_manifest_is_active_and_hash_bound() -> None:
    package = Path(stateaxis_one_step_scheduling.__file__).parent
    repo = package.parents[1]
    path = package / "vllm-hust-extension-v0.3.json"
    manifest = load_manifest(path)
    assert activation_blocker(manifest) is None
    raw = json.loads(path.read_text())
    expected = raw["activation"]["additional_config"]["stateaxis_mod"][
        "manifest_sha256"
    ]
    assert (
        hashlib.sha256((repo / "RESEARCH_MANIFEST.json").read_bytes()).hexdigest()
        == expected
    )


def test_contract_is_exact_and_does_not_claim_overlap() -> None:
    assert one_step_scheduling() == OneStepSchedulingConfig()
    with pytest.raises(ValueError, match="reviewed contract"):
        OneStepSchedulingConfig(executor_overlap=True)
