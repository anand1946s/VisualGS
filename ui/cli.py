import argparse

from ui.launcher import (
    interactive_launcher,
    run_live,
    run_replay,
    run_health,
    run_replay_noninteractive
)

def main():
    parser = argparse.ArgumentParser(
        prog="visualgs",
        description="VisualGS – Ground Station"
    )

    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("run", help="Open interactive launcher")
    sub.add_parser("live", help="Run live telemetry")

    replay = sub.add_parser("replay", help="Replay flight data")
    replay.add_argument("file")
    replay.add_argument("--speed", type=float, default=1.0)

    sub.add_parser("health", help="Run health check")

    args = parser.parse_args()

    # -------- dispatch --------
    if args.cmd is None or args.cmd == "run":
        interactive_launcher()

    elif args.cmd == "live":
        run_live()

    elif args.cmd == "replay":
        run_replay_noninteractive(args.file, args.speed)

    elif args.cmd == "health":
        run_health()


if __name__ == "__main__":
    main()
