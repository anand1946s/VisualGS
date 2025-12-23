import matplotlib.pyplot as plt
import math

class Plotter:
    def __init__(self,packets):
        self.t = [p.t for p in packets]
        self.pre = [p.pre for p in packets]
        self.ax = [p.ax for p in packets]
        self.ay = [p.ay for p in packets]
        self.az = [p.az for p in packets]

        self.acc_mag = [
            math.sqrt(x*x + y*y + z*z)
            for x, y, z in zip(self.ax, self.ay, self.az)
        ]


    def pre_vs_t(self):
        plt.plot(self.t,self.pre)
        plt.xlabel("Time(ms)")
        plt.ylabel("Pressure")
        plt.title("Pressure vs Time")
        plt.savefig("pressure_vs_time.png")
        plt.close()


