from kivy.uix.screenmanager import Screen
from kivy.properties import NumericProperty
from src.audio_manager import audio_manager

class SettingsScreen(Screen):
    volume = NumericProperty(0.5)  # Default volume

    def __init__(self, **kwargs):
        super(SettingsScreen, self).__init__(**kwargs)
        self.volume = audio_manager.volume

    def on_volume(self, instance, value):
        audio_manager.set_volume(value)

    def go_back(self):
        audio_manager.play_sound('click')
        self.manager.current = 'menu'