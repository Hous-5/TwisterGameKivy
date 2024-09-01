import os
from kivy.core.audio import SoundLoader
from kivy.clock import Clock

class AudioManager:
    def __init__(self):
        self.sounds = {}
        self.background_music = None
        self.volume = 0.025

    def load_sound(self, name, filename):
        full_path = os.path.join(os.path.dirname(__file__), '..', '..', filename)
        self.sounds[name] = SoundLoader.load(full_path)

    def play_sound(self, name):
        if name in self.sounds:
            sound = self.sounds[name]
            sound.volume = self.volume
            sound.play()

    def set_volume(self, volume):
        self.volume = max(0, min(1, volume))
        if self.background_music:
            self.background_music.volume = self.volume

    def load_background_music(self, filename):
        self.stop_background_music()
        full_path = os.path.join(os.path.dirname(__file__), '..', '..', filename)
        self.background_music = SoundLoader.load(full_path)

    def play_background_music(self, loop=True):
        if self.background_music:
            self.background_music.loop = loop
            self.background_music.volume = self.volume
            self.background_music.play()

    def stop_background_music(self):
        if self.background_music:
            self.background_music.stop()

    def pause_background_music(self):
        if self.background_music:
            self.background_music.stop()

    def resume_background_music(self):
        if self.background_music:
            self.background_music.play()

# Global audio manager instance
audio_manager = AudioManager()