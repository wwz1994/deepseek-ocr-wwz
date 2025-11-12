#!/bin/bash

# RTX 5090 Fix Script for DeepSeek-OCR
# This script helps users upgrade their environment for RTX 5090 compatibility

set -e

echo "========================================================================"
echo "RTX 5090 Compatibility Fix for DeepSeek-OCR"
echo "========================================================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if running in conda environment
if [ -z "$CONDA_DEFAULT_ENV" ]; then
    echo -e "${RED}Error: Not in a conda environment${NC}"
    echo "Please create and activate a conda environment first:"
    echo "  conda create -n deepseek-ocr-rtx5090 python=3.12.9 -y"
    echo "  conda activate deepseek-ocr-rtx5090"
    exit 1
fi

echo -e "${GREEN}✓ Conda environment detected: $CONDA_DEFAULT_ENV${NC}"
echo ""

# Check if CUDA is available
if ! command -v nvcc &> /dev/null; then
    echo -e "${YELLOW}Warning: nvcc not found. CUDA toolkit may not be installed.${NC}"
    echo "You may need to install CUDA 12.4+ manually."
    echo "Download from: https://developer.nvidia.com/cuda-downloads"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    CUDA_VERSION=$(nvcc --version | grep "release" | awk '{print $5}' | cut -d',' -f1)
    echo -e "${GREEN}✓ CUDA detected: $CUDA_VERSION${NC}"
    
    # Check CUDA version
    CUDA_MAJOR=$(echo $CUDA_VERSION | cut -d'.' -f1)
    CUDA_MINOR=$(echo $CUDA_VERSION | cut -d'.' -f2)
    
    if [ "$CUDA_MAJOR" -lt 12 ] || ([ "$CUDA_MAJOR" -eq 12 ] && [ "$CUDA_MINOR" -lt 4 ]); then
        echo -e "${YELLOW}Warning: CUDA $CUDA_VERSION detected. RTX 5090 requires CUDA 12.4+${NC}"
        echo "Please upgrade CUDA toolkit from: https://developer.nvidia.com/cuda-downloads"
        echo ""
        read -p "Continue anyway? (y/n) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
fi

echo ""
echo "========================================================================"
echo "Step 1: Uninstalling old PyTorch..."
echo "========================================================================"
pip uninstall -y torch torchvision torchaudio 2>/dev/null || true

echo ""
echo "========================================================================"
echo "Step 2: Installing PyTorch with CUDA 12.4 support..."
echo "========================================================================"
echo "This will install PyTorch nightly build with CUDA 12.4 support."
echo ""

pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu124

echo ""
echo "========================================================================"
echo "Step 3: Checking PyTorch installation..."
echo "========================================================================"

python -c "import torch; print(f'PyTorch version: {torch.__version__}'); print(f'CUDA available: {torch.cuda.is_available()}'); print(f'CUDA version: {torch.version.cuda}')"

echo ""
echo "========================================================================"
echo "Step 4: Installing vLLM..."
echo "========================================================================"
echo "Attempting to install vLLM..."
echo ""

# Try to install vLLM
if pip install vllm==0.8.5 2>/dev/null; then
    echo -e "${GREEN}✓ vLLM installed successfully${NC}"
else
    echo -e "${YELLOW}Warning: Pre-built vLLM not available. You may need to build from source.${NC}"
    echo "To build from source:"
    echo "  git clone https://github.com/vllm-project/vllm.git"
    echo "  cd vllm"
    echo "  pip install -e ."
    echo ""
    read -p "Continue without vLLM? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo ""
echo "========================================================================"
echo "Step 5: Installing Flash Attention..."
echo "========================================================================"
echo "This may take several minutes to compile..."
echo ""

if pip install flash-attn==2.7.3 --no-build-isolation; then
    echo -e "${GREEN}✓ Flash Attention installed successfully${NC}"
else
    echo -e "${YELLOW}Warning: Flash Attention installation failed.${NC}"
    echo "The model will fall back to eager attention (slower but functional)."
    echo ""
fi

echo ""
echo "========================================================================"
echo "Step 6: Installing other dependencies..."
echo "========================================================================"

if [ -f "requirements-rtx5090.txt" ]; then
    pip install -r requirements-rtx5090.txt
elif [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo "Installing basic dependencies..."
    pip install transformers==4.46.3 tokenizers==0.20.3 PyMuPDF img2pdf einops easydict addict Pillow numpy
fi

echo ""
echo "========================================================================"
echo "Step 7: Running compatibility check..."
echo "========================================================================"

if [ -f "DeepSeek-OCR-master/DeepSeek-OCR-vllm/check_gpu_compatibility.py" ]; then
    python DeepSeek-OCR-master/DeepSeek-OCR-vllm/check_gpu_compatibility.py
else
    echo -e "${YELLOW}Compatibility checker not found. Skipping...${NC}"
fi

echo ""
echo "========================================================================"
echo "Installation Complete!"
echo "========================================================================"
echo ""
echo -e "${GREEN}✓ Environment setup complete for RTX 5090${NC}"
echo ""
echo "Next steps:"
echo "1. Verify your GPU is detected:"
echo "   python -c \"import torch; print(torch.cuda.get_device_name(0))\""
echo ""
echo "2. Run the model:"
echo "   cd DeepSeek-OCR-master/DeepSeek-OCR-vllm"
echo "   python run_dpsk_ocr_image.py"
echo ""
echo "For more information, see:"
echo "  - RTX5090_INSTALLATION_GUIDE.md"
echo "  - ISSUE_53_SOLUTION.md"
echo ""
echo "========================================================================"
