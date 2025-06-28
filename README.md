# HoloGram-Hardware_Circuit
Hardware, circuit-ai, pose-estimation, holography, QSPICE, EdgeAI

 ## User Validation Guide for HoloGram_Circuit_Model
1. Prerequisites
Make sure your system includes:

Unix-based OS (Ubuntu 20.04+ / macOS)

Python 3.8+

Git

pip

QSPICE Simulator (Windows users may need Wine for compatibility)

WaveDrom (for browser-based timing diagrams)

A code editor (e.g., VSCode)

## Clone the Repository
2. git clone https://github.com/your-org/HoloGram-Circuit_Model.git
cd HoloGram-Circuit_Model

##Create a Virtual Environment
3. perform the steps if required 
python3 -m venv venv
source venv/bin/activate

## Install Dependencies
4. Do the step and check properly against the list 

pip install -r requirements (1).txt

Typical dependencies include:

text
Copy
Edit
numpy
opencv-python
matplotlib
torch
scikit-learn
waveform-analysis

## Check and validate 
5. Now Condider the project structure and run the files accordinly or validate the same
   Understand Project Structure
bash
Copy
Edit
HoloGram_Circuit_Model/
├── model/
│   ├── train_model.py          # Train depth and pose estimators
│   ├── test_model.py           # Evaluate model accuracy
│   ├── infer.py                # Inference pipeline to generate voltages
│   └── hologram_circuit_model.py
│
├── simulation/
│   ├── zero_shot_error_simulation.py  # Plots depth, pose, and error curves
│   ├── fusion_logic_qspice.sch        # QSPICE circuit file
│   └── fusion_timing_webdom.json

## Training the Model

Run the command
6. python model/test_model.py

## Get the output of the Model
7. It generates output like 
It outputs:
Pose Accuracy (PCK%)
Depth Accuracy (SSIM)
Saves .npy voltage output files used in circuit simulation

## Inference to Generate Simulation Voltages and run the files 

8. Run and validate the files properly 
python model/infer.py --input data/test_dataset/image1.jpg
Produces:

pose_voltage.npy

depth_voltage.npy

zero_shot_error.npy

## Visualize Zero-Shot Error 

9. run the command

 python simulation/zero_shot_error_simulation.py   

 Generates Output as like the figure 6:
Pose Voltage (Green)
Depth Voltage (Blue)
Zero-Shot Error (Red)

## Circuit Validation in QSPICE Simulator 

10. Perform following Action
Open QSPICE software (Windows or via Wine)

Load simulation/fusion_logic_qspice.sch

Inject voltages using exported .npy waveform data

Simulate and validate timing alignment

Verify fused output matches real-time frame sync

## Timing Diagram in WebDom Simulator to validate the functionality of the cuircuit 

11. Perform the following activities to get the timing diagram of the circuit
    Open https://wavedrom.com/editor.html

Paste content from simulation/fusion_timing_webdom.json
Validate:
MiDaS and BlazePose clocked inputs
Latch outputs
Frame sync logic
Run the .JSON file - hologram_timing_webdom additionally

