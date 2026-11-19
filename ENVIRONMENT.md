# Computational Environment Specification

## System Requirements

- Python Version: Python 3.12 (compatible with Python >= 3.10)
- Operating System: Linux (Ubuntu 20.04+ / Debian 11+ / RHEL 8+), Windows 10/11, macOS 12+, or Windows Subsystem for Linux (WSL2).
- Architecture: x86_64 or Apple Silicon (arm64).
- RAM: Minimum 8 GB (16 GB recommended for raw strain STFT transforms in Paper VII).
- Disk Space: ~2 GB for runtime and verification output.

## Python Dependencies

The minimal dependencies required to reproduce all analyses and verification suites are:

```
numpy>=1.26.0
scipy>=1.12.0
pandas>=2.2.0
h5py>=3.10.0
```

## Installation Instructions

### Standard pip Installation

```bash
pip install -r requirements.txt
```

### Conda Environment Creation

```bash
conda create -n miscore python=3.12 -y
conda activate miscore
pip install -r requirements.txt
```

## Environment Verification

To verify that all dependencies and environment paths are correctly configured:

```bash
python -c "import numpy, scipy, pandas, h5py; print('All dependencies imported successfully.')"
```
