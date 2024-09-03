from kivy.graphics import Color, Rectangle, PushMatrix, PopMatrix, Rotate, Translate
import math

class KivyTwister:
    def __init__(self, center_x, center_y, texture):
        self.center_x = center_x
        self.center_y = center_y
        self.texture = texture
        self.rotation = 0
        self.rotation_speed = 1
        self.size = (140, 140)

    def update(self, dt):
        self.rotation += self.rotation_speed
        if self.rotation >= 360:
            self.rotation -= 360

    def draw(self, canvas):
        with canvas:
            PushMatrix()
            Translate(self.center_x, self.center_y)
            Rotate(angle=self.rotation, origin=(0, 0))
            if self.texture:
                Color(1, 1, 1, 1)  # White color
                Rectangle(pos=(-self.size[0]/2, -self.size[1]/2), size=self.size, texture=self.texture)
            else:
                Color(0, 1, 0)  # Green color for placeholder
                Ellipse(pos=(-self.size[0]/2, -self.size[1]/2), size=self.size)
            PopMatrix()