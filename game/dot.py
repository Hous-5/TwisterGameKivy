from kivy.graphics import Color, Ellipse
import random
import math

class KivyDot:
    def __init__(self, center_x, center_y, ring_radius, scale_factor):
        self.center_x = center_x
        self.center_y = center_y
        self.ring_radius = ring_radius
        self.angle = random.uniform(0, 2 * math.pi)
        self.distance = 50
        self.good = random.choice([True, False])
        self.radius = max(6, int(8 * scale_factor))
        self.update_position()

    def update_position(self):
        self.x = self.center_x + math.cos(self.angle) * self.distance
        self.y = self.center_y + math.sin(self.angle) * self.distance

    def move(self, difficulty_multiplier):
        speed = 1.5 * difficulty_multiplier
        self.angle += 0.02 * difficulty_multiplier
        self.distance += speed * 1.2
        self.update_position()

    def draw(self):
        Color(0, 1, 0) if self.good else Color(1, 0, 0)  # Green for good, Red for bad
        Ellipse(pos=(self.x - self.radius, self.y - self.radius), size=(self.radius * 2, self.radius * 2))