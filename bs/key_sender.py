from evdev import UInput, ecodes
from time import sleep
from typing import List, Union, Tuple


class KeySender:

    def __init__(self, delay: float = 0):
        self._uinput = UInput()
        self._delay = delay or 0.01

    def close(self):
        self._uinput.syn()
        self._uinput.close()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()

    def send(self, key: Union[int, List[int]]) -> None:
        keys = key if isinstance(key, list) else [key]
        for k in keys:
            self._uinput.write(ecodes.EV_KEY, k, 1)
            sleep(self._delay)
        for k in keys:
            self._uinput.write(ecodes.EV_KEY, k, 0)
            sleep(self._delay)

    def send_many(self, keys: List[Union[int, List[int]]]) -> None:
        for k in keys:
            self.send(k)
