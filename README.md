# HoloGram-Hardware_Circuit
Hardware, circuit-ai, pose-estimation, holography, QSPICE, EdgeAI

# HoloGram_Circuit_ZeroShot

This repository provides the complete framework for validating the HoloGram hardware circuit, including:

- Real-time depth and pose estimation
- Zero-shot error detection
- QSPICE circuit-level simulation
- WebDom timing diagram generation

## Folder Structure

- `models/`: Contains the main circuit simulation models.
- `datasets/`: Real-time input datasets for testing.
- `train_model.py`: Training pipeline for voltage-mapped holographic circuit.
- `test_model.py`: Testing framework with pose and depth voltages.
- `infer.py`: Inference module for zero-shot error.
- `zero_shot_error_simulation.py`: Simulates error detection in fusion stage.
- `fusion_logic_qspice.sch`: Circuit-level fusion using logic gates.
- `timing_webdom.json`: Timing diagram code for WebDom simulator.

## Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

## Running Simulation

```bash
python train_model.py
python test_model.py
python zero_shot_error_simulation.py
```

## Output

All output graphs (JPEG) are stored in `/output` folder, including:
- Pose and Depth Voltage Curves
- Zero-shot Error Simulation
- WebDom Timing Diagram

---

**Note**: Ensure QSPICE and WebDom are pre-installed for circuit validation and waveform generation.
