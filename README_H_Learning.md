# H-Learning: depth–pose interaction and finite-state control

A runnable reference implementation prepared from the supplied **6 October 2026 H-Learning manuscript**. It provides actual MiDaS and BlazePose/GHUM inference, a synchronized common controller, abnormal-motion monitoring (`M=0`), interactive learning (`M=1`), live data collection, recorded-data validation and a compact hardware-control reference.

This repository is a new implementation of the described scheme. It is not a recovery of the authors' unpublished source code. Choices absent from the manuscript—gesture definitions, confirmation times, lesson content and motion thresholds—are explicit, configurable implementation choices.

**Start with the tested Python implementation.** MATLAB/Stateflow and QSPICE files are supplementary models with the execution status stated below. A simulator-like picture is not used as evidence.

## Included capabilities

| Component | Implementation |
|---|---|
| Single RGB source | Webcam, video, or official UR Fall PNG sequence |
| Monocular depth | Actual MiDaS v2.1 small ONNX inference through OpenCV DNN on CPU |
| Skeletal pose | Actual MediaPipe Pose Landmarker lite, a BlazePose/GHUM variant, with 33 landmarks |
| Synchronization | Same-image processing; frame IDs, source times, confidence and maximum skew checked |
| Stabilization | Bounded depth EMA and visible-pose smoothing; no optical-flow compensation claimed |
| Fusion representation | Pose coordinates and sampled relative inverse depth at each joint, kept in their respective units |
| Common control | Idle, DepthReady, PoseReady, FusionReady, OutputStable |
| Monitoring control | Neutral, Walk, Bend, Fall, Suspicious, Alert |
| Learning control | Eight states from detection to assessment, feedback/remediation and completion |
| Interaction | Selection, rotation, zoom, next/previous lesson, answer submission, cancellation and reset |
| Timing safeguards | Gesture hold confirmation, one commit per held gesture, frame-gap rejection and reacquisition |
| Data collection | Signals, state trace, raw model landmarks, timing, configuration and model checksums; optional frames/depth |
| Validation | Real recorded UR Fall features/timestamps, neural-clip runs, fault injection and independent-annotation utilities |
| Hardware reference | Synthesizable eight-state SystemVerilog control core, testbench and ZCU104 synthesis Tcl |
| Simulator interfaces | Actual Stateflow model builder, PWL voltage-interface model and WaveDrom timing export |

An AND combines **validity flags**, not numerical depth and pose arrays. Neural models run in software; op-amps do not implement MiDaS or BlazePose in this release. The three software FSMs have separate state registers. A single three-bit register does not encode all their joint combinations.

## 1. Installation and immediate offline controller validation

Use Python 3.10 or newer. Python 3.12 was used for the included execution evidence. Run commands from this repository's root.

```bash
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -e .
python -m unittest discover -s tests -v
h-learning demo --out runs/demo
```

The core controller uses only Python's standard library. The optional metric tests skip when NumPy/SciPy are absent. The demo deliberately generates **synthetic regression vectors**; it contains no measured human observations or neural predictions.

If installation is unavailable, the core can run directly on Linux/macOS:

```bash
PYTHONPATH=src python -m h_learning demo --out runs/demo
```

## 2. Install actual vision inference

```bash
python -m pip install -e ".[vision,plots,metrics]"
python scripts/download_models.py
```

`models/checksums.json` pins the exact downloaded model bytes used for the supplied runs. `requirements-vision-tested.txt` records the tested Python 3.12 dependency versions; the flexible extras in `pyproject.toml` support other compatible installations.

On Linux, MediaPipe also needs EGL/GLES shared libraries. If the loader reports `libGLESv2.so.2` missing, install the operating system's `libgles2` package; Debian/Ubuntu installations normally also have `libegl1`. A display server is required for the interactive window, but `--headless` inference works without a window. Use the OpenCV contrib package required by MediaPipe and avoid installing conflicting OpenCV wheels in the same environment.

