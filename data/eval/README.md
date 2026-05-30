# Evaluation data (paper §4.1–4.2)

| File | Rows | Use |
|------|------|-----|
| `harmful_validation.csv` | 507 | Harmful prompts + GCG/AutoDAN/PAIR variants (same schema as training); for `eval.py` ASR during development |
| `combined_test_dataset.csv` | 1,022 | **Test** harmful set: AdvBench + HarmBench + JailbreakBench (`dataset` column); includes `Original Prompt` (= `goal`) |
| `frr_validation.csv` | 500 | Benign prompts for validation FRR (`Original Prompt`) |
| `frr_test.csv` | 210 | Benign **test** FRR set (`Original Prompt` derived from `adversarial`) |

## Run evaluation

```bash
mkdir -p outputs
python eval/eval.py \
  --model-profile llama_2_7b_chat \
  --resume-from ./checkpoints/dcl_epoch5 \
  --validation-data data/eval/harmful_validation.csv \
  --benign-validation-data data/eval/frr_validation.csv \
  --eval-mode seen-family
```

For **test-benchmark** ASR (AdvBench / HarmBench / JBB), point `--validation-data` at `data/eval/combined_test_dataset.csv` and slice by `dataset` when aggregating (or use the paper’s full eval matrix scripts if restored).
