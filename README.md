# Directed Consistency Learning

Code and assets for **Directed Consistency Learning for Robust LLM Alignment Against Adversarial Jailbreaks** (NeurIPS 2026, under review).

Anonymous review URL (paper): https://anonymous.4open.science/r/directed-consistency-learning-0654/

## Released assets

| Asset | Location |
|-------|----------|
| **MaliciousInstruct++** (1k goals) + data card | [`data/MaliciousInstruct++/`](data/MaliciousInstruct%2B%2B/) |
| **Full training corpus** (~3k + variants) | [`data/train/`](data/train/) |
| **Evaluation CSVs** | [`data/eval/`](data/eval/) |
| **Training** | [`train.py`](train.py) |
| **Evaluation** | [`eval/eval.py`](eval/eval.py) |

## Install

```bash
pip install -r requirements.txt
huggingface-cli login
```

## Train (DCL)

Default table: `data/train/train_plus_validation.csv` (2,996 rows with GCG / AutoDAN / PAIR neighbours).

```bash
python train.py \
  --model-profile llama_2_7b_chat \
  --training-data data/train/train_plus_validation.csv \
  --finetuned-llm-path ./checkpoints/dcl \
  --lr 2e-5 \
  --lambda-val 0.1 \
  --epsilon -1.0 \
  --lm-loss-input clean \
  --total-epochs 5 \
  --start-epoch 1
```

**Adversarial SFT baseline:** `--lm-loss-input perturbed --lambda-val 0`.

**Held-out family training:** `--eval-mode unseen-family --unseen-family gcg`.

See [`data/train/README.md`](data/train/README.md).

## Evaluate

```bash
mkdir -p outputs
python eval/eval.py \
  --model-profile llama_2_7b_chat \
  --resume-from ./checkpoints/dcl_epoch5 \
  --validation-data data/eval/harmful_validation.csv \
  --benign-validation-data data/eval/frr_validation.csv \
  --eval-mode seen-family
```

**Test benchmarks** (AdvBench / HarmBench / JailbreakBench): use `data/eval/combined_test_dataset.csv`.

Details: [`data/eval/README.md`](data/eval/README.md).

## Layout

```
train.py
model_profiles.py
eval/eval.py, eval/eval_helpers.py
data/train/              # train.csv, validation.csv, train_plus_validation.csv
data/eval/               # harmful + benign eval splits
data/MaliciousInstruct++/
models/                  # model card + HF adapter URLs
scripts/
```

## Citation

```bibtex
@inproceedings{ahn2026dcl,
  title={Directed Consistency Learning for Robust {LLM} Alignment Against Adversarial Jailbreaks},
  author={Ahn, Andrew},
  booktitle={Advances in Neural Information Processing Systems},
  year={2026},
  note={Under review}
}
```

MIT — [LICENSE](LICENSE).
