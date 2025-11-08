#!/bin/bash
# Thesis Prototype - Quick Start Script
# Optimized startup for Linux/Mac

echo "============================================================"
echo "Thesis Prototype - Human Activity Recognition System"
echo "============================================================"
echo ""

# Check if conda environment exists
if ! conda env list | grep -q "env"; then
    echo "[ERROR] Conda environment 'env' not found!"
    echo ""
    echo "Please create the environment first:"
    echo "  conda create -n env python=3.10"
    echo "  conda activate env"
    echo "  pip install -r requirements.txt"
    echo ""
    exit 1
fi

# Activate environment
echo "[1/3] Activating conda environment..."
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate env
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to activate environment"
    exit 1
fi

# Check GPU
echo ""
echo "[2/3] Checking GPU availability..."
python -c "import torch; print(f'GPU Available: {torch.cuda.is_available()}'); print(f'GPU Name: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"N/A\"}')" 2>/dev/null || echo "[WARNING] PyTorch not installed or GPU check failed"

# Start server
echo ""
echo "[3/3] Starting server..."
echo "============================================================"
echo ""
python start_server.py
