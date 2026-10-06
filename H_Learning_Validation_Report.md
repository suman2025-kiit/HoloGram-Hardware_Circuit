# Executed validation report — 6 October 2026

The evidence in this release separates software correctness, recorded-data
experiments and compact RTL simulation. It does not establish physical FPGA
execution or student learning outcomes.

## Executed checks

| Check | Result | Retained evidence |
|---|---|---|
| Python behavior/metric tests | 28 passed, 0 skipped | `validation_runs/python_checks/unittest.log` |
| Fault injection | 5,000 frames, assertions passed | Deterministic seeded test in `tests/test_controller.py` |
| CLI, interface exports, PWL time ordering | Passed | `validation_runs/python_checks/report.json` |
| Core synthetic demonstration | 110 input frames, 5 committed commands, no invariant violations | `validation_runs/synthetic_controller/` |
| Compact RTL | 22 checks passed in Icarus Verilog 11.0 | `validation_runs/rtl/simulator.log`, `.vcd`, `report.json` |
| Source compilation | Python source, scripts and tests compiled successfully | `python -m compileall -q src scripts tests` |
| Editable package installation | Successful on Python 3.12 | `pyproject.toml`, command-line entry point |
| Official timestamp join | 11,524 timed rows from 11,544 original observations | `data/processed/urfall_recorded_features.manifest.json` |
| Real neural inference | Both models executed on 310 recorded RGB frames | Two recorded run directories listed below |

The checked invariants cover branch exclusivity, synchronized frame identity,
valid tracking for commands, monitoring-only alerts, cancellation priority and
valid fusion for enabled branches. Successful invariants prove the stated
control behavior under the tested inputs, not detector accuracy.

## Actual MiDaS + BlazePose recorded runs

| Measurement | `fall-01`, monitoring | `adl-01`, learning-mode replay |
|---|---:|---:|
| Processed frames | 160 | 150 |
| Paired-valid frames | 126 | 136 |
| Fusion-valid frames | 115 | 133 |
| Paused frames | 45 | 17 |
| Committed educational commands | 0 | 0 |
| Alert-output frames | 1 | 0 |
| Controller invariant violations | 0 | 0 |
| Mean serial processing (ms) | 224.14 | 243.22 |
| Median serial processing (ms) | 210.59 | 218.07 |
| 95th-percentile processing (ms) | 337.48 | 413.45 |
| Maximum processing (ms) | 593.90 | 602.90 |
| Wall throughput including I/O (frames/s) | 4.08 | 3.72 |

Directories:

- `validation_runs/recorded_fall_01/`
- `validation_runs/recorded_adl_01_learning/`

These are prerecorded image-sequence runs, with original camera-0 timestamps
used for control. Serial timing includes inference and control; wall throughput
also includes decoding, logging and saved-view rendering. Warm-up is included.
The reported timings do **not** support sub-60 ms processing on this host.
They do not measure sensor exposure, display refresh or end-to-end physical
latency. The ADL recording contains no annotated lesson intentions, so zero
commands in that replay is not a student-gesture accuracy result.

The monitoring heuristic performs poorly on this fall clip. On its 130
nontransitional labelled frames, the alert output has TP=1, FN=47, TN=82 and
FP=0. Lying-posture recall is therefore **2.08%**, despite its control
invariants passing. Pose availability, heuristic thresholds, confirmation and
output masking affect this result. Use these logs to calibrate on designated
training recordings; evaluate a held-out collection afterward. This run is a
prototype demonstration, not evidence of a validated fall-detection system.

## Separate Kinect depth-feature baseline

This benchmark uses the provider's recorded depth features directly, with
fixed thresholds and temporal persistence. It does not invoke MiDaS or
BlazePose. Split assignment is by sequence index, with no asserted separation
of participants. Label-0 transitions remain in temporal processing but are
excluded from binary posture metrics.

| Split | Labelled posture frames | Posture accuracy | Posture recall | Posture F1 | Any-alert fall-sequence accuracy |
|---|---:|---:|---:|---:|---:|
| Train: 42 sequences | 6,387 | 90.70% | 71.81% | 0.7174 | 78.57% |
| Validation: 14 sequences | 1,442 | 98.54% | 96.47% | 0.9791 | 78.57% |
| Test: 14 sequences | 1,976 | 91.04% | 77.68% | 0.8744 | 57.14% |

Test any-alert event counts are TP=6, TN=2, FP=6, FN=0. ADL clips can include
intentional lying, which explains why lying posture and an actual fall event
are different labels. These scores must not replace the full neural
pipeline's results. Exact thresholds and all confusion matrices are in
`validation_runs/urfall_depth_baseline/report.json`.

Twenty source observations—`adl-37`, frames 331–350—lack corresponding
recorded timestamps. They are retained in the original CSV, excluded from
the timed derivative, and listed in its manifest. No missing time was
estimated or inserted.

## Models and environment

| Item | Value |
|---|---|
| Runtime | Python 3.12.14, Linux x86-64 CPU |
| OpenCV contrib | 4.14.0.94 |
| MediaPipe | 0.10.35 |
| NumPy | 2.3.5 |
| SciPy | 1.17.0 |
| Matplotlib | 3.10.8 |
| OpenCV worker setting | 2 threads |
| MiDaS model | Official v2.1 small ONNX, 256×256 letterboxed input |
| Pose model | Official Pose Landmarker lite, float16 bundle, CPU execution |

MiDaS SHA256:
`2d8c6cb8f415229daf1eb041024208e2608c9f98e17c81cc7c6ecb449c56fd58`

Pose-model SHA256:
`59929e1d1ee95287735ddd833b19cf4ac46d29bc7afddbbf6753c459690d574a`

The ONNX path letterboxes to its fixed input shape, uses RGB ImageNet
normalization, crops padding from the prediction and resizes back to the
source. A bounded EMA stabilizes depth. These declared implementation choices
are not asserted equivalent to a pruned/quantized model in the manuscript.
MiDaS depth remains relative; estimated pose world coordinates are not
independent ground truth. Full run metadata identify model hashes and timing
scope.

## Supplied but unexecuted here

| Item | Status |
|---|---|
| New live webcam/participant capture | Recorder implemented; no camera or participants captured here |
| MATLAB/Simulink–Stateflow model | Builder supplied; required tools unavailable here |
| QSPICE voltage-interface transient simulation | Model/export supplied; QSPICE unavailable here |
| Vivado ZCU104 synthesis | Tcl supplied; Vivado unavailable here |
| Physical ZCU104/ASIC implementation | Not deployed or measured |
| Independent metric PCK/SSIM dataset experiment | Utilities tested; independent ground truth not supplied |
| Student study and learning gains | Templates/protocol supplied; observations not collected |
| Power measurement and optimization savings | Meter-analysis utility supplied; no power samples or savings measured |

The RTL VCD is an accelerated synthetic control-core waveform, not physical
hardware acquisition. Generated JPEG trace plots are explicitly labelled by
their source kind. Python execution views from UR Fall recordings are saved
from actual software execution and do not represent MATLAB or QSPICE windows.

