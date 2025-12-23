Telemetry Data Cleaner & Analyzer

This project is a ground-side telemetry processing tool built to handle raw rocket (or similar embedded system) telemetry data.

The goal is simple and strict:

Never trust raw telemetry.
Validate it, separate good data from bad data, and make the results usable.

This tool focuses on correctness, robustness, and clarity before visualization or UI.

What this project does

Given a CSV file containing raw telemetry data, the tool:

Ingests raw data

Converts it into typed packets

Validates each packet

Separates good and bad packets

Writes results to clean output files

Generates run statistics

Optionally derives altitude from pressure

Input format

The input CSV must contain the following columns:

t,pre,ax,ay,az


Where:

t → timestamp (int, ms since boot)

pre → pressure (Pa)

ax → acceleration x

ay → acceleration y

az → acceleration z

Example:

t,pre,ax,ay,az
0,101325,0.01,-0.02,9.78
20,101320,0.05,-0.01,9.80


Malformed rows or invalid values are expected and handled.

Output files

After running, the tool generates:

accept.csv

Contains only valid packets.

t,pre,ax,ay,az
0,101325,0.01,-0.02,9.78
20,101320,0.05,-0.01,9.80

reject.csv

Contains invalid packets + rejection reason.

t,pre,ax,ay,az,error
140,-100900,4.20,0.08,12.30,Negative or zero pressure

Console summary

At the end of each run, a summary is printed:

--- Packet Statistics ---
Total     : 14
Accepted  : 10
Rejected  : 4


This gives immediate insight into telemetry quality.

Project structure
telemetry/
├── load_csv.py      # Main driver (orchestration)
├── packet.py        # Packet data model + validation + altitude
├── stati.py         # Statistics + CSV writing
├── dataset.csv      # Input telemetry file
├── accept.csv       # Output: valid packets
├── reject.csv       # Output: rejected packets
└── README.md

Design principle

Each file has one responsibility:

packet.py → what a packet is and whether it is valid

stati.py → recording results and writing outputs

load_csv.py → wiring everything together

Validation logic (current)

A packet is rejected if:

timestamp is negative

pressure is zero or negative

values are malformed or missing

Each rejected packet carries a human-readable error reason.

Validation is intentionally conservative and can be extended later.

Altitude calculation

For accepted packets, altitude can be derived using the barometric formula:

ℎ
=
44330
⋅
(
1
−
(
𝑝
𝑝
0
)
0.1903
)
h=44330⋅(1−(
p
0
	​

p
	​

)
0.1903
)

Where:

p = packet pressure

p0 = 101325 Pa (sea-level reference)

This is optional and kept separate from validation.

How to run

From the project directory:

python load_csv.py


Requirements:

Python 3.10+

No external libraries required

Why this project exists

This project was built to solve a real engineering problem:

Raw telemetry is noisy, unreliable, and often misleading.
Analysis, visualization, or control logic built on bad data is worse than useless.

This tool enforces a clean boundary:

Only trusted data moves forward.