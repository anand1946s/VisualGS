class Packetstat:
    def __init__(self):
        self.fa = open("accept.csv","w")
        self.fr = open("reject.csv","w")
        

        self.fa.write("t,pre,ax,ay,az\n")
        self.fr.write("t,pre,ax,ay,az\n")

        self.total = 0
        self.accepted = 0
        self.rejected = 0
        self.malform = 0
        self.errors = []

    def accept(self,packet):
        self.total+=1
        self.accepted+=1

        self.fa.write(f"{packet.t},{packet.pre},{packet.ax},{packet.ay},{packet.az}\n")

    def reject(self,packet):
        self.total+=1
        self.rejected+=1

        self.fr.write(f"{packet.t},{packet.pre},{packet.ax},{packet.ay},{packet.az},{packet.error}\n")
        self.errors.append("reject")

    def malformed(self):
        self.total+=1
        self.malform +=1


    def close(self):
        self.fa.close()
        self.fr.close()

    def summary(self):
        print("\n--- Packet Statistics ---")
        print(f"Total     : {self.total}")
        print(f"Accepted  : {self.accepted}")
        print(f"Rejected  : {self.rejected}")
        print(f"Malformed : {self.malform}")