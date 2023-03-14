# Maze Game

This is the first task I gave myself. It's not really AI, just a POC for the screengrab and sendkeys
classes. Running it is a bit of work.

## Setup the Viewport

First, open your browser to [mathsisfun](https://www.mathsisfun.com/games/mazes.html) and start a
new `easy` puzzle. Put it on the screen where you can see it completely.

With the webpage visible, run the following command from within the project directory.

```bash
source venv/bin/activate
python3 -m bs_screenshot/draw_bbox.py
```

You are going to see a cv2 window pop up. It's probably pretty small. Use the arrow keys to locate
the edge of the maze. Be exact on the edge of the maze, not the window, the maze itself.

Once ou get the top, left corner where it needs to be, tap the space bar to switch the draw_bbox
program to resize mode. Use the arrow keys to grow or shring the window to encompase the entire
maze. Once again, be exact. Note, you can tap space again to go back to move mode.

Once you have it perfect, hit enter then q. You will see a tuple in the terminal.
Something like this:

```
(553, 391, 1978, 1132)
```

Put that tuple on line 12 of `maze_game/__main__.py`. It should look like this:

```python
VIEWPORT: Rect = (553, 391, 1978, 1132)
```

If you move the browser window at all, you will get to enjoy that experience all over again.

## Solve a maze

Ok, with the browser window visible and the maze ready to take input, run the following:

```bash
source venv/bin/activate
python -m maze_game
```

Then click on the browser window to give it focus.

## Notes

My next goal is to make this code work with different sizes of mazes. After that, i will make it
find the maze from a full screen capture. Babysteps :)

