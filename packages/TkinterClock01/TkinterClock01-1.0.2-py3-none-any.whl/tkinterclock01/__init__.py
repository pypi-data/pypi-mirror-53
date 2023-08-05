from omegamath01 import OmegaMath01 as h
name="TkinterClock01"

class Clock:
    def __init__(self,name):
        ad=h.Func.Clock(str(name)+"'s Clock")
        ad.run_time()
