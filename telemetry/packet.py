class Packet:
    def __init__(self,t,pre,ax,ay,az):
        self.t = t
        self.pre = pre
        self.ax = ax
        self.ay = ay
        self.az = az


    def validate(self):
        ok = True
        if self.t<0:
            ok = False
            self.error = "Neg time"

        if self.pre <0 :
            ok = False
            self.error = "Neg pressure"
        #if anything else to check
        return ok
    
    def altitude(self, p0=101325):
        return 44330 * (1 - (self.pre / p0) ** 0.1903)