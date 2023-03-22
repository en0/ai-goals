import cv2
import numpy as np
from hashlib import sha256
from os import listdir
from os.path import join as join_path, dirname

from bs import Vector2


def find_columns(img):

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

    if len(ret) % 2 != 0:
        ret = ret[:-1]

    return ret


def find_rows(img):

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

    return ret


def load_maze(path: str) -> np.array:
    raw = cv2.imread(path)
    img = cv2.cvtColor(raw, cv2.COLOR_RGB2GRAY)
    th, tw = img.shape
    hslice = [i for i in range(tw) if img[th//3, i] == 192]
    vslice = [i for i in range(th) if img[i, tw//3] == 192]
    xs, xe = hslice[0], hslice[-1]
    ys, ye = vslice[0], vslice[-1]
    img = img[ys:ye,xs:xe]
    raw = raw[ys:ye,xs:xe]
    img = cv2.GaussianBlur(img, (5, 5), 0)
    mask = np.zeros_like(img)
    mask[img == 192] = 255
    img = cv2.bitwise_and(img, mask)
    return img, raw


def find_test_points(img):
    columns = find_columns(img)
    rows = find_rows(img)
    return (
        [sx + round((ex - sx) / 2) for sx, ex in zip([0] + columns, columns + [img.shape[1]-1])],
        [sy + round((ey - sy) / 2) for sy, ey in zip([0] + rows, rows + [img.shape[0]-1])]
    )


def img2grid(img, xtp, ytp) -> np.array:
    # Walls are 1, spaces are 0
    grid = np.zeros((len(ytp), len(xtp)), dtype='uint8')
    for y, ty in enumerate(ytp):
        for x, tx in enumerate(xtp):
            grid[y, x] = 255 if img[ty, tx] != 0 else 0
    return grid


def show_img(img):
    while True:
        cv2.imshow('Maze', img)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break


def main():

    # !!! All the mazes we are using to train are the same size. !!!

    rawdir = join_path(dirname(__file__), "data", "raw")
    griddir = join_path(dirname(__file__), "data", "grids")
    mazedir = join_path(dirname(__file__), "data", "mazes")
    image_paths = [join_path(rawdir, p) for p in listdir(rawdir)]

    # Process the first image to collect some common features.
    img, raw = load_maze(image_paths[0])
    x_test_points, y_test_points = find_test_points(img)
    target = Vector2(len(x_test_points) - 2, len(y_test_points) - 2)

    ## Test area
    #grid = img2grid(img, x_test_points, y_test_points)
    #hash = sha256(grid.view(dtype='uint8')).hexdigest()
    #print(hash)
    #show_img(raw)
    #show_img(img)
    #show_img(grid)

    for i, p in enumerate(image_paths):
        img, raw = load_maze(p)
        grid = img2grid(img, x_test_points, y_test_points)
        hash = sha256(grid.view(dtype='uint8')).hexdigest()
        maze_name = join_path(mazedir, f"{hash}.png")
        grid_name = join_path(griddir, f"{hash}.npy")
        print("Saving image data", grid_name)
        cv2.imwrite(maze_name, raw)
        np.save(grid_name, grid, allow_pickle=False)


if __name__ == "__main__":
    main()


