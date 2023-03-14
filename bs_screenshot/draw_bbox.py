import cv2
import numpy as np
from mss import mss
from typing import Tuple, Dict


def main() -> int:
    bbox = (0, 0, 100, 100)
    #bbox = (553, 391, 1978, 1132)

    movers = [
        lambda _bbox: (_bbox[0], _bbox[1]-1, _bbox[2], _bbox[3]-1),
        lambda _bbox: (_bbox[0], _bbox[1]+1, _bbox[2], _bbox[3]+1),
        lambda _bbox: (_bbox[0]-1, _bbox[1], _bbox[2]-1, _bbox[3]),
        lambda _bbox: (_bbox[0]+1, _bbox[1], _bbox[2]+1, _bbox[3]),
    ]

    sizers = [
        lambda _bbox: (_bbox[0], _bbox[1], _bbox[2], _bbox[3]-1),
        lambda _bbox: (_bbox[0], _bbox[1], _bbox[2], _bbox[3]+1),
        lambda _bbox: (_bbox[0], _bbox[1], _bbox[2]-1, _bbox[3]),
        lambda _bbox: (_bbox[0], _bbox[1], _bbox[2]+1, _bbox[3]),
    ]

    fns = movers

    with mss() as g:
        while True:
            img = g.grab(bbox)
            img = np.asarray(img)
            cv2.imshow("ScreenGrabber Benchmark", img)
            k = cv2.waitKey(25)

            if k == 82:
                # up
                bbox = fns[0](bbox)
            elif k == 84:
                # down
                bbox = fns[1](bbox)
            elif k == 81:
                # right
                bbox = fns[2](bbox)
            elif k == 83:
                # left
                bbox = fns[3](bbox)
            elif k == 32:
                # space
                fns = movers if fns == sizers else sizers
                print("Activate Movers" if fns == movers else "Activate Sizers")
            elif k == 13:
                # Enter
                print(bbox)
            elif k & 0xFF == ord("q"):
                cv2.destroyAllWindows()
                break
            elif k != -1:
                print(k)


if __name__ == "__main__":
    main()
