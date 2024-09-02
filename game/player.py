from kivy.uix.widget import Widget
from kivy.graphics import PushMatrix, PopMatrix, Ellipse, Translate, Rotate, Rectangle, Color
from kivy.properties import NumericProperty
import math


class KivyPlayer:
    def __init__(self, center_x, center_y, ring_radius, scale_factor, texture):
        self.twister_center_x = center_x
        self.twister_center_y = center_y
        self.ring_radius = ring_radius
        self.radius = max(8, int(12 * scale_factor))
        self.angle = 0
        self.texture = texture
        self.size = (self.radius * 2.3, self.radius * 2.3)
        self.combo = 0
        self.combo_timer = 0
        self.score_multiplier = 1
        self.speed_multiplier = 1
        self.invincible = False
        self.update_position()

    def update_position(self):
        self.center_x = self.twister_center_x + self.ring_radius * math.cos(self.angle)
        self.center_y = self.twister_center_y + self.ring_radius * math.sin(self.angle)

    def move(self, clockwise, difficulty_multiplier):
        speed = 0.05 * difficulty_multiplier * self.speed_multiplier
        if clockwise:
            self.angle -= speed
        else:
            self.angle += speed
        self.angle %= 2 * math.pi
        self.update_position()

    def draw(self, canvas):
        print("Drawing player")
        print(f"Position: ({self.center_x}, {self.center_y}), Size: {self.size}")
        with canvas:
            PushMatrix()
            Translate(self.center_x, self.center_y)
            Rotate(angle=math.degrees(-self.angle), origin=(0, 0))
            if self.texture:
                Color(1, 1, 1, 1)  # White color
                Rectangle(pos=(-self.size[0]/2, -self.size[1]/2), size=self.size, texture=self.texture)
            else:
                Color(1, 0, 0)  # Red color for placeholder
                Ellipse(pos=(-self.radius, -self.radius), size=(self.radius*2, self.radius*2))
            PopMatrix()

    def collides_with(self, dot):
        distance = math.hypot(dot.x - self.center_x, dot.y - self.center_y)
        return distance < self.radius + dot.radius

    def update(self, dt):
        self.combo_timer -= dt
        if self.combo_timer <= 0:
            self.combo = 0

    def increase_combo(self):
        self.combo += 1
        self.combo_timer = 2  # Reset combo timer to 2 seconds

    def get_score_multiplier(self):
        return self.score_multiplier * (1 + self.combo * 0.1)  # 10% increase per combo level