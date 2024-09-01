import math
import random
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.graphics import Color, Ellipse
from src.constants import DOT_RADIUS, GAME_WIDTH, GAME_HEIGHT

class Dot(Widget):
    center_x = NumericProperty(0)
    center_y = NumericProperty(0)
    radius = NumericProperty(DOT_RADIUS)

    def __init__(self, **kwargs):
        super(Dot, self).__init__(**kwargs)
        self.angle = random.uniform(0, 2 * math.pi)
        self.distance = 50
        self.good = random.choice([True, False])
        self.update_position()

    def update_position(self):
        if self.parent:
            self.center_x = self.parent.center_x + math.cos(self.angle) * self.distance
            self.center_y = self.parent.center_y + math.sin(self.angle) * self.distance
        else:
            self.center_x = GAME_WIDTH / 2 + math.cos(self.angle) * self.distance
            self.center_y = GAME_HEIGHT / 2 + math.sin(self.angle) * self.distance

    def move(self, difficulty_multiplier):
        from src.constants import PLAYER_SPEED  # Import here to avoid circular import
        speed = PLAYER_SPEED * difficulty_multiplier
        self.angle += 0.02 * difficulty_multiplier
        self.distance += speed * 1.2
        self.update_position()

    def draw(self):
        with self.canvas:
            Color(0, 1, 0) if self.good else Color(1, 0, 0)  # Green for good, Red for bad
            Ellipse(pos=(self.center_x - self.radius, self.center_y - self.radius), 
                    size=(self.radius*2, self.radius*2))