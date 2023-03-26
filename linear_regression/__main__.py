import torch
from matplotlib import pyplot as plt
from torch import nn
from torch import optim


# Basic Linear regresion
lr = lambda x, w, b: x * w + b


class LinearRegresion(nn.Module):
    """A model to compute the linear regresion of an unknown slope and offset"""

    def __init__(self) -> None:
        super().__init__()
        self.weights = nn.Parameter(torch.rand(1, dtype=torch.float))
        self.bias = nn.Parameter(torch.rand(1, dtype=torch.float))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return lr(x, self.weights, self.bias)


def show_plot(
    x_train: torch.Tensor, y_train: torch.Tensor,
    x_test: torch.Tensor, y_test: torch.Tensor,
    prediction: torch.Tensor = None
) -> None:
    """Visualize the accuracy of the given predictions against the training and test data."""
    plt.scatter(x_train, y_train, c="blue", label="training data")
    plt.scatter(x_test, y_test, c="green", label="testing data")
    if prediction is not None:
        if prediction.requires_grad:
            prediction = prediction.detach()
        plt.scatter(x_test, prediction, c="red", label="testing data")
    plt.legend(loc="upper left")
    plt.show()


def main():

    # These are the values we want the model to learn.
    weight, bias = 0.4, 0.2

    # Create training and testing sets
    x_values = torch.arange(0, 1, step=0.01)
    y_values = lr(x_values, weight, bias)

    # Separate training and testing values
    train_index = int(len(x_values) * .8)
    x_train, y_train = x_values[:train_index], y_values[:train_index]
    x_test, y_test = x_values[train_index:], y_values[train_index:]

    # Create model and training functions
    model = LinearRegresion()
    criterion = nn.MSELoss()
    optimizer = optim.SGD(model.parameters(), lr=0.3)

    # Train the model
    for _ in range(10000):
        optimizer.zero_grad()
        prediction = model(x_test)
        loss = criterion(prediction, y_test)
        loss.backward()
        optimizer.step()

    # Show results
    print(f"Weight: Target={weight}, Actual={model.weights.data}")
    print(f"Bias: Target={bias}, Actual={model.bias.data}")
    show_plot(x_train, y_train, x_test, y_test, prediction)


if __name__ == "__main__":
    main()
