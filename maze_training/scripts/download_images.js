/*
 * I used this script to download a few thousand mazes from the mathisfun website.
 * That website uses client side code to generate mazes. It would probably be better
 * to reverse the drawMaze() function and understand how the maze[] array is structured
 * but, i couldn't be bothered. This code hijacks the existing code and simply saves the
 * output canvas as a png to your downloads directory.  Post processing will be needed.
 * REF: https://www.mathsisfun.com/measure/mazes.html
 */

for (var i = 0; i < 1000; i++) {
    g.reset();
    generateMaze();
    drawMaze();
    window.location=g.canvas.toDataURL('image/png').replace("image/png", "image/octet-stream");
}
