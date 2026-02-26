# QLoRA Fine-Tuning Training Report

## 1. Overview
This report details the execution and results of fine-tuning a base LLM using QLoRA (Parameter-Efficient Fine-Tuning) with 4-bit quantization.

## 2. Configuration & Hyperparameters

### Model Details
*   **Base Model:** `TinyLlama/TinyLlama-1.1B-Chat-v1.0`
*   **Dataset:** `train_clean.jsonl` (Polyglot Coding Instructions)

### PEFT (LoRA) Configuration
*   **Rank (r):** 16
*   **Alpha:** 32
*   **Dropout:** 0.05
*   **Target Modules:** `["q_proj", "v_proj", "k_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]`

### Training Arguments (Trainer)
*   **Learning Rate (lr):** 2e-4
*   **Batch Size:** 4
*   **Epochs:** 3
*   **Optimizer:** `paged_adamw_8bit`
*   **FP16:** False (Disabled to bypass T4 GradScaler NotImplementedError)

### Memory Saving Strategies
The following techniques were successfully implemented to prevent OOM (Out Of Memory) errors:
*   **4-bit Loading (BitsAndBytes):** Loaded the base model in NF4 format.
*   **Gradient Checkpointing:** Recomputed activations to save memory footprint (`model.config.use_cache = False`).
*   **Sanitization:** Explicitly cast BFloat16 tensors to Float16 to ensure T4 GPU compatibility.

## 3. Results & Deliverables Verification

*    **Trainable Parameters Only ~1-2%:**
    *   **Percentage Trainable:** ~1.8% (Targeted all linear layers for improved technical reasoning).
*    **Loss Optimizing:**
    *   **Start Loss:** 2.1622
    *   **Final Loss:** 0.1142
    *   **Avg Training Loss:** 0.1645
*    **Adapter Weights Saved:** Successfully generated `adapter_model.bin` and `adapter_config.json`.

## 4. Observations & Notes
- **Hardware:** Google Colab T4 GPU.
- **T4 Compatibility:** Successfully bypassed the `BFloat16` NotImplementedError by sanitizing tensors and adjusting mixed-precision settings.
- **Convergence:** Loss optimized from **2.16** down to **0.11**, demonstrating effective adaptation to the Polyglot Coding domain.
- **Performance:** Total training time was ~10 minutes (598.08s) for 1,000 samples over 3 epochs.
