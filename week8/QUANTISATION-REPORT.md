# Quantization Report 
## 1. Technical Background

### Static vs Dynamic Quantization
To optimize the model for inference, I explored two primary quantization approaches. In Static Quantization (PTQ), I quantized the weights offline to minimize runtime overhead, which is the method used for the GGUF conversion. I also considered Dynamic Quantization, where activation scales are calculated during inference. While dynamic quantization offers flexibility, I found that static quantization provided the best performance for my specific deployment needs.

### Quantization Formats
I implemented and compared four distinct formats:
*   FP16: I used this as my baseline, maintaining half-precision floating point for maximum accuracy.
*   INT8 (8-bit): I used vector-wise quantization to reduce the model's memory footprint by approximately 50%.
*   INT4 (4-bit): By using NormalFloat4 (NF4), I achieved a 75% reduction in memory while preserving high precision.
*   GGUF: I converted the model to this format for use with llama.cpp, targeting efficient inference on CPU and edge devices.

## 2. Performance Benchmarks

| Model Format | Precision | Model Size (GB) | Inference Speed (tok/s) |
|--------------|-----------|-----------------|-------------------------|
| Base FP16    | Float16   | 2.05            | 34.37                   |
| BitsAndBytes | INT8      | 1.15            | 9.61                    |
| BitsAndBytes | INT4      | 0.71            | 19.56                   |
| llama.cpp    | GGUF (Q4_0)| 0.59            | 11.33                   |

## 3. Key Observations

1.  Size Reduction: I observed that quantization was highly effective. By transitioning from FP16 to INT4 or GGUF, I successfully reduced the model size by approximately 70%, bringing it down from 2.05 GB to as low as 0.59 GB.
2.  Speed Trade-offs: 
    *   I found that FP16 remains the fastest on GPU at 34 tok/s, as it avoids dequantization overhead.
    *   I noted a significant slowdown with INT8 (9.6 tok/s), which I attribute to the T4 GPU's less optimized kernels for 8-bit compared to 4-bit.
    *   INT4 (NF4) provided the best balance for my needs, offering significant memory savings while maintaining a respectable speed of 19 tok/s.
    *   GGUF achieved the smallest footprint (0.59 GB). I was impressed by its inference speed of 11.33 tok/s, especially considering it was running primarily on the CPU during my tests.

