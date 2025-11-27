# deltakit-experiments

Stim / PyMatching / Cirq experiments for simple QEC demos:
- Repetition code (bit-flip, phase-flip)
- Shor (encode + first syndrome)
- Surface code d=3 (Stim DEM → PyMatching)

## Prerequisites
- Python 3.11+
- This repo has GitHub Actions CI that runs `pytest`.

# Bit-Flip Repetition Code (Cirq + StimSampler)

This project implements the **bit-flip quantum repetition code** exactly following  
Riverlane’s Deltakit Textbook (Chapter: *Building the bit-flip quantum repetition code from scratch*).

Textbook reference:  
https://textbook.riverlane.com/en/latest/notebooks/ch2-classical-to-quantum-repcodes/bit-flip-repetition-codes.html

## What this script demonstrates

### 1. Quantum state encoding
We implement the textbook 3-qubit repetition code encoder, which spreads the logical qubit across multiple physical qubits using CNOT operations.

### 2. Stabiliser-based error detection
We implement Z⊗Z stabiliser checks by:
- entangling adjacent data qubits with designated syndrome qubits,
- measuring the syndrome qubits to extract the error pattern.

### 3. Simulated noise
Noise is applied using Cirq’s built-in `with_probability()` method, following the textbook’s demonstration of independent Pauli X-errors.

### 4. Syndrome extraction
Syndromes are captured by measuring the stabiliser ancilla qubits and inspected via:

```
result.measurements['syndrome']
```

### 5. Simulation using StimSampler
The repetition code circuit is executed using `stimcirq.StimSampler()`, which offers efficient stabiliser simulation.

## File Overview

- `repetition_bitflip.py`  
  Implements the encoder, stabiliser measurement, noise model, full circuit assembly, and syndrome extraction exactly as in the textbook.

## Quickstart

### 1) Create a virtual environment
**macOS/Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