Weights are downloaded from their official providers and are not committed to Git. See [THIRD_PARTY.md](THIRD_PARTY.md) for origins and applicable terms.

## 3. Collect your own real-time validation dataset

Start the learning application with a connected webcam:

```bash
h-learning run --camera 0 --mode 1 --input gesture \
  --participant-id P001 --save-views --record-frames --out runs/P001_gesture
```

Run the comparison condition with a **new session directory**:

```bash
h-learning run --camera 0 --mode 1 --input keyboard \
  --participant-id P001 --save-views --out runs/P001_keyboard
```

For monitoring:

```bash
h-learning run --camera 0 --mode 0 --save-views --out runs/live_monitoring
```

For a noninteractive capture add `--headless --max-frames 300`. A camera must be physically available; this delivery environment was not used to capture new participants. Recorded runs are supplied separately and identified as recorded data.

### Keyboard and mouse controls

| Input | Command |
|---|---|
| `s` | Select the next object |
| `a` / `d` | Rotate left / right, 15 degrees per accepted command |
| `+` / `-` | Enlarge / reduce, bounded to 0.4–2.5 times |
| `n` / `p` | Next / previous lesson; `n` also acknowledges feedback |
| `1` / `2` / `3` | Submit answer A / B / C |
| `x` | Cancel pending interaction and release selection |
| `r` | Reset the controllers |
| `t` | Switch mode, clearing application state and requiring reacquisition |
| `q` | End and finalize the session |
| Left click in `--input mouse` | Select |
| Right click | Cancel |

Keyboard answer submission is available in gesture sessions. This implementation uses body gestures rather than finger-level gesture recognition:

| Body configuration, held for at least 200 ms | Command |
|---|---|
| Left wrist above the nose | Select |
| Right wrist above the nose | Next |
| Both wrists above the nose | Cancel, with immediate priority |
| Both wrists near shoulder height and widely separated | Zoom in |
| Both wrists near shoulder height and close together | Zoom out |
| One arm extended sideways at shoulder height | Rotate in that direction |
| Both wrists below the hips and widely separated | Previous |

Definitions and precedence are in `vision.py`. Neutral posture re-arms a held gesture. Rotation/zoom require an already selected object. Unstable or mismatched tracking suppresses commands and clears pending confirmation. Educational state is retained through tracking loss; control resumes after reacquisition. Mode changes clear both application histories.

The software view renders three simple polyhedra with lesson questions. It is a 3D interaction demonstration on a 2D screen; this repository does not establish optical hologram reconstruction or a manufactured display.

Actual Python execution view from the recorded `adl-01` example, with upstream
data attribution in `data/DATA_LICENSE.md`:

![Python execution on recorded UR Fall ADL data](validation_runs/recorded_adl_01_learning/views/000150.jpg)

### Session files

| File | Evidence |
|---|---|
| `metadata.json` | Source, software versions, model hashes, configuration, timing definitions and completion status |
| `signals.csv` | Per-frame inputs, source timestamp and measured processing durations |
| `trace.csv` | Inputs plus all FSM states, enables, commands, feedback and invariant-relevant outputs |
| `pose.jsonl` | Model image/world landmarks, smoothed landmarks and joint relative inverse depths |
| `report.json` | Timing distributions, gate availability, commands and invariant violations |
| `views/*.jpg` | Views rendered during actual Python execution, when requested |
| `frames/*.jpg`, `depth/*.npz` | Optional recorded images and numerical model depth outputs |

Directories must be empty at session start. Interrupted sessions retain their partial logs and failure status. Use consented, pseudonymous participant recordings for the learning study; keep those sessions out of the public Git repository.

## 4. Genuine recorded validation data

The accompanying **H_Learning_Recorded_Validation_Data.zip** contains official UR Fall data. Extract it **inside this repository** so it populates `data/urfall/` and `data/processed/`. It includes:

