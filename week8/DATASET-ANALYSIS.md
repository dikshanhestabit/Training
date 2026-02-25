# Dataset Analysis 

## 1. Overview
This dataset is designed for instruction tuning an LLM in the **Polyglot Coding** domain. It has been curated to provide high-entropy, technically deep samples for QA, Reasoning, and Extraction tasks, avoiding grammatical artifacts and repetitive stylistic bias.

- **Total Training Samples**: 1,000 (Cleaned)
- **Total Validation Samples**: 300 (Cleaned)
- **Avg Token Length**: 93.9 tokens
- **Format**: JSONL (Consistent Schema: `instruction`, `input`, `output`)

## 2. Distribution Analysis
The dataset maintains an approximately balanced distribution for both the Training and Validation sets.

### Train Set Distribution
```text
Extraction  342 (34.2%)
Reasoning   335 (33.5%)
QA          323 (32.3%)
```

### Val Set Distribution
```text
QA          110 (36.7%)
Reasoning   98  (32.7%)
Extraction  92  (30.6%)
```

## 3. Token Length Statistics (Train)
Analyzed using the `Qwen/Qwen2.5-1.5B` tokenizer.

| Metric | Value |
|--------|-------|
| Mean Length | 93.9 tokens |
| Median | 99.0 tokens |
| Min / Max | 59 / 122 tokens |
| Std Dev | 16.0 tokens |

## 4. Cleaning & Quality Control
- **Deduplication**: Successfully removed duplicates.
- **Outlier Removal**: samples flagged at the 3-sigma (Z > 3.0) threshold.
- **De-biasing**: Implemented dynamic intro hooks and randomized prepositions to eliminate repetitive stylistic patterns.
- **Semantic Integrity**: High-quality technical facts (MRO, Event Loop, Borrow Checker, etc.) provide deep learning signal for PEFT adaptation.


