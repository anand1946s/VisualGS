import csv , time
from .packet import Packet
from .stati import Packetstat
from .plotter import Plotter
from .serialize import Serialize
from .serialize import find_ports , update_status_line


def run_csv(mode = "replay",filepath = "dataset.csv", speed = 1.0):
    stati = Packetstat()
    accepted_packets = []


    if mode == "replay" :
        prev_t = None
        prev_packet = None
        with open(filepath, "r") as f:
            reader = csv.reader(f)
            next(reader)  
    
            for row in reader:
                data = csv_to_dict(row)

                if data is None:  # for malformed packets , csv_to_dict returns empty list
                    stati.malformed()
                    
                    continue

                packet = Packet(data["t"],data["pre"],data["ax"],data["ay"],data["az"])

                if prev_t is not None:
                    dt = packet.t - prev_t
                    if dt >0:
                        time.sleep((dt/speed)/1000)
                prev_t = packet.t

                if packet.validate():
                    #alti = packet.altitude()
                    #print(alti)
                    stati.accept(packet)
                    accepted_packets.append(packet)

                    if prev_packet is not None:
                        vel = compute_velocity(prev_packet, packet)
                    else:
                        vel = 0.0

                    alt = packet.altitude()
                    status = (
                        f"T={packet.t:6d} ms | "
                        f"ALT={alt:7.1f} m | "
                        f"VEL={vel:+8.2f} m/s | "
                        "STATE=---"
                    )

                    update_status_line(status)
                    prev_packet = packet


                else:
                    #print("reject")
                    stati.reject(packet)

            print()

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
                            f"T={packet.t:6d} ms | "
                            f"PRE={packet.pre:7.0f} Pa | "
                            f"AZ={packet.az:+6.2f} m/s² | "
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


def csv_to_dict(row):
    try:
        return {
            "t": int(row[0]),
            "pre": float(row[1]),
            "ax": float(row[2]),
            "ay": float(row[3]),
            "az": float(row[4]),
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