- The two unchanged original depth-feature CSVs: **11,544 observations across 70 sequences**.
- All 70 synchronization files with recorded camera-0 timestamps.
- Complete `fall-01` and `adl-01` camera-0 RGB and depth PNG archives, plus their official MP4 previews.
- A processed **11,524-row** feature CSV, checksum manifest and deterministic sequence split.

Twenty `adl-37` feature rows have no matching official timestamp. They remain in the raw CSV and are explicitly excluded from the timed adapter; no timestamps are invented.

The small feature/timing files and previews are also bundled in the code archive. The larger RGB/depth archives are distributed separately to keep the Git repository manageable. Re-download from the official host if needed:

```bash
python scripts/download_urfall.py --sync --clips fall-01 adl-01 --videos
h-learning prepare-urfall
h-learning urfall-baseline --out runs/urfall_depth_baseline
```

For all RGB/depth sequences, pass the desired identifiers to `--clips`, for example `--clips fall-02 fall-03 adl-02`. The official complete collection is larger than the two image-sequence examples supplied here.

This is a **recorded real-world dataset**, not a live stream captured during this delivery. The feature baseline operates on Kinect-derived measurements, not MiDaS/BlazePose predictions. Its posture labels are not fraud intent or student-learning outcomes. These data are **CC BY-NC-SA 4.0**, separate from the MIT source-code licence. See [data/DATA_LICENSE.md](data/DATA_LICENSE.md).

### Execute both neural models on recorded RGB

```bash
h-learning run --urfall-dir data/urfall --sequence fall-01 --mode 0 \
  --headless --save-views --out runs/recorded_fall_01
h-learning run --urfall-dir data/urfall --sequence adl-01 --mode 1 \
  --headless --save-views --out runs/recorded_adl_01_learning
```

The learning-mode ADL replay tests the model and controller plumbing. It does not turn the ADL recording into a student experiment or supply intended-gesture ground truth. Headless prerecorded execution uses recorded timestamps for control decisions; its wall-clock throughput is reported separately. It does not prove 30-frame/s real-time operation.

## 5. Validation evidence included with this version

See [VALIDATION.md](VALIDATION.md) and `validation_runs/` for actual logs and the exact measurement scope.

- Python: **28 tests passed**, including 5,000 fault-injected frames, cancellation priority, timing, mode exclusivity, assessment and recovery.
- Compact SystemVerilog: **22 checks passed** in Icarus Verilog 11.0; simulator log and VCD included.
- Official data: all 70 sequence feature/timestamp files processed; fixed depth-feature baseline executed on 11,524 timed observations.
- Actual MiDaS + BlazePose inference: executed on the two supplied RGB recordings, with retained outputs and model checksums.

The full monitoring heuristic is an uncalibrated prototype and performs poorly on the supplied fall clip. The depth-only baseline's better scores must not be substituted for the full neural pipeline's scores. The measured CPU timings do not establish the manuscript's sub-60 ms latency claim. The supplied report identifies these limitations directly.

No original manuscript value—SSIM 0.89, PCK 92%, memory saving 40%, power saving 60%—is hard-coded as a validation result. Model quantization/pruning, physical ZCU104 deployment, ASIC implementation and measured energy savings are not implemented or validated here.

### Ground-truth-dependent vision and interaction metrics

MiDaS values are **relative inverse depth**, not calibrated metres. MediaPipe's hip-relative world coordinates are estimates, not reference motion capture. The UR Fall feature files do not provide the 33 independently measured 3D joints required for metric PCK.

```bash
python scripts/evaluate_vision.py independent_pairs.npz --metric pck \
  --threshold-m 0.1 --ground-truth-description "independent motion capture, hip-relative metres" \
  --out runs/pck/report.json
python scripts/evaluate_vision.py registered_images.npz --metric ssim --data-range 1 \
  --ground-truth-description "independently registered images, declared normalization" \
  --out runs/ssim/report.json
```

PCK input arrays are `pose_pred_m`, `pose_gt_m`, and optional `pose_valid`. SSIM inputs are `image_pred` and `image_gt`. Coordinate systems, registration, units and evaluation masks must be established before invoking these utilities. No automatic camera registration or metric-depth calibration is provided.

