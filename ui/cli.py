import sys
from pathlib import Path
from health.healthpacket import process_health

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))


from telemetry.load_csv import run_csv




while True:
    print("==================================================")
    print("VisualGS = Ground Station Launcher")
    print("==================================================")
    print("\n")
    print("Select an operation mode: ")
    print("\n")
    print("1. Live Serial")
    print("2. Replay Flight Data (CSV)")
    print("3. Health Check")
    print("4. Exit")
    print("\n")

    try:
        choice = int(input("Enter choice [1–4]:"))
    except ValueError:
        print("(WARNING) Enter valid choice")
        continue

    if choice == 2:
        print("--------------------------------------------------")
        print("Replay Mode - Flight Data  ")
        print("--------------------------------------------------")
        try:
            datapath = input("Enter File path : ").strip()

            patha = Path(datapath)
            if not patha.is_file():
                print("File Not Found !!!")
                continue

            speed = float(input ("Enter speed in x"))

        except ValueError:
            print("Require valid input !!!")
            continue
        if speed <= 0 :
            print("Cant be negative")
            continue
        

        run_csv(mode = "replay", filepath=str(patha) , speed = speed)

    elif choice == 1:
        print("--------------------------------------------------")
        print("Live Telemetry Mode  ")
        print("--------------------------------------------------")
        print("\n")
        print("Scanning serial ports ...")
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
