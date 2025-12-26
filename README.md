# VisualGS

VisualGS is a Python-based ground station software for model rocketry.  
It supports live telemetry over serial, replay of recorded flight data, and basic offline analysis.

---

## Features

- Live telemetry over serial
- Replay telemetry from CSV with adjustable speed
- Health packet monitoring
- Offline plots (pressure, altitude, velocity)

---

## Requirements

- Windows
- Python 3.10 or newer

No additional tools are required.

---

## Quick Start

## Note
Currently this tool expects data in the CSV format

[time,pre,ax,ay,az]

The input source must be tuned for that.



### 1. Clone the repository
```bash
git clone <git@github.com:anand1946s/VisualGS.git>
cd VisualGS
```
### 2.  Run the File

```bash
start.bat
```
This will start the application, install dependencies,create virtual environment and waits for instruction


## How To Use

After setting up run

```bash
visualgs run
```

this will open up an interactive menu to use custom features


```bash
visualgs live
```
This will directly open COM port and waits for data packets to arrive

```bash
visualgs replay <filepath> --speed <speed>
```
Will start replay a custom dataset of a flight with specified speed

```bash
visualgs health
```
To recieve healthdata packets and evaulate mission readiness  pre-flight

All these features can be attaoined through menu driven commands also



## Project Structure

VisualGS/
├── ui/ # CLI entry points and interactive menus
├── telemetry/ # Telemetry parsing, replay, plotting
├── health/ # Health packet handling
├── examples/ # Sample datasets
├── start.bat # Windows bootstrap script
├── pyproject.toml # Project metadata and dependencies
└── README.md


Generated at runtime (not committed):
- `.venv/`
- `.visualgs/`
- `datasets/`
- `plots/`

