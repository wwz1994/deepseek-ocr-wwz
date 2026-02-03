# Solution for GitHub Issue #53: RTX 5090 Compatibility

## Problem Summary

Users with RTX 5090 GPUs encounter the following error when running DeepSeek-OCR with the default environment setup:

```
RuntimeError: CUDA error: no kernel image is available for execution on the device
CUDA kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.
```

**Root Cause:**
- RTX 5090 uses Blackwell architecture with CUDA compute capability **sm_120**
- Default environment (CUDA 11.8 + PyTorch 2.6.0) only supports up to **sm_90** (Hopper)
- PyTorch kernels are not compiled for sm_120, causing runtime errors

## Solution Overview

The RTX 5090 requires a newer software stack. Three solutions are provided:

### ✅ Solution 1: Upgrade Environment (RECOMMENDED)

**Requirements:**
- CUDA 12.4 or later
- PyTorch 2.7 or later (or nightly build)
- vLLM 0.8.5+ compiled for CUDA 12.4
- Flash Attention 2.7.3+ compiled for sm_120

**Installation Steps:**

```bash
# 1. Create new conda environment
conda create -n deepseek-ocr-rtx5090 python=3.12.9 -y
conda activate deepseek-ocr-rtx5090

# 2. Install PyTorch with CUDA 12.4 support (nightly recommended)
pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu124

# 3. Install vLLM (may need to build from source)
pip install vllm==0.8.5+cu124
# OR build from source:
# git clone https://github.com/vllm-project/vllm.git
# cd vllm && pip install -e . && cd ..

# 4. Install Flash Attention
pip install flash-attn==2.7.3 --no-build-isolation

# 5. Install other dependencies
pip install -r requirements-rtx5090.txt

# 6. Verify installation
python DeepSeek-OCR-master/DeepSeek-OCR-vllm/check_gpu_compatibility.py
```

**See `RTX5090_INSTALLATION_GUIDE.md` for detailed instructions.**

---

### 🔄 Solution 2: Use Eager Attention (Fallback)

If you cannot upgrade PyTorch, disable Flash Attention and use eager attention:

**For Transformers version:**

```bash
cd DeepSeek-OCR-master/DeepSeek-OCR-hf
```

Edit `run_dpsk_ocr.py` and change:

```python
model = AutoModel.from_pretrained(
    model_name, 
    _attn_implementation='eager',  # Changed from 'flash_attention_2'
    trust_remote_code=True, 
    use_safetensors=True
)
```

**Note:** This will be slower but should work with older PyTorch versions.

---

### 🐳 Solution 3: Use Docker

Use NVIDIA's official PyTorch container with CUDA 12.4+ support:

```bash
docker pull nvcr.io/nvidia/pytorch:24.12-py3

docker run --gpus all -it --rm \
  -v $(pwd):/workspace \
  nvcr.io/nvidia/pytorch:24.12-py3 \
  bash

# Inside container:
cd /workspace
pip install -r requirements-rtx5090.txt
# Continue with setup
```

---

## Files Created

1. **`requirements-rtx5090.txt`** - Updated requirements for RTX 5090
2. **`RTX5090_INSTALLATION_GUIDE.md`** - Comprehensive installation guide
3. **`check_gpu_compatibility.py`** - GPU compatibility checker script
4. **`deepencoder/sam_vary_sdpa_patched.py`** - Patched encoder with compatibility checks
5. **`ISSUE_53_SOLUTION.md`** - This file

## Quick Start for RTX 5090 Users

```bash
# 1. Check compatibility first
python DeepSeek-OCR-master/DeepSeek-OCR-vllm/check_gpu_compatibility.py

# 2. If incompatible, follow the upgrade guide
cat RTX5090_INSTALLATION_GUIDE.md

# 3. After upgrading, verify again
python DeepSeek-OCR-master/DeepSeek-OCR-vllm/check_gpu_compatibility.py

# 4. Run the model
cd DeepSeek-OCR-master/DeepSeek-OCR-vllm
python run_dpsk_ocr_image.py
```

## Technical Details

### Why This Happens

CUDA kernels in PyTorch are compiled for specific GPU architectures (compute capabilities). When PyTorch is compiled with CUDA 11.8, it includes kernels for:
- sm_50 (Maxwell)
- sm_60 (Pascal)
- sm_70 (Volta)
- sm_75 (Turing)
- sm_80 (Ampere)
- sm_86 (Ampere)
- sm_90 (Hopper)

The RTX 5090's sm_120 (Blackwell) is not in this list, causing the "no kernel image available" error.

### What Changed in PyTorch 2.7+

PyTorch 2.7+ with CUDA 12.4+ includes:
- Compiled kernels for sm_120 (Blackwell)
- Updated CUDA runtime libraries
- Support for new Blackwell-specific features

### Performance Impact

- **With Flash Attention (sm_120)**: ~2-3x faster attention computation
- **Without Flash Attention (eager)**: Slower but functional
- **RTX 5090 VRAM**: 32GB allows for larger batch sizes and higher resolution images

## Verification

After installation, you should see:

```bash
$ python check_gpu_compatibility.py
======================================================================
GPU Compatibility Check for DeepSeek-OCR
======================================================================
Device: NVIDIA GeForce RTX 5090
Compute Capability: sm_120
PyTorch Version: 2.7.0 (or later)
CUDA Version: 12.4 (or later)
Supported Architectures: [..., 'sm_120', ...]
======================================================================

Status: ✓ COMPATIBLE
Message: RTX 5090 is compatible with current environment

======================================================================
Flash Attention Check:
======================================================================
Flash Attention version: 2.7.3

======================================================================

✓ Your environment appears to be compatible with DeepSeek-OCR
```

## FAQ

**Q: Can I use CUDA 11.8 with RTX 5090?**
A: No, CUDA 11.8 does not support sm_120. You must upgrade to CUDA 12.4+.

**Q: Will this work with other Blackwell GPUs?**
A: Yes, all Blackwell architecture GPUs (sm_120) require the same upgrade.

**Q: Can I downgrade my GPU driver?**
A: No, the issue is with PyTorch/CUDA, not the driver. You need to upgrade the software stack.

**Q: Is there a performance difference?**
A: Yes, RTX 5090 with proper support will be significantly faster than older GPUs.

**Q: Can I use the HuggingFace transformers version instead?**
A: Yes, but you still need PyTorch 2.7+ with CUDA 12.4+ for RTX 5090 support.

## Support

For issues or questions:
1. Check `RTX5090_INSTALLATION_GUIDE.md` for detailed instructions
2. Run `check_gpu_compatibility.py` to diagnose issues
3. Report issues on GitHub with the output of the compatibility check

## References

- [PyTorch Installation Guide](https://pytorch.org/get-started/locally/)
- [NVIDIA CUDA Toolkit](https://developer.nvidia.com/cuda-downloads)
- [vLLM Documentation](https://docs.vllm.ai/)
- [Flash Attention Repository](https://github.com/Dao-AILab/flash-attention)
- [NVIDIA Blackwell Architecture](https://www.nvidia.com/en-us/data-center/technologies/blackwell-architecture/)
