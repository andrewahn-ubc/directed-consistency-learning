"""Default base LLM and safety-critic paths for training."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Literal

HingeStyle = Literal["llama_guard", "mistral_self_twin"]


def _path(env_var: str, default: str) -> str:
    return os.environ.get(env_var, default)


@dataclass(frozen=True)
class ModelProfile:
    key: str
    base_llm: str
    hinge_guard_path: str
    hinge_style: HingeStyle
    default_system_prompt: str | None
    eval_refusal_judge_path: str
    eval_jailbreak_classifier_path: str


MODEL_PROFILES: dict[str, ModelProfile] = {
    "llama_2_7b_chat": ModelProfile(
        key="llama_2_7b_chat",
        base_llm=_path("LLAMA2_7B_CHAT_PATH", "meta-llama/Llama-2-7b-chat-hf"),
        hinge_guard_path=_path("LLAMA_GUARD_7B_PATH", "meta-llama/LlamaGuard-7b"),
        hinge_style="llama_guard",
        default_system_prompt=None,
        eval_refusal_judge_path=_path(
            "MISTRAL_7B_JUDGE_PATH", "mistralai/Mistral-7B-Instruct-v0.2"
        ),
        eval_jailbreak_classifier_path=_path(
            "HARMBENCH_CLS_PATH", "cais/HarmBench-Mistral-7b-val-cls"
        ),
    ),
    "llama_3_8b_instruct": ModelProfile(
        key="llama_3_8b_instruct",
        base_llm=_path("LLAMA3_8B_INSTRUCT_PATH", "meta-llama/Meta-Llama-3-8B-Instruct"),
        hinge_guard_path=_path("LLAMA_GUARD_2_PATH", "meta-llama/LlamaGuard-2-8b"),
        hinge_style="llama_guard",
        default_system_prompt=None,
        eval_refusal_judge_path=_path(
            "MISTRAL_7B_JUDGE_PATH", "mistralai/Mistral-7B-Instruct-v0.2"
        ),
        eval_jailbreak_classifier_path=_path(
            "HARMBENCH_CLS_PATH", "cais/HarmBench-Mistral-7b-val-cls"
        ),
    ),
    "mistral_7b_instruct": ModelProfile(
        key="mistral_7b_instruct",
        base_llm=_path("MISTRAL_7B_INSTRUCT_PATH", "mistralai/Mistral-7B-Instruct-v0.2"),
        hinge_guard_path=_path("MISTRAL_7B_INSTRUCT_PATH", "mistralai/Mistral-7B-Instruct-v0.2"),
        hinge_style="mistral_self_twin",
        default_system_prompt=None,
        eval_refusal_judge_path=_path(
            "MISTRAL_7B_JUDGE_PATH", "mistralai/Mistral-7B-Instruct-v0.2"
        ),
        eval_jailbreak_classifier_path=_path(
            "HARMBENCH_CLS_PATH", "cais/HarmBench-Mistral-7b-val-cls"
        ),
    ),
}

MODEL_PROFILE_CHOICES: tuple[str, ...] = tuple(sorted(MODEL_PROFILES.keys()))
DEFAULT_MODEL_PROFILE = "llama_2_7b_chat"


def resolve_profile(name: str | None) -> ModelProfile:
    key = (name or DEFAULT_MODEL_PROFILE).strip()
    if key not in MODEL_PROFILES:
        raise ValueError(
            f"Unknown model profile {key!r}. Choose one of: {', '.join(MODEL_PROFILE_CHOICES)}"
        )
    return MODEL_PROFILES[key]


MISTRAL_SELF_HINGE_PROMPT = """[INST] Task: Check if the following PARTIAL Assistant response is starting to generate unsafe content according to our safety policy. The reply may be incomplete; still label it unsafe if it clearly trends toward disallowed content (violence, sexual exploitation of minors, self-harm instructions, illegal weapons trafficking, malware, severe hate targeting protected groups). If it is benign, a refusal, or too ambiguous to judge as harmful, label it safe.

You must answer with exactly one lowercase word as the first token after this instruction block: either unsafe or safe.

<BEGIN CONVERSATION>
"""
