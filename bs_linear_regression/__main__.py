import torch
from matplotlib import pyplot as plt
from collections import deque
from torch import nn
from torch import optim
from typing import List, Callable, Tuple
from functools import partial


# Basic Linear regresion
lr = lambda x, w, b: x * w + b


class LinearRegresion(nn.Module):
    """A model to compute the linear regresion of an unknown slope and offset"""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
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


def train_and_evaluate(
    model: nn.Module,
    loss_fn: Callable[[torch.Tensor, torch.Tensor], torch.Tensor],
    optimizer: optim.Optimizer,
    training_input: torch.Tensor,
    training_target: torch.Tensor,
    testing_input: torch.Tensor,
    testing_target: torch.Tensor,
    epoch: int,
) -> Tuple[torch.Tensor, torch.Tensor]:
    """This function implements a single train and test step for the given model.

    This function should be called once for each epoch of training.

    Arguments:
        model: The model to train.
        loss_fn: The loss function to use for training and evaluation.
        optimizer: The optimizer that implements a gradient descent.
        training_input: A tensor of training inputs.
        training_target: A tensor of training targets.
        testing_input: A tensor of testing inputs used for evaluation.
        testing_target: A tensor of testing targets used for evaluation.
        epoch: An integer identifying the epoch used in logging.

    Returns: A tuple with 2 members
        0: The result of the loss function after the training step.
        1: The result of the loss function after the testing step.
    """

    model.train()

    training_output = model(training_input)
    training_loss = loss_fn(training_output, training_target)

    optimizer.zero_grad()
    training_loss.backward()
    optimizer.step()

    model.eval()
    with torch.inference_mode():
        testing_output = model(testing_input)
        testing_loss = loss_fn(testing_output, testing_target)

    if epoch % 10 == 0:
        print(f"LOSS: {training_loss}/{testing_loss}")

    return (
        training_loss.detach(),
        testing_loss.detach()
    )


def create_data(
    weight: float,
    bias: float,
    step: float = 0.01
) -> Tuple[torch.Tensor, torch.Tensor]:
    """Generate data for this experiment.

    This function generates a range of data as X. Then, generates the corresponding
    Y values for each generated X using the standard linear regresion algorithm.

    Arguments:
        weight: The slope of the target LR function.
        bias: The y-intercept of the target LR function.
        step: The partial step to use when generating the range of x values.

    Returns: A tuple containing 2 members.
        0: The inputs (x values)
        1: The targets (y values)
    """
    inputs = torch.arange(0, 1, step=step)
    return inputs, lr(inputs, weight, bias)


def split_for_training(
    inputs: torch.Tensor,
    targets: torch.Tensor,
    factor: float = 0.8
) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
    """Linearly split data into training and testing parts.

    Arguments:
        inputs: A tensor suitable for input data.
        targets: A tensor representing the expected outputs for the given inputs.
        factor: A float specifing the ratio of training to testing data (split).

    Returns: A tuple containing 4 members.
        0: The inputs for training.
        1: The targets for training.
        2: The inputs for testing.
        3: The targets for testing.
    """
    index = int(len(inputs) * .8)
    training_inputs, training_targets = inputs[:index], targets[:index]
    testing_inputs, testing_targets = inputs[index:], targets[index:]
    return (
        training_inputs, training_targets,
        testing_inputs, testing_targets
    )

def main():

    # For perdictability, we would like the randomness to be less random.
    torch.manual_seed(42)

    epochs = 200 # the number of training steps
    weight, bias = 0.4, 0.2 # These are the values our model is searching for.
    model = LinearRegresion() # Our model to train.

    x_values, y_values = create_data(weight, bias)
    x_train, y_train, x_test, y_test = split_for_training(x_values, y_values)

    # Wrap the train_and_evaluate function with a partial to simplify calling later.
    trainer = partial(
        train_and_evaluate,
        model,
        nn.L1Loss(), # Mean Absolute Error (MAE) loss function.
        optim.SGD(model.parameters(), lr=0.01), # Stochastic (random) gradient descent.
        x_train, y_train,
        x_test, y_test
    )

    # Train and evalute the model, collect results so we can plot them.
    results = [trainer(x) for x in range(epochs)]

    # Show training loss correction
    plt.plot(list(results))
    plt.show()

    # Show predictions
    print(f"Weight: Target={weight}, Actual={model.weights.data}")
    print(f"Bias: Target={bias}, Actual={model.bias.data}")
    with torch.inference_mode():
        show_plot(x_train, y_train, x_test, y_test, model(x_test))


if __name__ == "__main__":
    main()
