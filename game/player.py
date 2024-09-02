from kivy.uix.widget import Widget
from kivy.graphics import PushMatrix, PopMatrix, Ellipse, Translate, Rotate, Rectangle, Color
from kivy.properties import NumericProperty
import math

class KivyPlayer(Widget):
    def __init__(self, center_x, center_y, ring_radius, scale_factor, asset_manager, **kwargs):
        super(KivyPlayer, self).__init__(**kwargs)
        self.twister_center_x = center_x
        self.twister_center_y = center_y
        self.ring_radius = ring_radius
        self.radius = max(8, int(12 * scale_factor))
        self.angle = 0  # Angle in radians
        self.combo = 0
        self.combo_timer = 0
        self.score_multiplier = 1
        self.speed_multiplier = 1
        self.invincible = False
        self.texture = asset_manager.get_texture('Player.png')
        if self.texture is None:
            print("Warning: Player texture not loaded")
        self.size = (self.radius * 2.3, self.radius * 2.3)
        self.update_position()
        print(f"Player initialized at: {self.pos}")


    def update_position(self):
        # Calculate position on the ring
        self.center_x = self.twister_center_x + self.ring_radius * math.cos(self.angle)
        self.center_y = self.twister_center_y + self.ring_radius * math.sin(self.angle)
        self.pos = (self.center_x - self.size[0]/2, self.center_y - self.size[1]/2)
        print(f"Player position updated to: {self.pos}")  # Debug print

    def move(self, clockwise, difficulty_multiplier):
        speed = 0.05 * difficulty_multiplier * self.speed_multiplier  # Adjust speed as needed
        if clockwise:
            self.angle -= speed  # Subtract for clockwise movement
        else:
            self.angle += speed  # Add for counter-clockwise movement
        
        # Keep angle between 0 and 2π
        self.angle %= 2 * math.pi
        
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
        print(f"Drawing player at: {self.pos}")  # Debug print
        with self.canvas:
            PushMatrix()
            Translate(self.center_x, self.center_y)
            Rotate(angle=math.degrees(-self.angle), origin=(0, 0))
            Color(1, 1, 1)  # White color
            if self.texture:
                Rectangle(pos=(-self.size[0]/2, -self.size[1]/2), size=self.size, texture=self.texture)
            else:
                print("Warning: Player texture is None, drawing placeholder")
                Color(1, 0, 0)  # Red color for placeholder
                Ellipse(pos=(-self.radius, -self.radius), size=(self.radius*2, self.radius*2))
            PopMatrix()