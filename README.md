Radar Signal Processing Simulator

A modular Python-based radar receiver simulation that generates radar pulses, adds realistic noise, applies detection algorithms, and evaluates system performance using matched filtering and sensitivity analysis.

This project models the core behaviour of a basic radar receiver pipeline, including signal generation, noise modelling, threshold detection, hysteresis detection, matched filtering, segment extraction, grouping, and performance evaluation.

✨ Features
Signal Generation

Configurable sampling rate and duration

Rectangular radar pulse generator

Adjustable pulse start, end, and amplitude

Noise Modelling

Gaussian noise generation

Adjustable noise sigma (standard deviation)

Combined received signal (pulse + noise)

Detection Algorithms

Simple threshold detection

Hysteresis-based detection

Detection window extraction

Segment grouping to merge close detections

Matched filter detection using FFT convolution

Matched Filtering

Template-based matched filter

Normalized output for thresholding

Sharp peak response for easy detection

Outperforms simple thresholding under noise

Visualization

Raw signal plot

Noisy signal plot

Threshold detection plot

Matched filter output plot

Grouped detection windows

Hysteresis detection marking

Sensitivity Analysis

Sweeps multiple noise levels

Sweeps multiple matched filter thresholds

True positive rate

False alarm rate

Latency and duration error

Heatmap visualizations

📁 Project Structure
radar-simulator/
│
├── src/
│   ├── __init__.py
│   ├── timebase.py           # Generates time axis
│   ├── pulse.py              # Pulse generator
│   ├── noise.py              # Noise model
│   ├── detect.py             # Detection algorithms
│   ├── filter.py             # Matched filter implementation
│   ├── run_sim.py            # Main simulation + plots
│   └── sensitivity.py        # Parameter tuning & heatmaps
│
├── tests/
│   └── test_pulse.py
│
├── venv/                     # Virtual environment
├── README.md
└── .gitignore

🛠️ Installation
1. Clone the repo
git clone <your-repo-url>
cd radar-simulator

2. Create and activate virtual environment

Windows:

python -m venv venv
venv\Scripts\activate

3. Install dependencies
pip install numpy matplotlib scipy pytest

🚀 Running the Simulation
Run the radar simulation:
python -m src.run_sim


This generates:

Noisy radar signal plot

Matched filter output

Threshold and hysteresis detections

Detection windows printed on console

📊 Running Sensitivity Analysis

Evaluate how detection behaves under different noise levels and thresholds:

python -m src.sensitivity


Generates:

True positive heatmap

False alarm heatmap

Prints metrics for each parameter combination

🧪 Tests

Run unit tests:

python -m pytest -q

📦 Dependencies

Python 3.10+

NumPy

Matplotlib

SciPy

PyTest

🎯 Use Cases

This project is ideal for:

Radar signal processing learning

System-level simulation

Real-time detection concept study

Interviews for embedded/system/software roles

Academic mini-projects

👨‍💻 Author

Kancherla Abyudhay
Radar Signal Processing Simulator — 2025
GitHub: your link
LinkedIn: your link