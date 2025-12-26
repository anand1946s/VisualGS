# VisualGS

VisualGS is a Python-based ground station software for processing, validating, and replaying rocket telemetry data.

## Features

- Parses raw telemetry packets
- Validates packets and separates accepted/rejected data
- Generates basic plots
- Supports **replay of telemetry CSVs with real-time speed control**
- Uses the same pipeline for replay and live serial data

## Requirements

- Python 3.10+
- Works on Windows (serial via COM ports)


## Setup

Clone the repository:

```bash
git clone https://github.com/<your-username>/VisualGS.git
cd VisualGS
```

Create and activate a virtual environment (recommended):

python -m venv .venv
.venv\Scripts\activate   # Windows


### 5. How to run replay (your killer feature)

This section is what makes your project usable.

```md
## Running Telemetry Replay

Prepare a CSV file with the format:

t,pre,ax,ay,az

Example timestamps are in milliseconds.

Run the CLI:

```bash
python -m ui.cli
```


## Design Philosophy

- Raw telemetry is never trusted
- Validation happens before visualization
- Replay and live telemetry share the same processing pipeline
- Time fidelity is preserved during replay