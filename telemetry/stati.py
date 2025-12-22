class Packetstat:
    def __init__(self):
        self.total = 0
        self.accepted = 0
        self.rejected = 0
        self.errors = []

    def accept(self):
        self.total+=1
        self.accepted+=1

    def reject(self):
        self.total+=1
        self.rejected+=1
        self.errors.append("reject")

    def summary(self):
        print("\n--- Packet Statistics ---")
        print(f"Total     : {self.total}")
        print(f"Accepted  : {self.accepted}")
        print(f"Rejected  : {self.rejected}")