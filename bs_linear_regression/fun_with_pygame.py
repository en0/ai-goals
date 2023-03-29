import pygame as pg
import torch as pt
import numpy as np


FRAMERATE = 60
HEIGHT = 800
WIDTH = 600
SIZE = HEIGHT, WIDTH

WEIGHT = 0.3
BIAS = 0.7
LR = lambda x, w, b: x * w + b


class LinearRegresionModel(pt.nn.Module):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layer = pt.nn.Linear(in_features=1, out_features=1)

    def forward(self, x: pt.Tensor) -> pt.Tensor:
        return self.layer(x)


class Game:

    def __init__(self):
        self.screen = pg.display.set_mode(SIZE)
        self.clock = pg.time.Clock()
        self.frame_delta = 1
        self.playing = False
        self.font = pg.font.Font(size=50)
        self.train_outputs = None
        self.test_outputs = None
        self.hud = ["loading..."]

        self.model = LinearRegresionModel()
        self.loss = pt.nn.L1Loss()
        self.optim = pt.optim.SGD(self.model.parameters(), lr=0.005)

        inputs = pt.arange(0, 1, step=0.01).unsqueeze(1)
        targets = LR(inputs, WEIGHT, BIAS)
        index = int(len(inputs) * 0.8)
        self.train_inputs = inputs[:index]
        self.train_targets = targets[:index]
        self.test_inputs = inputs[index:]
        self.test_targets = targets[index:]

    def _train_model_step(self):

        self.model.train()

        train_outputs = self.model(self.train_inputs)
        train_loss = self.loss(train_outputs, self.train_targets)
        self.hud.append(f"Training Loss: {train_loss.squeeze().item():.4f}")
        self.train_outputs = train_outputs.detach()

        self.optim.zero_grad()
        train_loss.backward()
        self.optim.step()

        self.model.eval()
        with pt.inference_mode():
            test_outputs = self.model(self.test_inputs)
            test_loss = self.loss(test_outputs, self.test_targets)
            self.hud.append(f"Testing Loss: {test_loss.squeeze().item():.4f}")
            self.test_outputs = test_outputs.detach()

    def _render_points(self, xs, ys, color):
        for point in np.interp(np.concatenate((xs, ys), axis=1), [0, 1], [0, WIDTH]):
            x, y = point
            pg.draw.circle(self.screen, color, (x+100, HEIGHT-y), radius=4)

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.playing = False
            elif event.type == pg.KEYUP and event.key == pg.K_q:
                self.playing = False

    def update(self):
        self.frame_delta = self.clock.tick(FRAMERATE)
        self.hud = [f"fps: {self.clock.get_fps():.2f}"]
        self._train_model_step()

    def render(self):
        self.screen.fill("black")
        self._render_points(self.train_inputs, self.train_targets, "blue")
        self._render_points(self.test_inputs, self.test_targets, "green")
        self._render_points(self.test_inputs, self.test_outputs, "red")
        for i, hud in enumerate(self.hud):
            self.screen.blit(self.font.render(hud, True, "blue"), (10, i * 50 + 10))
        pg.display.flip()

    def run(self):
        self.playing = True
        while self.playing:
            self.check_events()
            self.update()
            self.render()
        pg.quit()


if __name__ == "__main__":
    pt.manual_seed(2)
    pg.font.init()
    game = Game()
    game.run()
