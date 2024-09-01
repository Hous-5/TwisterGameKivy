import math
import random
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse
from src.constants import POWER_UP_RADIUS, GAME_WIDTH, GAME_HEIGHT

class PowerUp(Widget):
    def __init__(self, **kwargs):
        super(PowerUp, self).__init__(**kwargs)
        self.angle = random.uniform(0, 2 * math.pi)
        self.distance = 50
        self.type = random.choice(["speed", "invincibility", "score_multiplier"])
        self.radius = POWER_UP_RADIUS
        self.update_position()

    def update_position(self):
        if self.parent:
            self.center_x = self.parent.center_x + math.cos(self.angle) * self.distance
            self.center_y = self.parent.center_y + math.sin(self.angle) * self.distance
        else:
            # Use default game dimensions if parent is not set
            self.center_x = GAME_WIDTH / 2 + math.cos(self.angle) * self.distance
            self.center_y = GAME_HEIGHT / 2 + math.sin(self.angle) * self.distance

    def move(self, difficulty_multiplier):
        from src.constants import PLAYER_SPEED  # Import here to avoid circular import
        speed = PLAYER_SPEED * difficulty_multiplier
        self.angle += 0.02 * difficulty_multiplier
        self.distance += speed * 1.2
        self.update_position()

    def activate(self, player):
        if self.type == "speed":
            player.speed_multiplier = 2
        elif self.type == "invincibility":
            player.invincible = True
        elif self.type == "score_multiplier":
            player.score_multiplier = 2
        # Schedule deactivation after a certain time

    def draw(self):
        with self.canvas:
            Color(0, 0, 1)  # Blue for all power-ups
            Ellipse(pos=(self.center_x - self.radius, self.center_y - self.radius), 
                    size=(self.radius*2, self.radius*2))