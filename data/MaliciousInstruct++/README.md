---
license: mit
task_categories:
  - text-classification
language:
  - en
tags:
  - safety
  - jailbreak
  - harmful-content
pretty_name: MaliciousInstruct++
size_categories:
  - 1K<n<10K
---

# MaliciousInstruct++

**1,000** harmful user-intent strings used as one third of the 3,000-prompt training corpus in *Directed Consistency Learning for Robust LLM Alignment Against Adversarial Jailbreaks* (NeurIPS 2026, under review). The remaining 2,000 training prompts come from [CySecBench](https://huggingface.co/datasets/CysecBench/CySecBench) and [WildJailbreak](https://huggingface.co/datasets/allenai/wildjailbreak) (not redistributed here).

## Files

| File | Description |
|------|-------------|
| `MaliciousInstruct_1k.csv` | One column `goal` per row (UTF-8). |

## Construction (Section 4.1)

1. **Few-shot seeds:** Original [MaliciousInstruct](https://arxiv.org/abs/2312.04724) examples (see `scripts/generate_maliciousinstruct_candidates.py`).
2. **Candidate generation:** ~20,000 new instructions from an uncensored helper LLM (`LLM_NAME` env var in the script).
3. **Deduplication:** `all-mpnet-base-v2` embeddings; hierarchical clustering; merge cutoff cosine distance 0.88; keep one prompt per cluster until 1,000 remain.

To regenerate candidates (not the final 1k list), run:

```bash
export LLM_NAME=<your_uncensored_hf_model>
python scripts/generate_maliciousinstruct_candidates.py
```

The released `MaliciousInstruct_1k.csv` is the **final filtered list** used in experiments.

## Usage

```python
import pandas as pd
df = pd.read_csv("MaliciousInstruct_1k.csv")
prompts = df["goal"].tolist()
```

The full ~3k training table (this slice + CySecBench + WildJailbreak, with perturbations and refusals) is in [`../train/`](../train/). This file is the MaliciousInstruct++ portion only.

## Ethics & license

- **Research use only.** Prompts are intentionally harmful; do not use to attack production systems or harass individuals.
- **No warranty.** Dataset may contain biased or overlapping content despite deduplication.
- **License:** MIT (same as repository). Upstream MaliciousInstruct has its own terms; cite [Huang et al., 2024](https://arxiv.org/abs/2312.04724) when using the seed concept.

## Citation

If you use this slice, cite the paper (see repository [CITATION.cff](../../CITATION.cff)).