For intended-command accuracy, manually annotate the real recordings using `data/templates/interaction_annotations.csv`, then run:

```bash
python scripts/evaluate_interaction.py runs/P001_gesture/trace.csv annotations.csv \
  --out runs/P001_gesture/interaction_evaluation
```

`start_ms`/`end_ms` are non-overlapping intention windows in the session's source-time coordinate system. `expected_command` is an independently observed command or `NONE` for a neutral window. The template intentionally contains no invented observations. Learning-study design and outcome collection are in [docs/HUMAN_VALIDATION.md](docs/HUMAN_VALIDATION.md).

### Measured power

Supply actual meter readings in `time_s,power_w` format:

```bash
python scripts/analyze_power.py measured_power.csv \
  --meter-description "meter model, sampling rate, complete measurement boundary" \
  --battery-wh 37 --out runs/power/report.json
```

The script integrates measured power and reports energy. Nominal battery-capacity fraction is an estimate and is not measured state of charge. No power observations are bundled.

## 6. Reproducible figure and simulator exports

```bash
h-learning plot runs/demo/trace.csv --out runs/demo/figures
python scripts/export_interfaces.py runs/demo/synthetic_signals.csv --out runs/interfaces
```

Figure 3 shows depth/confidence/validity; Figure 4 shows abnormal evidence/alert; Figure 5 shows mode/branch enables; Figure 6 shows education state/commands/recovery. JPEG plots are drawn from the specified trace and visibly identify its source kind. Choose a recorded or participant trace to plot measured data. Demo plots stay labelled synthetic.

### MATLAB / Simulink–Stateflow

From this repository root in MATLAB:

```matlab
addpath('matlab');
build_H_Learning_Stateflow('runs/interfaces/matlab_signals.csv', 'runs/matlab');
open_system('H_Learning_Compact/ExecutionScope');
Simulink.sdi.view;
```

The builder creates an actual Stateflow diagram and Simulink Scope, executes the compact control model and saves `.slx`, `.mat` and an execution plot **when run in MATLAB**. It replays input values on a 1 ms grid with source-frame strobes. It uses two stability samples and eight monitoring samples, rather than the software's elapsed-time thresholds. It starts acquisition automatically; after compact reset/cancel, explicit START is required. It is not equivalent to the complete Python education controller. MATLAB, Simulink and Stateflow are required; this script is supplied **unexecuted** because they are unavailable in the delivery environment.

### QSPICE and WaveDrom

`runs/interfaces/H_Learning_Interface.cir` replays voltage inputs, tests comparator/validity gating and an RC depth interface. Open and run it in QSPICE from the same folder as its PWL files. Plot `V(depth)`, `V(depth_filtered)`, `V(fusion)`, `V(mode)`, `V(monitor_gate)` and `V(education_gate)`. `alert_reference` is a software-reference input, not a circuit-computed fall alert. The file does not model analog neural inference, optical display or a complete physical latch implementation. QSPICE execution is not claimed here.

WaveDrom JSON uses **sample index**, with real timestamps in `matlab_signals.csv`. WaveDrom renders timing; it does not simulate or verify the circuit.

## 7. FPGA / ASIC control-core path

```bash
python scripts/run_rtl_validation.py --out runs/rtl
vivado -mode batch -source rtl/create_zcu104_project.tcl
```

The Tcl targets the ZCU104 part `xczu7ev-ffvc1156-2-e` and performs **out-of-context control-core synthesis**. Vivado synthesis was not run here. RTL inputs must be delivered atomically in the controller clock domain with a frame strobe and a paired-frame validity flag. Use an AXI/register bridge and proper clock-domain crossings in a board design; they are not supplied as a ready-to-boot platform image. No physical pin assignments, board bitstream or FPGA power numbers are claimed. ASIC implementation also needs a technology library and physical-design flow.

