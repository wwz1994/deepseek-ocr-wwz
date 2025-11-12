@echo off
REM RTX 5090 Fix Script for DeepSeek-OCR (Windows)
REM This script helps users upgrade their environment for RTX 5090 compatibility

echo ========================================================================
echo RTX 5090 Compatibility Fix for DeepSeek-OCR
echo ========================================================================
echo.

REM Check if running in conda environment
if "%CONDA_DEFAULT_ENV%"=="" (
    echo Error: Not in a conda environment
    echo Please create and activate a conda environment first:
    echo   conda create -n deepseek-ocr-rtx5090 python=3.12.9 -y
    echo   conda activate deepseek-ocr-rtx5090
    pause
    exit /b 1
)

echo [OK] Conda environment detected: %CONDA_DEFAULT_ENV%
echo.

REM Check if CUDA is available
where nvcc >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Warning: nvcc not found. CUDA toolkit may not be installed.
    echo You may need to install CUDA 12.4+ manually.
    echo Download from: https://developer.nvidia.com/cuda-downloads
    echo.
    set /p CONTINUE="Continue anyway? (y/n): "
    if /i not "%CONTINUE%"=="y" exit /b 1
) else (
    echo [OK] CUDA toolkit detected
)

echo.
echo ========================================================================
echo Step 1: Uninstalling old PyTorch...
echo ========================================================================
pip uninstall -y torch torchvision torchaudio 2>nul

echo.
echo ========================================================================
echo Step 2: Installing PyTorch with CUDA 12.4 support...
echo ========================================================================
echo This will install PyTorch nightly build with CUDA 12.4 support.
echo.

pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu124

echo.
echo ========================================================================
echo Step 3: Checking PyTorch installation...
echo ========================================================================

python -c "import torch; print(f'PyTorch version: {torch.__version__}'); print(f'CUDA available: {torch.cuda.is_available()}'); print(f'CUDA version: {torch.version.cuda}')"

echo.
echo ========================================================================
echo Step 4: Installing vLLM...
echo ========================================================================
echo Attempting to install vLLM...
echo.

pip install vllm==0.8.5
if %ERRORLEVEL% NEQ 0 (
    echo Warning: Pre-built vLLM not available. You may need to build from source.
    echo To build from source:
    echo   git clone https://github.com/vllm-project/vllm.git
    echo   cd vllm
    echo   pip install -e .
    echo.
    set /p CONTINUE="Continue without vLLM? (y/n): "
    if /i not "%CONTINUE%"=="y" exit /b 1
)

echo.
echo ========================================================================
echo Step 5: Installing Flash Attention...
echo ========================================================================
echo This may take several minutes to compile...
echo.

pip install flash-attn==2.7.3 --no-build-isolation
if %ERRORLEVEL% NEQ 0 (
    echo Warning: Flash Attention installation failed.
    echo The model will fall back to eager attention (slower but functional).
    echo.
)

echo.
echo ========================================================================
echo Step 6: Installing other dependencies...
echo ========================================================================

if exist requirements-rtx5090.txt (
    pip install -r requirements-rtx5090.txt
) else if exist requirements.txt (
    pip install -r requirements.txt
) else (
    echo Installing basic dependencies...
    pip install transformers==4.46.3 tokenizers==0.20.3 PyMuPDF img2pdf einops easydict addict Pillow numpy
)

echo.
echo ========================================================================
echo Step 7: Running compatibility check...
echo ========================================================================

if exist DeepSeek-OCR-master\DeepSeek-OCR-vllm\check_gpu_compatibility.py (
    python DeepSeek-OCR-master\DeepSeek-OCR-vllm\check_gpu_compatibility.py
) else (
    echo Compatibility checker not found. Skipping...
)

echo.
echo ========================================================================
echo Installation Complete!
echo ========================================================================
echo.
echo [OK] Environment setup complete for RTX 5090
echo.
echo Next steps:
echo 1. Verify your GPU is detected:
echo    python -c "import torch; print(torch.cuda.get_device_name(0))"
echo.
echo 2. Run the model:
echo    cd DeepSeek-OCR-master\DeepSeek-OCR-vllm
echo    python run_dpsk_ocr_image.py
echo.
echo For more information, see:
echo   - RTX5090_INSTALLATION_GUIDE.md
echo   - ISSUE_53_SOLUTION.md
echo.
echo ========================================================================

pause
