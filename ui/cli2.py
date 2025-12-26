import argparse
from telemetry.load_csv import run_csv


def main():
    parser = argparse.ArgumentParser(
        prog="visualgs",
        description="VisualGS – telemetry ground station"
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True
    )

    # -------- run (live serial) --------
    subparsers.add_parser(
        "run",
        help="Run live telemetry over serial"
    )

    # -------- replay (CSV) --------
    replay_parser = subparsers.add_parser(
        "replay",
        help="Replay telemetry from CSV"
    )

    replay_parser.add_argument(
        "filepath",
        help="Path to telemetry CSV file"
    )

    replay_parser.add_argument(
        "--speed",
        type=float,
        default=1.0,
        help="Replay speed multiplier (default: 1.0)"
    )

    args = parser.parse_args()

    # -------- dispatch --------
    if args.command == "run":
        run_csv(mode="serial")

    elif args.command == "replay":
        run_csv(
            mode="replay",
            filepath=args.filepath,
            speed=args.speed
        )


if __name__ == "__main__":
    main()
