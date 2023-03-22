# I after downloading canvas images, my browser named all these things as 'download (n)'.
# I wanted to orginize this a bit more so i renamed all the files using this script:
# This is just hacky and i did it in the repl.
# These files where the only thing i had in my download directory

import os, os.path
DOWNLOAD=os.path.join(os.environ["HOME"], "Downloads")
for i, p in enumerate(os.listdir("DOWNLOAD")):
    os.rename(os.path.join(DOWNLOAD, p), os.path.join(DOWNLOAD, f'maze.{i:04}'))

# Then, i just moved everything into this projects data/raw directory

