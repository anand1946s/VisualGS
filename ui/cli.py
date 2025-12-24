import sys
from pathlib import Path
from health.healthpacket import process_health

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))


from telemetry.load_csv import run_csv




while True:
    print("=== Telemetry Processor ===")
    print("1: Load CSV")
    print("2: Live Serial")
    print("3: Run Health Checkup")
    print("4: Exit")

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
        com = input("Enter COM No (e.g. 3): ")
        try:
            baud = int(input("Enter baudrate: "))
        except ValueError:
            print("Invalid baudrate")
            continue

        process_health(port=f"COM{com}", baudrate=baud)


    elif choice == 4:
        print("Exiting...")
        sys.exit(0)
    else:
        print("(WARNING Enter choice (1,2,3))")
        continue
