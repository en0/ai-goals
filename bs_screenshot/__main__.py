import cv2
import numpy as np

from collections import deque
from bs import ScreenGrabber


def main() -> int:

    with ScreenGrabber() as g:
        img = g.grab_gray()
        while True:
            cv2.imshow(f"view", img)
            if cv2.waitKey(25) & 0xFF == ord("q"):
                cv2.destroyAllWindows()
                break

if __name__ == "__main__":
    main()
