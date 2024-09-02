from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Ellipse, PushMatrix, PopMatrix, Rotate, Translate
from kivy.properties import NumericProperty, ObjectProperty
import math

class KivyTwister(Widget):
    rotation = NumericProperty(0)
    texture = ObjectProperty(None)

    def __init__(self, center_x, center_y, asset_manager, **kwargs):
        super(KivyTwister, self).__init__(**kwargs)
        self.center_x = center_x
        self.center_y = center_y
        self.texture = asset_manager.get_texture('Center_Sun.png')
        self.rotation_speed = 1  # Adjust as needed
        self.size = (140, 140)
        self.bind(pos=self.update_canvas, size=self.update_canvas, rotation=self.update_canvas)

    def update(self, dt):
        self.rotation += self.rotation_speed
        if self.rotation >= 360:
            self.rotation -= 360

    def update_canvas(self, *args):
        self.canvas.clear()
        with self.canvas:
            PushMatrix()
            Translate(self.center_x, self.center_y)
            Rotate(angle=self.rotation, origin=(0, 0))
            Rectangle(pos=(-self.size[0]/2, -self.size[1]/2), size=self.size, texture=self.texture)
            PopMatrix()

            # Draw central circles
            for i in range(2):
                offset = i * 5
                x = math.cos(math.radians(self.rotation + i * 120)) * offset
                y = math.sin(math.radians(self.rotation + i * 120)) * offset
                Color(1, 1, 1, 0.5)  # Semi-transparent white
                Ellipse(pos=(self.center_x + x - 5, self.center_y + y - 5), size=(10, 10))

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            return True
        return super(KivyTwister, self).on_touch_down(touch)