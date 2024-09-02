import os
from kivy.core.image import Image as CoreImage
from kivy.core.audio import SoundLoader

class AssetManager:
    def __init__(self):
        self.textures = {}
        self.sounds = {}
        # Adjust this path to match your project structure
        self.asset_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets')

    def get_texture(self, image_name):
        if image_name not in self.textures:
            image_path = os.path.join(self.asset_dir, 'images', image_name)
            if os.path.exists(image_path):
                self.textures[image_name] = CoreImage(image_path).texture
            else:
                print(f"Warning: Image {image_name} not found at {image_path}")
                return None
        return self.textures[image_name]

    def get_sound(self, sound_name):
        if sound_name not in self.sounds:
            sound_path = os.path.join(self.asset_dir, 'sounds', sound_name)
            if os.path.exists(sound_path):
                self.sounds[sound_name] = SoundLoader.load(sound_path)
            else:
                print(f"Warning: Sound {sound_name} not found at {sound_path}")
                return None
        return self.sounds[sound_name]

    def unload_unused_assets(self):
        # Implement logic to unload assets that haven't been used recently
        pass