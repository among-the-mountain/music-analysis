#!/bin/bash
# Music Analysis System - Linux/macOS Startup Script
# 音乐分析系统 - Linux/macOS 启动脚本

echo "========================================"
echo "Music Analysis System"
echo "音乐分析系统"
echo "========================================"
echo ""

# Check if conda is available
if ! command -v conda &> /dev/null; then
    echo "ERROR: Conda is not installed or not in PATH"
    echo "错误: Conda 未安装或不在 PATH 中"
    echo "Please install Anaconda or Miniconda first"
    echo "请先安装 Anaconda 或 Miniconda"
    exit 1
fi

# Activate conda environment
echo "Activating conda environment..."
echo "激活 conda 环境..."
eval "$(conda shell.bash hook)"
conda activate music-analysis

if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: Failed to activate conda environment"
    echo "错误: 无法激活 conda 环境"
    echo ""
    echo "Please create the environment first:"
    echo "请先创建环境:"
    echo "conda env create -f environment.yml"
    echo ""
    exit 1
fi

echo ""
echo "Starting Flask application..."
echo "启动 Flask 应用..."
echo ""
echo "The application will be available at:"
echo "应用程序将在以下地址可用:"
echo "http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo "按 Ctrl+C 停止服务器"
echo ""

# Start the Flask application
python app.py
