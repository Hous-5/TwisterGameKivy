import math
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.graphics import Color, Ellipse
from src.constants import PLAYER_RADIUS, RING_RADIUS, GAME_WIDTH, GAME_HEIGHT

class Player(Widget):
    radius = NumericProperty(PLAYER_RADIUS)

    def __init__(self, **kwargs):
        super(Player, self).__init__(**kwargs)
        self.angle = 0
        self.radius = PLAYER_RADIUS
        self.combo = 0
        self.speed_multiplier = 1
        self.invincible = False
        self.score_multiplier = 1

    def update_position(self):
        if self.parent:
            self.center_x = self.parent.center_x + math.cos(self.angle) * RING_RADIUS
            self.center_y = self.parent.center_y + math.sin(self.angle) * RING_RADIUS
        else:
            # Use default game dimensions if parent is not set
            self.center_x = GAME_WIDTH / 2 + math.cos(self.angle) * RING_RADIUS
            self.center_y = GAME_HEIGHT / 2 + math.sin(self.angle) * RING_RADIUS

    def move(self, clockwise, difficulty_multiplier):
        from src.constants import PLAYER_SPEED  # Import here to avoid circular import
        speed = PLAYER_SPEED * difficulty_multiplier * self.speed_multiplier
        if clockwise:
            self.angle += speed / RING_RADIUS
        else:
            self.angle -= speed / RING_RADIUS
        self.update_position()

    def reset(self):
        self.angle = 0
        self.combo = 0
        self.speed_multiplier = 1
        self.invincible = False
        self.score_multiplier = 1
        self.update_position()

    def increase_combo(self):
        self.combo += 1

    def draw(self):
        with self.canvas:
            Color(1, 1, 0)  # Yellow
            Ellipse(pos=(self.center_x - self.radius, self.center_y - self.radius), 
                    size=(self.radius*2, self.radius*2))