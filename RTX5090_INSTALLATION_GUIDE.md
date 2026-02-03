# RTX 5090 Installation Guide for DeepSeek-OCR

## Issue Description

The RTX 5090 uses the Blackwell architecture with CUDA compute capability **sm_120**, which is not supported by the default environment configuration (CUDA 11.8 + PyTorch 2.6.0). This causes the following error:

```
RuntimeError: CUDA error: no kernel image is available for execution on the device
```

## Root Cause

- **RTX 5090**: CUDA compute capability sm_120 (Blackwell architecture)
- **PyTorch 2.6.0 + CUDA 11.8**: Only supports up to sm_90 (Hopper architecture)
- The error occurs during model initialization when creating Conv2d layers in the SAM encoder

## Solution Options

### Option 1: Upgrade to PyTorch 2.7+ with CUDA 12.4+ (RECOMMENDED)

This is the recommended solution as it provides full native support for RTX 5090.

#### Step 1: Create Conda Environment

```bash
conda create -n deepseek-ocr-rtx5090 python=3.12.9 -y
conda activate deepseek-ocr-rtx5090
```

#### Step 2: Install CUDA 12.4+ Toolkit

```bash
# Install CUDA 12.4 or later
# Download from: https://developer.nvidia.com/cuda-downloads
# Or use conda:
conda install cuda -c nvidia/label/cuda-12.4.0
```

#### Step 3: Install PyTorch with CUDA 12.4 Support

```bash
# Option A: Stable release (if available)
pip install torch==2.7.0 torchvision==0.22.0 torchaudio==2.7.0 --index-url https://download.pytorch.org/whl/cu124

# Option B: Nightly build (recommended for latest RTX 5090 support)
pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu124
```

#### Step 4: Install vLLM

```bash
# Option A: Pre-built wheel (if available for CUDA 12.4)
pip install vllm==0.8.5+cu124

# Option B: Build from source
git clone https://github.com/vllm-project/vllm.git
cd vllm
pip install -e .
cd ..
```

#### Step 5: Install Flash Attention

```bash
# Flash Attention needs to be compiled for sm_120
pip install flash-attn==2.7.3 --no-build-isolation

# If the above fails, try building from source:
git clone https://github.com/Dao-AILab/flash-attention.git
cd flash-attention
# Edit setup.py to add sm_120 to supported architectures if needed
python setup.py install
cd ..
```

#### Step 6: Install Other Dependencies

```bash
pip install -r requirements-rtx5090.txt
```

#### Step 7: Verify Installation

```bash
python -c "import torch; print(f'PyTorch version: {torch.__version__}'); print(f'CUDA available: {torch.cuda.is_available()}'); print(f'CUDA version: {torch.version.cuda}'); print(f'Device name: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"N/A\"}')"
```

Expected output:
```
PyTorch version: 2.7.0 (or later)
CUDA available: True
CUDA version: 12.4 (or later)
Device name: NVIDIA GeForce RTX 5090
```

---

### Option 2: Use Eager Attention (Fallback)

If you cannot upgrade PyTorch or Flash Attention fails to compile, you can disable Flash Attention and use eager attention mode.

#### Modify the Code

Edit `DeepSeek-OCR-master/DeepSeek-OCR-vllm/deepseek_ocr.py` and change the attention implementation:

```python
# In the __init__ method, add:
self.use_flash_attn = False  # Disable flash attention
```

Or use the transformers version instead of vLLM:

```bash
cd DeepSeek-OCR-master/DeepSeek-OCR-hf
python run_dpsk_ocr.py
```

And modify the model loading to use eager attention:

```python
model = AutoModel.from_pretrained(
    model_name, 
    _attn_implementation='eager',  # Changed from 'flash_attention_2'
    trust_remote_code=True, 
    use_safetensors=True
)
```

---

### Option 3: Use Docker with Pre-configured Environment

Use NVIDIA's PyTorch container with CUDA 12.4+ support:

```bash
docker pull nvcr.io/nvidia/pytorch:24.12-py3

docker run --gpus all -it --rm \
  -v $(pwd):/workspace \
  nvcr.io/nvidia/pytorch:24.12-py3 \
  bash

# Inside container:
cd /workspace
pip install -r requirements-rtx5090.txt
# Continue with installation
```

---

## Verification Steps

After installation, test the setup:

```bash
cd DeepSeek-OCR-master/DeepSeek-OCR-vllm

# Test with a sample image
python run_dpsk_ocr_image.py
```

If you see the model loading successfully without CUDA errors, the installation is complete.

---

## Troubleshooting

### Issue: Flash Attention still fails

**Solution**: Disable Flash Attention by modifying the attention implementation to use PyTorch's native SDPA (Scaled Dot-Product Attention):

```python
# In deepencoder/sam_vary_sdpa.py, the code already uses SDPA
# Ensure flash_attn import is wrapped in try-except
```

### Issue: vLLM not compatible with CUDA 12.4

**Solution**: Build vLLM from source or use the transformers version:

```bash
cd DeepSeek-OCR-master/DeepSeek-OCR-hf
python run_dpsk_ocr.py
```

### Issue: Out of memory errors

**Solution**: Reduce batch size or use smaller image sizes in `config.py`:

```python
BASE_SIZE = 640  # Reduced from 1024
IMAGE_SIZE = 512  # Reduced from 640
MAX_CROPS = 4     # Reduced from 6
```

---

## Performance Notes

- RTX 5090 has 32GB VRAM, which should handle the default configuration well
- For optimal performance, ensure you're using CUDA 12.4+ and PyTorch 2.7+
- Flash Attention provides ~2-3x speedup when properly compiled for sm_120

---

## Additional Resources

- [PyTorch Installation Guide](https://pytorch.org/get-started/locally/)
- [NVIDIA CUDA Toolkit](https://developer.nvidia.com/cuda-downloads)
- [vLLM Documentation](https://docs.vllm.ai/)
- [Flash Attention Repository](https://github.com/Dao-AILab/flash-attention)

---

## Summary

For RTX 5090 support, you **must** upgrade to:
- **CUDA 12.4+**
- **PyTorch 2.7+** (or nightly build)
- **vLLM 0.8.5+** compiled for CUDA 12.4
- **Flash Attention 2.7.3+** compiled for sm_120

The default environment (CUDA 11.8 + PyTorch 2.6.0) does not support the RTX 5090's sm_120 compute capability.