The compact RTL uses the paper's eight state codes, has explicit START after reset/cancel and uses sample-count confirmation. It is a reference control component, not the entire three-FSM Python application or an FPGA implementation of MiDaS/BlazePose. See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## 8. Publish the code to your GitHub repository

Create an empty GitHub repository, then execute locally:

```bash
git init -b main
git add .
git commit -m "Add H-Learning reference implementation and validation workflow"
git remote add origin https://github.com/YOUR_USERNAME/H-Learning.git
git push -u origin main
```

No GitHub repository was created or pushed during this delivery. `.gitignore` excludes neural weights, large recording archives, personal live sessions and build files. The official data licence and attribution remain in the repository. Put the larger dataset archive in a release or provide the official download commands; do not treat it as MIT data.


##For the data validation against different datasets:##

# H Learning data starter

This package provides a small example dataset and a collection workflow for the H-Learning paper. All populated observations are invented synthetic examples. No people were recruited, no camera or board was measured, and no MiDaS or BlazePose model was run to create these records. They demonstrate file structure and analysis only. They do not substantiate the paper's reported accuracy, latency, memory or power values.

## Start here

1. Open `H_Learning_Data_Starter.xlsx`. `Synthetic_demo` contains 90 example trials; `Real_trials` is a blank collection sheet with calculated columns. Neither sheet contains real experimental results.
2. Read `data_dictionary.csv` before collecting observations. Use `real_templates/` to start your own logs. Preserve the CSV headers and use an empty field for missing/not-applicable data.
3. Keep invented examples in `synthetic_demo/`. Put only actual collected observations in `real_templates/` or, preferably, copy the templates into a new folder named `real_run_001`.
4. Run the demonstration with Python 3.10 or later, without installing packages:

```bash
python scripts/analyze.py --input synthetic_demo --mode demo --output results/DEMO_metrics.json
```

5. After collecting real data and filling the configuration, run:

```bash
python scripts/analyze.py --input real_run_001 --mode real --raw-root . --output results/real_metrics.json
```

The default mode is `real`. It rejects synthetic rows, missing raw evidence files, duplicate trial IDs, participant/sequence split leakage, and invalid intervals. The script calculates descriptive metrics, not significance tests or a publication acceptance decision. Workbook formulas update in the prepared 30-row real-entry area. Copy formulas AA:AD into new rows if you extend that area. Export only the raw table as CSV, not the Guide sheet.

Real-mode analysis defaults to the held-out `test` split; demo mode defaults to `all`. You can specify `--split validation` for development reports. Do not pool training and test observations for final evaluation. Pose output is pooled over the selected records: restrict input to the method/protocol being evaluated before using it in a paper.

## What is included

| File | One row represents | Purpose |
|---|---|---|
| synthetic_demo/trials.csv | One interaction trial | 90 invented trials from six fictional participants, three input methods and five commands |
| synthetic_demo/joints.csv | One joint in one frame | 120 invented records: three joints, 20 frames, two example trials |
| synthetic_demo/power.csv | One power sample | 540 invented voltage/current samples linked by trial ID |
| real_templates/trials.csv | One real interaction trial | Empty template with identical headers |
| real_templates/joints.csv | One real joint in one frame | Empty pose-reference template |
| real_templates/power.csv | One real power sample | Empty instrument-log template |
| real_templates/image_pairs.csv | One aligned reference/prediction pair | Image evaluation manifest; no images or SSIM scores are supplied |
| real_templates/learning_outcomes.csv | One participant, lesson and condition | Optional pre/post/retention and workload log; no survey responses are supplied |
| real_templates/monitoring_events.csv | One annotated monitoring interval | Separate abnormal-motion/alert evaluation; never label motion as fraudulent intent |
| config/real_config_template.json | One run configuration | Hardware, models, thresholds, measurement settings and provenance |

Synthetic trials use a fixed random seed, 20261105. All three methods use the same toy delay/error generation rules. Example differences are random, not evidence that any method is better. The six fictional participants and sparse sample rates are not a recommended sample size or instrument configuration.

