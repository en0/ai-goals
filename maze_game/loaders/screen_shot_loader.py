import cv2
from bs import ScreenGrabber, Vector2
from ..typing import MazeLoader, Maze, MazeFactory


class ScreenShotMazeLoader(MazeLoader):
    """Load a maze from a screen shot"""

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
        dy, dx = ye-ys, xe-xs

        # Adjust capture size to be perfectly divisible by the tilesize
        img = img[ys:ye,xs:xe]

        # Aproximate the tilesize
        state = "initial"
        for tilesize in range(min(th, tw)):
            if state == "initial" and img[tilesize//2, tilesize] == 189:
                state = "identify"
            elif state == "identify" and img[tilesize//2, tilesize] > 200:
                break

        # Downsize the image to make grid detection easier
        th, tw = [x//tilesize for x in img.shape]
        img = cv2.resize(img, (tw, th), 0, 0, interpolation=cv2.INTER_NEAREST_EXACT)

        # Convert to a map
        grid = [[1 if c == 189 else 0 for c in row] for row in img]
        return self._factory.create(grid, Vector2(1, 1), Vector2(tw-2, th-2))

