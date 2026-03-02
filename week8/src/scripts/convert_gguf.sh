#!/bin/bash

# Setting up
echo "Setting up llama.cpp..."
if [ ! -d "llama.cpp" ]; then
    git clone https://github.com/ggerganov/llama.cpp
fi
cd llama.cpp

# Building
echo "Building llama.cpp..."
cmake -B build
cmake --build build --config Release -j 2

# Installing dependencies
echo "Installing dependencies..."
pip install -q -U gguf sentencepiece transformers tokenizers

# Converting
echo "Converting model..."
python3 convert_hf_to_gguf.py ../src/merged_model --outfile ../src/quantized/model-f16.gguf --outtype f16

# Quantizing
echo "Quantizing model..."
./build/bin/llama-quantize ../src/quantized/model-f16.gguf ../src/quantized/model.gguf q4_0

echo "GGUF conversion complete! Saved to ./src/quantized/model.gguf"
