import cv2
import numpy as np
from mss import mss
from .typing import Rect


class ScreenGrabber:

    def __init__(self, bbox: Rect = None):
        self._bbox = bbox
        self._sct = mss()
        if self._bbox is None:
            self._bbox = self._sct.monitors[0]

    def close(self):
        self._sct.close()

    def grab(self) -> np.array:
        img = self._sct.grab(self._bbox)
        return np.asarray(img)

    def grab_gray(self) -> np.array:
        img = self._sct.grab(self._bbox)
        img = np.asarray(img)
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()

