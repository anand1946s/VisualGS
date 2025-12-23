import csv
from .packet import Packet
from .stati import Packetstat
from .plotter import Plotter
from .serialize import Serialize


def run_csv(mode = "csv",filepath = "dataset.csv"):
    stati = Packetstat()
    accepted_packets = []


    if mode == "csv" :
        with open(filepath, "r") as f:
            reader = csv.reader(f)
            next(reader)  # skip header
    
            for row in reader:
                data = csv_to_dict(row)

                if data is None:
                    print("reject: malformed row")
                    continue

                packet = Packet(
                    data["t"],
                    data["pre"],
                    data["ax"],
                    data["ay"],
                    data["az"]
                )

                if packet.validate():
                    #alti = packet.altitude()
                    #print(alti)
                    stati.accept(packet)
                    accepted_packets.append(packet)
                else:
                    print("reject")
                    stati.reject(packet)

    elif mode == "serial":
        print("Waiting for USB...")
        # next we implement cli to recieve com and baud grm  user
        seri = Serialize(port = "COM3",baudrate=9600)   
        try:
            seri.open()
        except RuntimeError:
            print("Access Denied to COM!!!")
            return
        
        for packet in seri.packets():
            if packet.validate():
                stati.accept(packet)
                accepted_packets.append(packet)
            else:
                stati.reject(packet)  
                #also this never stops.so need a mechanism to halt this after n sec of inactivity.     


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
