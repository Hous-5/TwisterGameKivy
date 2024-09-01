from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, PushMatrix, Rotate, PopMatrix
from src.constants import GAME_WIDTH, GAME_HEIGHT
import math

class Twister(Widget):
    def __init__(self, **kwargs):
        super(Twister, self).__init__(**kwargs)
        self.angle = 0
        self.rotation_speed = 1  # degrees per frame
        self.size = (140, 140)  # Set a default size for the twister

    def update(self, dt):
        self.angle += self.rotation_speed

    def draw(self):
        with self.canvas:
            PushMatrix()
            # Use self.center if parent is not available
            origin = self.parent.center if self.parent else (GAME_WIDTH / 2, GAME_HEIGHT / 2)
            Rotate(origin=origin, angle=self.angle)
            Color(0.5, 0.5, 0.5)  # Gray
            Ellipse(pos=(self.center_x - self.width / 2, self.center_y - self.height / 2), size=self.size)
            PopMatrix()

    def on_size(self, *args):
        self.center = self.parent.center if self.parent else (GAME_WIDTH / 2, GAME_HEIGHT / 2)