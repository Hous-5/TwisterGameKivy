import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivy.core.window import Window
from kivy.lang import Builder

from src.screens.game_screen import GameScreen
from src.screens.menu_screen import MenuScreen
from src.screens.settings_screen import SettingsScreen
from src.screens.leaderboard_screen import LeaderboardScreen
from src.audio_manager import audio_manager

class TwisterApp(App):
    def build(self):
        Window.size = (480, 848)
        self.init_audio()
        
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(GameScreen(name='game'))
        sm.add_widget(SettingsScreen(name='settings'))
        sm.add_widget(LeaderboardScreen(name='leaderboard'))
        
        return sm

    def init_audio(self):
        audio_manager.load_sound('click', 'assets/sounds/click.wav')
        audio_manager.load_sound('collect', 'assets/sounds/collect.wav')
        audio_manager.load_sound('game_over', 'assets/sounds/game_over.wav')
        audio_manager.load_background_music('assets/music/background_music.mp3')
        audio_manager.play_background_music()

if __name__ == '__main__':
    Builder.load_file('twister.kv')
    TwisterApp().run()