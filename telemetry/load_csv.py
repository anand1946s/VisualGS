import csv , time
from .packet import Packet
from .stati import Packetstat
from .plotter import Plotter
from .serialize import Serialize


def run_csv(mode = "replay",filepath = "dataset.csv", speed = 1.0):
    stati = Packetstat()
    accepted_packets = []


    if mode == "replay" :
        prev_t = None
        with open(filepath, "r") as f:
            reader = csv.reader(f)
            next(reader)  # skip header
    
            for row in reader:
                data = csv_to_dict(row)

                if data is None:
                    print("reject: malformed row")
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

                    #print(f"time={packet.t} ms | pre={packet.pre} Pa | ax={packet.ax} | ay={packet.ay} | az={packet.az}")


                else:
                    print("reject")
                    stati.reject(packet)

    elif mode == "serial":
        print("Waiting for USB...")
        # next we implement cli to recieve com and baud grm  user
        com = input("Enter COM No: ")
        try:
            baud = int(input("Enter baudrate"))
        except ValueError:
            print("Enter valid number")
            return

        seri = Serialize(port = f"COM{com}",baudrate=baud)   
        try:
            seri.open()
        except RuntimeError:
            print("Access Denied to COM!!!")
            return
        
        try:
            for packet in seri.packets():
                if packet.validate():
                    stati.accept(packet)
                    accepted_packets.append(packet)
                else:
                    stati.reject(packet)  
             
        except KeyboardInterrupt:
            print("Stopping Serial...")
        finally:
            seri.close()   


    plot_instance = Plotter(accepted_packets)
    plot_instance.pre_vs_t()
    stati.summary()


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
