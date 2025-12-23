import csv
from .packet import Packet
from .stati import Packetstat
from .plotter import Plotter


def run_csv(filepath="dataset.csv"):
    stati = Packetstat()
    accepted_packets = []

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
                alti = packet.altitude()
                print(alti)
                stati.accept(packet)
                accepted_packets.append(packet)
            else:
                print("reject")
                stati.reject(packet)

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