## A practical collection plan

### 1 Define the comparison before recording

Choose a primary endpoint, such as unintended activations per minute or task completion rate. Compare the proposed FSM controller, direct gesture mapping and mouse/keyboard on the same objects, lesson content, target criteria and device configuration. Mouse/keyboard is a usability reference, not a camera-algorithm benchmark. For algorithm comparisons, replay the same held-out captures through each eligible vision/controller variant.

Include selection, rotation, zoom and next-object tasks, plus fixed-duration no-command windows. Record dim light, occlusion, short noise bursts, deliberate cancellation, tracking loss and recovery. Change one mechanism at a time for ablations such as no temporal confirmation or no clock gating. Define the expected response and any exclusion rule in advance. Save every action to the raw UI log, even though the summary CSV retains only the first executed command.

Begin with a small pilot to debug synchronization, task instructions and logging. Use pilot variability and a meaningful effect size to plan the final participant count. The sample here does not justify a specific final sample size. Randomize/counterbalance method order and use matched tasks to reduce practice effects. Obtain the approvals and participant consent required by your institution; use pseudonyms and store the participant-name key separately.

### 2 Record raw evidence before calculating results

For each trial retain the original RGB capture, any depth/reference capture, per-frame landmarks, raw UI events, state transitions, model confidence, and configuration. A saved capture manifest can point to large or restricted recordings. Store raw files under `raw/`, keep them unchanged, and write cleaned/derived records under `processed/`.

Use `trial_id` to join logs. Use monotonic timestamps with documented clock synchronization. `input_event_ms` must come from independently annotated action onset. `display_update_ms` must identify the declared presentation boundary. A render-submission timestamp is not physical motion-to-photon latency. For physical display latency, use a synchronized external measurement such as a photodiode or high-speed camera and document the method.

Keep a versioned configuration for camera intrinsics, model/checkpoint hashes, image resolution, quantization, gesture thresholds, FSM logic, device, operating system, software commit, display refresh rate and instrument calibration. The example memory column is peak resident process memory in MiB; it does not measure memory activity or transferred bytes.

### 3 Keep training and evaluation separate

For your own learned/tuned models, assign whole participants and source sequences to train, validation or test once. Do not randomly split neighbouring frames. Fit thresholds, depth alignment and any learned mapping on training/validation data and freeze them before final evaluation. Use official splits and protocols for public benchmarks. The supplied script checks participant and source-sequence disjointness in the example manifest, but cannot detect duplicated video bytes unless you also track hashes.

If the study evaluates a fixed interface rather than training a model, identify the held-out evaluation cohort explicitly. Do not describe ordinary repeated interaction trials as model training. Keep the mapping of benchmark joints to BlazePose joints fixed and document missing joints, coordinate systems and any allowed alignment.

### 4 Calculate each metric from its correct source

| Metric | Calculation and required evidence |
|---|---|
| Correct command rate | Correctly executed intended commands / intended-command trials. NONE windows have a separate denominator. |
| Task completion rate | Trials meeting the predefined object/task target / intended-task trials. A recognized command alone is insufficient. |
| False activation rate per window | NONE windows containing an action / all predefined NONE windows. Do not call this a frame-based false-positive rate. |
| Unintended actions per minute | Count all unintended actions / observation time in minutes. |
| Response latency | Display-update time minus ground-truth input onset for correctly executed commands. Report the number of valid intervals, failures, median and tail latency. |
| Tracking recovery | Recovery time minus tracking-loss onset. Report unrecovered episodes separately; the script's latency summary covers recovered intervals only. |
| PCK at 0.1 m | Correct joints within 0.1 m / all usable ground-truth joints. Missing predictions count as failures. Predictions and reference must use the same calibrated metric frame. |
| MPJPE | Mean Euclidean joint error, reported in mm, with the protocol and prediction coverage stated. The script uses available predictions and reports their coverage. |
| Power and energy | P(t)=V(t)I(t). Integrate power over elapsed seconds using the trapezoidal rule; divide joules by 3.6 for mWh. Report instrument, sample rate and whole-system/device scope. |
| Memory reduction | Compare the same defined memory metric on the same workload/device. Peak resident memory, traffic and memory activity are different quantities. |
| SSIM | Requires aligned predicted and reference images, an explicitly defined reconstruction target, common resolution/range and a declared mask. No SSIM is calculated by this package. Do not calculate it from voltages or pose CSVs. |

