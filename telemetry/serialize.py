import serial , sys , time 
from serial.tools import list_ports
from .packet import Packet  



_last_ui_update = 0.0   


class Serialize:
    def __init__(self,port,baudrate = 9600, timeout=1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = None

    def open(self):
        try:
            self.ser = serial.Serial(self.port,self.baudrate,timeout = self.timeout)

        except serial.SerialException as e:
            self.ser = None
            raise RuntimeError(f"Access Denied for Port {self.port}: {e}")
        
    def close(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
    def packets(self):
        if self.ser is None:
            raise RuntimeError("Serial port not opened")
        
        try:
            while True:
                raw = self.ser.readlines()

                if not raw:
                    continue  # timeout, no data

                try:
                    line = raw.decode("utf-8").strip()
                except UnicodeDecodeError:
                    continue

                if not line:
                    continue

                yield line

        finally:
            self.close()

def find_ports():
    ports = list(list_ports.comports())

    if not ports:
        print("No serial devices detected.")
        return []

    print("Available serial ports:")
    for i, port in enumerate(ports, start=1):
        desc = port.description if port.description else "Unknown device"
        print(f"  [{i}] {port.device} — {desc}")

    return ports
    

def update_status_line(text, min_interval=0.1):
    
        global _last_ui_update
        now = time.time()
        if now - _last_ui_update < min_interval:
            return
        _last_ui_update = now

        sys.stdout.write("\r" + text)
        sys.stdout.flush()   