import matplotlib.pyplot as plt
import math

class Plotter:
    def __init__(self,packets):
        self.t = [p.t for p in packets]
        self.pre = [p.pre for p in packets]
        self.ax = [p.ax for p in packets]
        self.ay = [p.ay for p in packets]
        self.az = [p.az for p in packets]

        self.alt = [p.altitude() for p in packets]

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

    def alt_vs_t(self):
        plt.plot(self.t, self.alt)
        plt.xlabel("Time (ms)")
        plt.ylabel("Altitude (m)")
        plt.title("Altitude vs Time")
        plt.savefig("altitude_vs_time.png")
        plt.close()

    def vel_vs_t(self):
        vel = [0.0]
        for i in range(1, len(self.alt)):
            dt = (self.t[i] - self.t[i-1]) / 1000.0
            if dt <= 0:
                vel.append(0.0)
            else:
                vel.append((self.alt[i] - self.alt[i-1]) / dt)

        plt.plot(self.t, vel)
        plt.xlabel("Time (ms)")
        plt.ylabel("Vertical Velocity (m/s)")
        plt.title("Velocity vs Time")
        plt.savefig("velocity_vs_time.png")
        plt.close()

    def acc_mag_vs_t(self):
        plt.plot(self.t, self.acc_mag)
        plt.xlabel("Time (ms)")
        plt.ylabel("Acceleration Magnitude (m/s²)")
        plt.title("Acceleration Magnitude vs Time")
        plt.savefig("acc_mag_vs_time.png")
        plt.close()

