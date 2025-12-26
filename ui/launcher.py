import sys
from pathlib import Path
from health.healthpacket import process_health
from telemetry.load_csv import run_csv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))



def run_live():
    print("--------------------------------------------------")
    print("Live Telemetry Mode")
    print("--------------------------------------------------\n")
    print("Scanning serial ports ...")
    run_csv(mode="serial")

def run_replay():
    print("--------------------------------------------------")
    print("Replay Mode - Flight Data")
    print("--------------------------------------------------")

    try:
        datapath = input("Enter File path : ").strip()
        patha = Path(datapath)

        if not patha.is_file():
            print("File Not Found !!!")
            return

        speed = float(input("Enter speed in x"))
        if speed <= 0:
            print("Speed must be positive")
            return

    except ValueError:
        print("Invalid input")
        return

    run_csv(mode="replay", filepath=str(patha), speed=speed)


def run_health():
    com = input("Enter COM No (e.g. 3): ")
    try:
        baud = int(input("Enter baudrate: "))
    except ValueError:
        print("Invalid baudrate")
        return

    process_health(port=f"COM{com}", baudrate=baud)


def interactive_launcher():
    while True:
        print("==================================================")
        print("VisualGS = Ground Station Launcher")
        print("==================================================\n")
        print("Select an operation mode:\n")
        print("1. Live Serial")
        print("2. Replay Flight Data (CSV)")
        print("3. Health Check")
        print("4. Exit\n")

        try:
            choice = int(input("Enter choice [1–4]: "))
        except ValueError:
            print("(WARNING) Enter valid choice")
            continue

        if choice == 1:
            run_live()

        elif choice == 2:
            run_replay()

        elif choice == 3:
            run_health()

        elif choice == 4:
            print("Exiting...")
            sys.exit(0)

        else:
            print("(WARNING) Enter choice (1,2,3,4)")


def run_replay_noninteractive(filepath, speed):
    patha = Path(filepath)

    if not patha.is_file():
        print("File Not Found !!!")
        return

    if speed <= 0:
        print("Speed must be positive")
        return

    run_csv(mode="replay", filepath=str(patha), speed=speed)

