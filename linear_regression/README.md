# Linear Regression AI

This is a really simply NN to find the weight and bias of a linear regression formula.

**The formula**

`y = x * w + b`

- x, y describes a point on plane.
- w is a weight that describes the slop of a line
- b is the bias describing the y intercept of the line

As shown above, y can be computed for any given x value using a predefined weight and bias.

This project will create a set of x and y values using some constant values for w and b. Then, we will
define a NN that implements the same formula but doesn't know the values of w and b. Then, using
training, we will fit the NN (find the values for w and b) using gradient descent and back
propagation built into pytorch.
