from collections import deque
from time import time_ns

class Clock:

    def __init__(self):
        self._enter = time_ns()
        self._deltas = deque(maxlen=50)
        self._accum = 0

    def tick(self) -> int:
        e = time_ns()
        r = e - self._enter
        self._deltas.append(r)
        self._enter = e
        return r

    def get_average_tps(self) -> float:
        if self._deltas:
            return 1000000000 / (sum(self._deltas) / len(self._deltas))
        return 0

    def tick_and_show(self) -> int:
        """Calls tick() and prints the TPS every 1 second."""
        val = self.tick()
        self._accum += val
        if self._accum >= 1000000000:
            self._accum = 0
            print("fps:", self.get_average_tps())
        return val


