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

        vlines = {}
        for x in find_vlines(img):
            img[:,x] = 0

        for y in find_hlines(img):
            img[y,:] = 0


        while True:
            cv2.imshow(f"view", img)
            if cv2.waitKey(25) & 0xFF == ord("q"):
                cv2.destroyAllWindows()
                break


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
    return ret


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
    return ret


if __name__ == "__main__":
    main()