MiDaS relative depth values are not automatically metres. A metric PCK threshold needs an independently calibrated pose/reference coordinate system. If evaluating relative depth, specify and apply the appropriate benchmark alignment and depth metrics. Do not select alignment separately to improve each test example without declaring that protocol.

For power comparisons, record the same workload and measurement boundary for baseline and proposed conditions. Six synthetic samples per five-second trial only demonstrate the schema; choose a real instrument/sample rate appropriate to transient power. The script reports the maximum sampled power, not a guaranteed instantaneous peak. Convert energy to battery percentage only using the stated usable battery capacity and assumptions; label that percentage as derived rather than measured charge depletion.

### 5 Report uncertainty and provenance

Repeated frames and trials from the same participant are correlated. Calculate participant-level paired differences and uncertainty for the main comparisons; do not treat thousands of frames as thousands of independent people. Report errors, exclusions, unsuccessful trials, missing predictions and unrecovered tracking episodes. The supplied descriptive report does not calculate confidence intervals or hypothesis tests.

Use `results/DEMO_metrics.json` only to inspect the workflow. Actual paper tables must come from the real logs and a frozen analysis configuration. Preserve a table-to-input mapping, software version, run configuration and checksums so each published value can be reproduced. Adding a sample dataset does not resolve incorrect citations or validate a holographic display implementation.

## Public datasets that can support individual components

These datasets are not included in this package. Obtain them from their maintainers, follow their access/license conditions, use the official protocols and cite the original work.

- **NYU Depth V2** provides indoor RGB/depth recordings, including aligned labeled image pairs and depth in metres. It can support depth evaluation, not your own interface usability or power claims. https://cs.nyu.edu/~fergus/datasets/nyu_depth_v2.html
- **MPI-INF-3DHP** provides human pose data with independent 3D ground truth and an indoor/outdoor evaluation benchmark. It can support a documented, joint-mapped pose evaluation. https://vcai.mpi-inf.mpg.de/3dhp-dataset/
- **EgoGesture** provides color/depth hand-gesture recordings. It may support gesture recognition after defining which gestures correspond to your commands; it does not provide your H-Learning lesson outcomes. https://english.ia.cas.cn/jp/eiathesis/201807/t20180710_194944.html

Real end-to-end H-Learning interaction, display timing, board power and educational outcomes require recordings from the implemented system and the appropriate study. Public vision datasets alone do not supply those measurements.


## Repository layout

| Path | Purpose |
|---|---|
| `src/h_learning/` | Core FSM, real inference, acquisition, display, replay and metrics |
| `config/` | Temporal thresholds and example lesson content |
| `scripts/` | Downloads, annotation evaluation, power analysis, exports and RTL runner |
| `tests/` | Controller fault/behavior and metric tests |
| `rtl/` | Compact control core, testbench and ZCU104 synthesis Tcl |
| `matlab/` | Actual compact Stateflow model builder |
| `data/` | Official features/timestamps, provenance and empty study templates |
| `validation_runs/` | Executed recorded/synthetic runs and simulator evidence |
| `docs/` | Architecture, study design and dataset description |

## Attribution and licence

Original repository code: [MIT](LICENSE). UR Fall data and their redistributed/derived examples: [CC BY-NC-SA 4.0](data/DATA_LICENSE.md). Third-party models and packages retain their upstream terms. Cite the supplied manuscript as an unpublished draft until a publication record exists, and cite the original model/dataset papers in [docs/references.bib](docs/references.bib).
