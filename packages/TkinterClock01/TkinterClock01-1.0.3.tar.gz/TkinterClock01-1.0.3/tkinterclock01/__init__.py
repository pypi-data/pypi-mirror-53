from omegamath01 import OmegaMath01 as h
name="TkinterClock01"

class Clock:
    def __init__(self,name):
        self.ad=h.Func.Clock(str(name)+"'s Clock")
        self.ad.run_time()
    def destroy(self):
        self.ad.kill()
        
