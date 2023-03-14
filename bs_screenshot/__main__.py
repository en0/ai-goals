import cv2

from perf import Clock
from bs import ScreenGrabber


def main() -> int:
    mon = (0, 0, 2560, 1600)
    c = Clock()

    with ScreenGrabber(mon) as g:
        while True:
            img = g.grab()
            cv2.imshow("ScreenGrabber Benchmark", img)
            if cv2.waitKey(25) & 0xFF == ord("q"):
                cv2.destroyAllWindows()
                break
            c.tick_and_show()


if __name__ == "__main__":
    main()
