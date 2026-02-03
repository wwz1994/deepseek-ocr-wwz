# RTX 5090 Support Addendum

## ⚠️ Important Notice for RTX 5090 Users

If you have an **NVIDIA RTX 5090** (or other Blackwell architecture GPUs), the default installation instructions will **NOT work**. You will encounter this error:

```
RuntimeError: CUDA error: no kernel image is available for execution on the device
```

### Why This Happens

The RTX 5090 uses the new Blackwell architecture with CUDA compute capability **sm_120**, which is not supported by the default environment (CUDA 11.8 + PyTorch 2.6.0).

### Quick Fix

**Option 1: Automated Script (Recommended)**

```bash
# Linux/Mac
bash fix_rtx5090.sh

# Windows
fix_rtx5090.bat
```

**Option 2: Manual Installation**

```bash
# 1. Create new environment
conda create -n deepseek-ocr-rtx5090 python=3.12.9 -y
conda activate deepseek-ocr-rtx5090

# 2. Install PyTorch with CUDA 12.4
pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu124

# 3. Install dependencies
pip install -r requirements-rtx5090.txt

# 4. Install vLLM and Flash Attention
pip install vllm==0.8.5
pip install flash-attn==2.7.3 --no-build-isolation

# 5. Verify installation
python DeepSeek-OCR-master/DeepSeek-OCR-vllm/check_gpu_compatibility.py
```

### Required Versions for RTX 5090

| Component | Minimum Version | Recommended |
|-----------|----------------|-------------|
| CUDA | 12.4 | 12.6+ |
| PyTorch | 2.7.0 | Nightly build |
| vLLM | 0.8.5 | Latest |
| Flash Attention | 2.7.3 | Latest |

### Documentation

For detailed instructions, see:
- **[RTX5090_INSTALLATION_GUIDE.md](RTX5090_INSTALLATION_GUIDE.md)** - Complete installation guide
- **[ISSUE_53_SOLUTION.md](ISSUE_53_SOLUTION.md)** - Technical details and solutions
- **[check_gpu_compatibility.py](DeepSeek-OCR-master/DeepSeek-OCR-vllm/check_gpu_compatibility.py)** - Compatibility checker

### Compatibility Check

Before running the model, check your environment:

```bash
python DeepSeek-OCR-master/DeepSeek-OCR-vllm/check_gpu_compatibility.py
```

Expected output for RTX 5090:
```
Device: NVIDIA GeForce RTX 5090
Compute Capability: sm_120
PyTorch Version: 2.7.0+
CUDA Version: 12.4+
Status: ✓ COMPATIBLE
```

### Alternative: Use Transformers Version

If you cannot upgrade PyTorch, use the Transformers version with eager attention:

```bash
cd DeepSeek-OCR-master/DeepSeek-OCR-hf
# Edit run_dpsk_ocr.py to use _attn_implementation='eager'
python run_dpsk_ocr.py
```

### Support

For issues specific to RTX 5090:
1. Run the compatibility checker
2. Check the installation guide
3. Report issues with the checker output

---

## Original Installation Instructions

> **Note:** The instructions below are for GPUs with compute capability sm_90 or lower (RTX 4090, A100, H100, etc.). RTX 5090 users must follow the instructions above.

[Original README content continues here...]
