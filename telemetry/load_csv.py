import csv , time, os, sys
from rich.console import Console
from rich.table import Table
from rich.live import Live
from .packet import Packet
from .stati import Packetstat
from .plotter import Plotter
from .serialize import Serialize
from .serialize import find_ports , update_status_line


def run_csv(mode = "replay",filepath = "dataset.csv", speed = 1.0):
    console = Console()
    stati = Packetstat()
    accepted_packets = []


    if mode == "replay":

        last_lat = None
        last_lon = None

        prev_t = None
        prev_packet = None
        prev_vel = 0.0

        with Live(console=console, refresh_per_second=10) as live:
            with open(filepath, "r") as f:
                reader = csv.reader(f)
                next(reader)

                for row in reader:
                    data = csv_to_dict(row)
                    if data is None:
                        stati.malformed()
                        continue

                    packet = Packet(
                        data["t"],
                        data["pre"],
                        data["ax"],
                        data["ay"],
                        data["az"],
                        data["lat"],
                        data["lon"],
                    )

                    if packet.lat is not None and packet.lon is not None:
                        last_lat = packet.lat
                        last_lon = packet.lon

                    if prev_t is not None:
                        dt = packet.t - prev_t
                        if dt > 0:
                            time.sleep((dt / speed) / 1000)
                    prev_t = packet.t

                    if packet.validate():
                        stati.accept(packet)
                        accepted_packets.append(packet)

                        vel = compute_velocity(prev_packet, packet) if prev_packet else 0.0
                        alt = packet.altitude()

                        state = detect_flight_state(
                            alt=alt,
                            vel=vel,
                            prev_vel=prev_vel,
                        )

                        table = make_flight_table(
                            t=packet.t,
                            alt=alt,
                            vel=vel,
                            state=state,
                            lat=last_lat,
                            lon=last_lon,
                        )

                        live.update(table)

                        prev_vel = vel
                        prev_packet = packet
                    else:
                        stati.reject(packet)


        print()  # finalize box before summary

    elif mode == "serial":
        print("Waiting for USB...")

        ports = find_ports()
        if not ports:
            return   

        if len(ports) == 1:
            port_name = ports[0].device
            print(f"Using {port_name}")
        else:
            try:
                choice = int(input("Select port number: "))
                port_name = ports[choice - 1].device
            except (ValueError, IndexError):
                print("Invalid port selection")
                return

        
        try:
            baud = int(input("Enter baudrate: "))
        except ValueError:
            print("Enter valid number")
            return

        seri = Serialize(port=port_name, baudrate=baud)

        
        try:
            seri.open()
        except RuntimeError:
            print(f"Access denied to {port_name}")
            return

        print("Serial link established. Waiting for data...")

        
        try:
            for packet in seri.packets():
                if packet.validate():
                    stati.accept(packet)
                    status = (
                            f"T={packet.t:6d} ms "
                            f"PRE={packet.pre:7.0f} Pa  "
                            f"AZ={packet.az:+6.2f} m/s²  "
                            f"LINK=OK"
                        )
                    
                    update_status_line(status)   # to update in realtime(not spamming)
                    
                    accepted_packets.append(packet)
                else:
                    stati.reject(packet)

        except KeyboardInterrupt:
            print("\nStopping Serial...")

        finally:
            seri.close()

    
    plot_instance = Plotter(accepted_packets)
    
    stati.summary()

    print("\n")
    print("=======================")
    print( " Generating Plots ...")
    print("=======================")
    print("\n \n")
    plot_instance.pre_vs_t()
    plot_instance.acc_mag_vs_t()
    plot_instance.alt_vs_t()
    plot_instance.vel_vs_t()


def make_flight_table(t, alt, vel, state, lat=None, lon=None):
    table = Table(
        title="VisualGS – Flight Monitor",
        expand=True,
        show_header=False,
        border_style="cyan"
    )

    table.add_column("Field", style="bold cyan", width=12)
    table.add_column("Value", style="white")

    table.add_row("Time (ms)", f"{t}")
    table.add_row("Altitude (m)", f"{alt:.1f}")
    table.add_row("Velocity (m/s)", f"{vel:+.2f}")
    table.add_row("State", f"[bold yellow]{state}[/]")

    if lat is not None and lon is not None:
        table.add_row("GPS", f"{lat:.5f}, {lon:.5f}")
    else:
        table.add_row("GPS", "---")

    return table


def csv_to_dict(row):
    try:
        return {
            "t": int(row[0]),
            "pre": float(row[1]),
            "ax": float(row[2]),
            "ay": float(row[3]),
            "az": float(row[4]),
            "lat": float(row[5]) if len(row) > 5 and row[5] else None,
            "lon": float(row[6]) if len(row) > 6 and row[6] else None,
        }
    except (ValueError, IndexError):
        return None


def compute_velocity(prev_packet, curr_packet):
    """
    Compute vertical velocity (m/s) from pressure-derived altitude.
    Uses two packets.
    """
    dt = (curr_packet.t - prev_packet.t) / 1000.0  # ms → s
    if dt <= 0:
        return 0.0

    h1 = prev_packet.altitude()
    h2 = curr_packet.altitude()

    return (h2 - h1) / dt


def detect_flight_state(alt, vel, prev_vel):
    """
    Determine flight state from altitude and vertical velocity.
    """

    # Tunable thresholds (keep conservative)
    VEL_EPS = 2.0      # m/s
    ALT_EPS = 5.0      # meters

    if alt < ALT_EPS and abs(vel) < VEL_EPS:
        return "LANDED"

    if vel > 20:
        return "BOOST"

    if vel > VEL_EPS and vel < prev_vel:
        return "COAST"

    if abs(vel) <= VEL_EPS:
        return "APOGEE"

    if vel < -VEL_EPS:
        return "DESCENT"

    return "IDLE"


def draw_flight_box():
    print("+------------------------------------------------------+")
    print("|              VISUALGS - FLIGHT MONITOR               |")
    print("+------------------------------------------------------+")
    print("| Time     :                                           |")
    print("| Altitude :                                           |")
    print("| Velocity :                                           |")
    print("| GPS      :                                           |")
    print("| State    :                                           |")
    print("|                                                      |")
    print("| Press Ctrl+C to stop                                 |")
    print("+------------------------------------------------------+")


def update_flight_box(t, alt, vel, state="---", lat=None, lon=None):
    gps = f"{lat:.5f}, {lon:.5f}" if lat is not None and lon is not None else "---"

    # Move cursor to the "Time" line
    sys.stdout.write("\033[8A")

    sys.stdout.write(f"| Time     : {t:8d} ms{' ' * 30}|\n")
    sys.stdout.write(f"| Altitude : {alt:8.1f} m{' ' * 31}|\n")
    sys.stdout.write(f"| Velocity : {vel:8.2f} m/s{' ' * 28}|\n")
    sys.stdout.write(f"| GPS      : {gps:<38}|\n")
    sys.stdout.write(f"| State    : {state:<10}{' ' * 29}|\n")

    sys.stdout.write("\033[2B")
    sys.stdout.flush()