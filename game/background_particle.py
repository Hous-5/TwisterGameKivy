from kivy.graphics import Color, Ellipse
import random
import math

class KivyBackgroundParticle:
    def __init__(self, game_width, game_height):
        self.game_width = game_width
        self.game_height = game_height
        self.reset_position()
        self.size = random.randint(1, 3)
        self.speed = random.uniform(0.5, 2)
        self.angle = random.uniform(0, 2 * math.pi)

    def reset_position(self):
        self.x = random.uniform(0, self.game_width)
        self.y = random.uniform(0, self.game_height)

    def move(self):
        self.x += math.cos(self.angle) * self.speed
        self.y += math.sin(self.angle) * self.speed
        if self.x < 0 or self.x > self.game_width or self.y < 0 or self.y > self.game_height:
            self.reset_position()

    def draw(self):
        Color(0.37, 0.37, 0.37)  # Light grey
        Ellipse(pos=(self.x - self.size // 2, self.y - self.size // 2), size=(self.size, self.size))