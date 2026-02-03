"""
GPU Compatibility Checker for DeepSeek-OCR
Checks if the current GPU and PyTorch installation are compatible
"""

import torch
import sys
import warnings


def get_compute_capability():
    """Get the CUDA compute capability of the current GPU"""
    if not torch.cuda.is_available():
        return None
    
    device = torch.cuda.current_device()
    capability = torch.cuda.get_device_capability(device)
    return capability


def get_supported_architectures():
    """Get the list of CUDA architectures supported by current PyTorch"""
    if not torch.cuda.is_available():
        return []
    
    # Get the CUDA architectures that PyTorch was compiled with
    # This is stored in torch.cuda.get_arch_list()
    try:
        arch_list = torch.cuda.get_arch_list()
        return arch_list
    except:
        return []


def check_compatibility():
    """
    Check if the current GPU is compatible with the installed PyTorch version
    
    Returns:
        tuple: (is_compatible, warning_message, recommendation)
    """
    if not torch.cuda.is_available():
        return False, "CUDA is not available", "Install CUDA and PyTorch with CUDA support"
    
    device_name = torch.cuda.get_device_name(0)
    compute_capability = get_compute_capability()
    pytorch_version = torch.__version__
    cuda_version = torch.version.cuda
    
    print("=" * 70)
    print("GPU Compatibility Check for DeepSeek-OCR")
    print("=" * 70)
    print(f"Device: {device_name}")
    print(f"Compute Capability: sm_{compute_capability[0]}{compute_capability[1]}")
    print(f"PyTorch Version: {pytorch_version}")
    print(f"CUDA Version: {cuda_version}")
    print(f"Supported Architectures: {get_supported_architectures()}")
    print("=" * 70)
    
    # Check for RTX 5090 (Blackwell - sm_120)
    if compute_capability[0] == 12 and compute_capability[1] == 0:
        # RTX 5090 detected
        if cuda_version and cuda_version.startswith('11'):
            return False, \
                   "RTX 5090 (sm_120) detected but PyTorch is compiled with CUDA 11.x", \
                   """
RTX 5090 requires CUDA 12.4+ and PyTorch 2.7+

Please upgrade your environment:
1. Install CUDA 12.4 or later
2. Install PyTorch 2.7+ with CUDA 12.4:
   pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu124

See RTX5090_INSTALLATION_GUIDE.md for detailed instructions.
"""
        elif cuda_version and float(cuda_version.split('.')[0]) >= 12:
            # Check PyTorch version
            pytorch_major_minor = '.'.join(pytorch_version.split('.')[:2])
            if float(pytorch_major_minor) < 2.7:
                return False, \
                       f"RTX 5090 requires PyTorch 2.7+, but {pytorch_version} is installed", \
                       """
Please upgrade PyTorch to 2.7 or later:
   pip install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu124

See RTX5090_INSTALLATION_GUIDE.md for detailed instructions.
"""
            else:
                return True, "RTX 5090 is compatible with current environment", ""
    
    # Check for other newer GPUs (Hopper - sm_90)
    elif compute_capability[0] == 9 and compute_capability[1] == 0:
        if cuda_version and cuda_version.startswith('11'):
            warnings.warn("Hopper GPU detected with CUDA 11.x. Consider upgrading to CUDA 12.x for better performance.")
    
    # Check for Ampere and older (should work with CUDA 11.8)
    elif compute_capability[0] <= 8:
        return True, f"{device_name} is compatible with current environment", ""
    
    # Unknown future architecture
    else:
        return False, \
               f"Unknown GPU architecture: sm_{compute_capability[0]}{compute_capability[1]}", \
               "This GPU may require a newer version of PyTorch and CUDA"
    
    return True, "GPU appears to be compatible", ""


def check_flash_attention():
    """Check if Flash Attention is available and working"""
    try:
        import flash_attn
        print(f"Flash Attention version: {flash_attn.__version__}")
        return True
    except ImportError:
        print("Flash Attention is not installed")
        return False
    except Exception as e:
        print(f"Flash Attention error: {e}")
        return False


def main():
    """Main function to run compatibility checks"""
    is_compatible, message, recommendation = check_compatibility()
    
    print(f"\nStatus: {'✓ COMPATIBLE' if is_compatible else '✗ INCOMPATIBLE'}")
    print(f"Message: {message}")
    
    if recommendation:
        print(f"\nRecommendation:")
        print(recommendation)
    
    print("\n" + "=" * 70)
    print("Flash Attention Check:")
    print("=" * 70)
    flash_available = check_flash_attention()
    
    if not flash_available:
        print("\nNote: Flash Attention is not available. The model will use eager attention.")
        print("This may result in slower inference but should still work.")
    
    print("\n" + "=" * 70)
    
    if not is_compatible:
        print("\n⚠️  WARNING: Your GPU may not work with the current environment!")
        print("Please follow the recommendations above before running the model.")
        sys.exit(1)
    else:
        print("\n✓ Your environment appears to be compatible with DeepSeek-OCR")
        sys.exit(0)


if __name__ == "__main__":
    main()
