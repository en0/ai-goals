# AI Goals

Just playing around with bots.

This is just some hacked together stuff to play around with bots that play games through the same
interface as humans do.  Screen grabs, keystrokes, and mouse clicks. Just seeing what I can do.

## Quick start

Create a virtual environment and install the requirements

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

To do anything useful, go poke through the subdirectories (like `maze_game`).

## Explaination of Project

This project is a ordered set of goals directed some friends that are experts in the industry. The
meta-goal is simply, learn more about deep learning.

## The plan

The intent is to build bots the play some games. However, i will need to bounce inbetween some of
these projects to build skills in each area.

### Mazes Part 1

Play maze games using classical programming.

1. Get screen captures working so i can feed images into the bot.
2. Get keyboard output working so the bot can feed commands into the game.

### Flappy Bird

Play flappy bird using NICE (NN + GA without gradient or backprop)

1. Learn pytorch.nn
2. get xp with NN

### Mazes Part 2

Play mazes using genetic algorithm

1. Refamiliarize myself with GA
2. Make the maze program more interesting.


### Mazes Part 3

Make a NN to play a maze using Flood Fill metrics. This will require that i pre-process the
iamge into a concrete map.

1. Learn how to use pytorch tensors and models
2. Learn how to save and load models

### Mazes Part 4

Make a NN to generate maze grids. I don't know this is possible but i was adivsed i would
learn alot about image processing and convolution networks.

1. Learn how to create tensors from image data.
2. Learn how Convolution network are structured.
3. learn how to deal with probabilistic output to generate concrete results.

## Folders

Each folder is intended to be a peice of my learning.
note: bs stands for baby-steps.

- `bs_screenshot` is a test ground for doing screen shots.
- `bs_sendkey` is a test ground for doing keystroke stuff.
- `bs_mouse` is a test ground for doing mouse stuff.
- `bs_edge_detection` is a test ground for some edge detection stuff.
- `bs` is a set of classes i created from the *bs* test grounds.
- `linear_regression` is a hello-world of NN.
- `maze_game` is the maze bot.

