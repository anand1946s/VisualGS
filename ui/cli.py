import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))


from telemetry.load_csv import run_csv




while True:
    print("=== Telemetry Processor ===")
    print("1: Load CSV")
    print("2: Live Serial")
    print("3: Exit")

    try:
        choice = int(input("Enter a choice: "))
    except ValueError:
        print("(WARNING) Enter valid choice")
        continue

    if choice == 1:
        run_csv(mode = "csv", filepath="telemetry/dataset.csv")

    elif choice == 2:
        print("Reading live serial data...  ")
        run_csv(mode = "serial")  # this needs to be implemented in load_csv.py

    elif choice == 3:
        print("Exiting...")
        sys.exit(0)
    else:
        print("(WARNING Enter choice (1,2,3))")
        continue
