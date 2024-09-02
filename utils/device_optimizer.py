from kivy.utils import platform
from kivy.core.window import Window

class DeviceOptimizer:
    def __init__(self):
        self.device_tier = self.determine_device_tier()

    def determine_device_tier(self):
        if platform == 'android' or platform == 'ios':
            # Simple mobile device detection based on resolution and pixel density
            width, height = Window.size
            density = Window.dpi / 160  # Convert DPI to density

            if width * height * density > 2073600:  # Equivalent to 1080p at standard density
                return 'high'
            elif width * height * density > 921600:  # Equivalent to 720p at standard density
                return 'medium'
            else:
                return 'low'
        else:
            return 'high'  # Assume desktop is high-tier

    def get_particle_count(self):
        if self.device_tier == 'high':
            return 20
        elif self.device_tier == 'medium':
            return 10
        else:
            return 5

    def get_background_particle_count(self):
        if self.device_tier == 'high':
            return 50
        elif self.device_tier == 'medium':
            return 30
        else:
            return 15

    def should_use_advanced_shaders(self):
        return self.device_tier == 'high'