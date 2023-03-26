# Detect edges of a maze -> https://www.mathsisfun.com/games/mazes.html

import cv2
import numpy as np

from collections import deque
from bs import ScreenGrabber


def main() -> int:
    with ScreenGrabber() as g:

        img = g.grab_gray()
        th, tw = img.shape
        hslice = [i for i in range(tw) if img[th//2, i] == 189]
        vslice = [i for i in range(th) if img[i, tw//2] == 189]
        xs, xe = hslice[0], hslice[-1]
        ys, ye = vslice[0], vslice[-1]

        img = img[ys:ye,xs:xe]
        th, tw = [int(x*0.5) for x in img.shape]
        img = cv2.resize(img, (tw, th))

        vlines, ts = find_vlines(img)
        hlines, _ = find_hlines(img)

        vlines.insert(0, 0)
        hlines.insert(0, 0)
        ts //= 2

        grid = np.zeros((len(hlines), len(vlines)), dtype="uint8")

        for gy, y in enumerate(hlines):
            for gx, x in enumerate(vlines):
                if img[y+ts, x+ts] == 189:
                    grid[gy, gx] = 1

        while True:
            cv2.imshow(f"view", grid)
            if cv2.waitKey(25) & 0xFF == ord("q"):
                cv2.destroyAllWindows()
                break


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
    for x, v in enumerate(vlines):
        cooldown = max(0, cooldown - 1)
        if v > p+20 and cooldown == 0:
            ret.append(x)
            cooldown = 3
        p = v

    if len(ret) % 2 != 0:
        ret = ret[:-1]

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
    for y, v in enumerate(lines):
        cooldown = max(0, cooldown - 1)
        if v > p+10 and cooldown == 0:
            ret.append(y)
            cooldown = 3
        p = v

    if len(ret) % 2 != 0:
        ret = ret[:-1]

    return fill_in_missing_lines(ret)


if __name__ == "__main__":
    main()
