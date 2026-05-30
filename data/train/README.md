# Training data (paper §4.1)

| File | Rows | Use |
|------|------|-----|
| `train.csv` | 2,489 | Semantic **train** split (topic-disjoint clusters) |
| `validation.csv` | 507 | Semantic **validation** split (not used for HP search in paper; for manual checks) |
| `train_plus_validation.csv` | 2,996 | **Default training table** (~3k prompts); concat of train + validation splits |

Each row includes `Original Prompt`, `Original Response`, `GCG Variant`, `AutoDAN Variant`, `PAIR Variant`, plus `dataset` and `goal_cluster` metadata.

```bash
python train.py --training-data data/train/train_plus_validation.csv ...
```

MaliciousInstruct++ goals (1k) are in [`../MaliciousInstruct++/`](../MaliciousInstruct++/); this corpus also includes CySecBench and WildJailbreak-derived rows (`dataset` column).
