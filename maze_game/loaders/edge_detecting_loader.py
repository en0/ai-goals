import cv2
import numpy as np
from bs import ScreenGrabber, Vector2
from ..typing import MazeLoader, Maze, MazeFactory


def fill_in_missing_lines(lines):
    deltas = []
    last_v = 0
    for v in lines:
        deltas.append(v - last_v)
        last_v = v

    _lines = []
    tg = sorted(deltas)[len(deltas)//2]

    f = 0
    for i, (d, v) in enumerate(zip(deltas, lines)):
        if d - tg < tg:
            _lines.append(v)
            continue
        for _ in range(1, round(d/tg)):
            _lines.append(_lines[-1] + tg)
        _lines.append(v)
    return _lines, tg


def find_vlines(img):

    imgl = cv2.filter2D(img, -1, np.array([
        [1, 0, -1],
        [2, 0, -2],
        [1, 0, -1],
    ]))
    imgr = cv2.filter2D(img, -1, np.array([
        [-1, 0, 1],
        [-2, 0, 2],
        [-1, 0, 1],
    ]))

    vlines = [0] * img.shape[1]
    for y, row in enumerate(img):
        for x, _ in enumerate(row):
            try:
                if all([
                    imgl[i+y, x] == 255
                    for i in range(-2, 2)
                ]) or all([
                    imgr[i+y, x] == 255
                    for i in range(-2, 2)
                ]):
                    vlines[x] += 1
            except:
                pass

    ret = []
    p = 0
    cooldown = 0
    last_tw = 0
    for x, v in enumerate(vlines):
        cooldown = max(0, cooldown - 1)
        if v > p+20 and cooldown == 0:
            ret.append(x)
            cooldown = last_tw // 3
            last_tw = 0
        else:
            last_tw += 1
        p = v

    #if len(ret) % 2 != 0:
        #ret = ret[:-1]

    return fill_in_missing_lines(ret)


def find_hlines(img):

    imgt = cv2.filter2D(img, -1, np.array([
        [1, 2, 1],
        [0, 0, 0],
        [-1, -2, -1],
    ]))
    imgb = cv2.filter2D(img, -1, np.array([
        [-1, -2, -1],
        [0, 0, 0],
        [1, 2, 1],
    ]))

    lines = [0] * img.shape[0]
    for y, row in enumerate(img):
        for x, _ in enumerate(row):
            try:
                if all([
                    imgt[y, i+x] > 200
                    for i in range(-2, 2)
                ]) or all([
                    imgb[y, i+x] > 200
                    for i in range(-2, 2)
                ]):
                    lines[y] += 1
            except:
                pass

    ret = []
    p = 0
    cooldown = 0
    last_tw = 0
    for y, v in enumerate(lines):
        cooldown = max(0, cooldown - 1)
        if v > p+10 and cooldown == 0:
            ret.append(y)
            cooldown = last_tw // 2
            last_tw = 0
        else:
            last_tw += 1
        p = v

    if len(ret) % 2 != 0:
        ret = ret[:-1]

    return fill_in_missing_lines(ret)


class EdgeDetectingMazeLoader(MazeLoader):
    """Load a maze from a screen shot and use edge-detection to find build the maze"""

    def __init__(self, screen: ScreenGrabber, factory: MazeFactory):
        self._screen = screen
        self._factory = factory

    def load(self) -> Maze:
        img = self._screen.grab_gray()

        # Find the map in the screen capture
        th, tw = img.shape
        hslice = [i for i in range(tw) if img[th//2, i] == 189]
        vslice = [i for i in range(th) if img[i, tw//2] == 189]
        xs, xe = hslice[0], hslice[-1]
        ys, ye = vslice[0], vslice[-1]
        img = img[ys:ye,xs:xe]

        # Make the image smaller to speed things up
        th, tw = [int(x*0.5) for x in img.shape]
        img = cv2.resize(img, (tw, th))

        # Find all the vertical and horizontal lines.
        vlines, ts = find_vlines(img)
        hlines, _ = find_hlines(img)

        # Push in a leading edge to simply the math.
        vlines.insert(0, 0)
        hlines.insert(0, 0)

        # Compute the step-width as half the tile size.
        ts //= 2

        #for x in vlines:
        #    img[:, x] = 0
        #for y in hlines:
        #    img[y, :] = 0

        #while True:
        #    cv2.imshow(f"img", img)
        #    if cv2.waitKey(25) & 0xFF == ord("q"):
        #        cv2.destroyAllWindows()
        #        break

        # Fill a grid by checking the center pixel of each tile.
        grid = np.zeros((len(hlines), len(vlines)), dtype="uint8")
        for gy, y in enumerate(hlines):
            for gx, x in enumerate(vlines):
                if img[y+ts, x+ts] == 189:
                    grid[gy, gx] = 1

        th, tw = grid.shape
        return self._factory.create(grid, Vector2(1, 1), Vector2(tw-2, th-2))

