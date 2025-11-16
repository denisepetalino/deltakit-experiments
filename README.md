# deltakit-experiments

Stim / PyMatching / Cirq experiments for simple QEC demos:
- Repetition code (bit-flip, phase-flip)
- Shor (encode + first syndrome)
- Surface code d=3 (Stim DEM → PyMatching)

## Prerequisites
- Python 3.11+
- This repo has GitHub Actions CI that runs `pytest`.

## Quickstart

### 1) Create a virtual environment
**macOS/Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
