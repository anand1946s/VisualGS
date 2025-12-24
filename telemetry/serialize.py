import serial
from .packet import Packet  

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
    