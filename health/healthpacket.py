import csv
from telemetry.serialize import Serialize

class Healthpacket:
    def __init__(self,time,imu,sd,gps):
        self.time = time
        self.imu = imu
        self.sd = sd
        self.gps = gps

    def to_csv(self):
        return [
            self.time,
            int(self.imu),
            int(self.sd),
            int(self.gps),
        ]
    
def process_health(port,baudrate,path = "health.csv"):
    seri = Serialize(port,baudrate)

    try:
        seri.open()
    except RuntimeError:
        print("Access Denied to COM")
        return
    
    f = open(path,"w")
    writer = csv.writer(f)
    writer.writerow(["time_ms", "imu", "sd", "gps"])

    try:
        for line in seri.packets():
            if not line.startswith("HEALTH"):
                continue

            if len(parts) != 5:
                continue

            parts = line.split(",")

            try:
                packet = Healthpacket(time=int(parts[1]),imu = bool(int(parts[2])), sd = bool(int(parts[3])), gps = bool(int(parts[4])))

            except ValueError:
                continue

            writer.writerow(packet.to_csv())
            f.flush()

    except KeyboardInterrupt:
        print("Health processing stopped")

    finally:
        f.close()
        seri.close()