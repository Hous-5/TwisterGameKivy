from kivy.uix.widget import Widget
from kivy.graphics import PushMatrix, PopMatrix, Translate, Rotate, Rectangle, Color
from kivy.properties import NumericProperty
import math

class KivyPlayer(Widget):
    def __init__(self, center_x, center_y, ring_radius, scale_factor, asset_manager, **kwargs):
        super(KivyPlayer, self).__init__(**kwargs)
        self.center_x = center_x
        self.center_y = center_y
        self.ring_radius = ring_radius
        self.radius = max(8, int(12 * scale_factor))
        self.angle = 0
        self.combo = 0
        self.combo_timer = 0
        self.score_multiplier = 1
        self.speed_multiplier = 1
        self.invincible = False
        self.texture = asset_manager.get_texture('Player.png')
        self.size = (self.radius * 2.3, self.radius * 2.3)
        self.update_position()

    def update_position(self):
        self.center = (
            self.center_x + math.cos(self.angle) * self.ring_radius,
            self.center_y + math.sin(self.angle) * self.ring_radius
        )

    def move(self, clockwise, difficulty_multiplier):
        speed = 3 * difficulty_multiplier * self.speed_multiplier  # Adjust base speed as needed
        if clockwise:
            self.angle += speed / self.ring_radius
        else:
            self.angle -= speed / self.ring_radius
        self.update_position()

    def update_canvas(self, *args):
        self.canvas.clear()
        with self.canvas:
            PushMatrix()
            Rotate(angle=math.degrees(self.angle), origin=self.center)
            Color(1, 1, 1)  # White color
            Rectangle(pos=self.pos, size=self.size, texture=self.texture)
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
    
    def draw(self):
        with self.canvas:
            PushMatrix()
            Translate(*self.center)
            Rotate(angle=math.degrees(self.angle), origin=(0, 0))
            Rectangle(pos=(-self.size[0]/2, -self.size[1]/2), size=self.size, texture=self.texture)
            PopMatrix()