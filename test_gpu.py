#!/usr/bin/env python3
"""
Test script to verify GPU detection and usage
"""
import torch
import os
import sys

def test_gpu_setup():
    """Test GPU setup similar to the application"""
    print("=" * 50)
    print("GPU Detection Test")
    print("=" * 50)
    
    # Basic PyTorch info
    print(f"PyTorch version: {torch.__version__}")
    print(f"CUDA available: {torch.cuda.is_available()}")
    
    if torch.cuda.is_available():
        print(f"CUDA version: {torch.version.cuda}")
        print(f"Device count: {torch.cuda.device_count()}")
        print(f"Current device: {torch.cuda.current_device()}")
        print(f"Device name: {torch.cuda.get_device_name(0)}")
        
        # Memory info
        props = torch.cuda.get_device_properties(0)
        print(f"Total memory: {props.total_memory / 1024**3:.1f} GB")
        print(f"Multiprocessor count: {props.multi_processor_count}")
        
        # Test tensor operations
        print("\nTesting tensor operations...")
        try:
            device = torch.device("cuda:0")
            test_tensor = torch.randn(1000, 1000, device=device)
            result = torch.mm(test_tensor, test_tensor.t())
            print("✓ GPU tensor operations successful")
            print(f"✓ Tensor device: {result.device}")
            
            # Clean up
            del test_tensor, result
            torch.cuda.empty_cache()
            
        except Exception as e:
            print(f"✗ GPU tensor operations failed: {e}")
            return False
            
    else:
        print("CUDA is not available. Possible reasons:")
        print("- PyTorch was installed without CUDA support")
        print("- NVIDIA GPU drivers are not installed")
        print("- CUDA toolkit is not installed")
        return False
    
    return True

def test_device_selection():
    """Test the device selection logic from the application"""
    print("\n" + "=" * 50)
    print("Device Selection Test")
    print("=" * 50)
    
    def _setup_device():
        """Enhanced device setup with better GPU detection"""
        try:
            if torch.cuda.is_available():
                device_count = torch.cuda.device_count()
                print(f"CUDA is available. Found {device_count} GPU(s)")
                
                try:
                    device = torch.device("cuda:0")
                    # Test GPU by creating a small tensor
                    test_tensor = torch.randn(1, device=device)
                    print(f"Successfully initialized GPU: {torch.cuda.get_device_name(0)}")
                    del test_tensor
                    torch.cuda.empty_cache()
                    return device
                except Exception as gpu_error:
                    print(f"GPU initialization failed: {gpu_error}")
                    print("Falling back to CPU")
                    
            else:
                print("CUDA is not available")
                
        except Exception as e:
            print(f"Error during device setup: {e}")
            
        print("Using CPU device")
        return torch.device("cpu")
    
    device = _setup_device()
    print(f"Selected device: {device}")
    return device.type == "cuda"

if __name__ == "__main__":
    print("Testing GPU setup for thesis application...")
    
    # Test basic GPU detection
    gpu_available = test_gpu_setup()
    
    # Test device selection logic
    gpu_selected = test_device_selection()
    
    print("\n" + "=" * 50)
    print("Summary")
    print("=" * 50)
    
    if gpu_available and gpu_selected:
        print("✓ GPU is properly detected and configured")
        print("✓ The application should use GPU acceleration")
    elif gpu_available and not gpu_selected:
        print("⚠ GPU is available but not being selected")
        print("⚠ Check device selection logic in the application")
    else:
        print("✗ GPU is not available")
        print("✗ The application will use CPU (slower performance)")
    
    print("\nTo run the application with GPU support:")
    print("python app.py")