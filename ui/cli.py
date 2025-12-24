import sys
from pathlib import Path
from health.healthpacket import process_health

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))


from telemetry.load_csv import run_csv




while True:
    print("=== Telemetry Processor ===")
    print("1: Run Replay")
    print("2: Live Serial")
    print("3: Run Health Checkup")
    print("4: Exit")

    try:
        choice = int(input("Enter a choice: "))
    except ValueError:
        print("(WARNING) Enter valid choice")
        continue

    if choice == 1:
        try:
            speed = float(input ("Enter speed in x"))
        except ValueError:
            print("Require valid input !!!")
            continue
        if speed <= 0 :
            print("Cant be negative")
            continue
        

        run_csv(mode = "replay", filepath="telemetry/dataset.csv" , speed = speed)

    elif choice == 2:
        print("Reading live serial data...  ")
        run_csv(mode = "serial")  

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
