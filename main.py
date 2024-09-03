from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FadeTransition, SlideTransition, CardTransition
from kivy.core.window import Window
from screens.menu import MainMenu
from screens.game_screen import GameScreen
from screens.settings import SettingsMenu
from screens.leaderboard import LeaderboardMenu
from screens.login import LoginMenu
from screens.game_over import GameOverScreen
from screens.tutorial import TutorialScreen
from screens.pause import PauseMenu
from screens.difficulty import DifficultyScreen
from screens.achievements import AchievementsScreen
from utils.sound_manager import SoundManager
from utils.server_communication import ServerCommunication
from utils.asset_manager import AssetManager
from utils.device_optimizer import DeviceOptimizer
from game.achievement_system import AchievementSystem
import config

class TwisterApp(App):
    def build(self):
        # Initialize managers and settings
        self.asset_manager = AssetManager()
        self.sound_manager = SoundManager(self.asset_manager)
        self.server_comm = ServerCommunication("http://localhost:5000/api")
        self.device_optimizer = DeviceOptimizer()
        self.achievement_system = AchievementSystem()  # Add this line
        self.is_logged_in = False
        self.username = ""
        self.last_score = 0
        self.graphics_quality = config.INITIAL_GRAPHICS_QUALITY
        self.music_volume = config.INITIAL_MUSIC_VOLUME
        self.sfx_volume = config.INITIAL_SFX_VOLUME
        self.vibration_enabled = config.INITIAL_VIBRATION_ENABLED

        # Set window size
        Window.size = (config.SCREEN_WIDTH, config.SCREEN_HEIGHT)

        # Create ScreenManager with custom transitions
        self.sm = ScreenManager(transition=FadeTransition(duration=0.5))

        # Create and add all screens with custom transitions
        screens = [
            (MainMenu(name='menu'), SlideTransition(direction='left')),
            (GameScreen(name='game'), FadeTransition(duration=0.3)),
            (SettingsMenu(name='settings'), CardTransition(direction='up', mode='push')),
            (LeaderboardMenu(name='leaderboard'), SlideTransition(direction='left')),
            (LoginMenu(name='login'), CardTransition(direction='up', mode='push')),
            (GameOverScreen(name='gameover'), FadeTransition(duration=0.5)),
            (TutorialScreen(name='tutorial'), SlideTransition(direction='left')),
            (PauseMenu(name='pause'), CardTransition(direction='down', mode='pop')),
            (DifficultyScreen(name='difficulty'), SlideTransition(direction='left')),
            (AchievementsScreen(name='achievements'), SlideTransition(direction='left'))
        ]

        for screen, transition in screens:
            self.sm.add_widget(screen)
            screen.transition = transition

        # Set initial screen
        self.sm.current = 'menu'

        return self.sm

    def on_start(self):
        self.sound_manager.start_background_music()

    def on_stop(self):
        self.sound_manager.stop_background_music()
        self.asset_manager.unload_unused_assets()

    def start_game(self):
        self.sm.get_screen('game').start_game()
        self.sm.current = 'game'

    def show_settings(self):
        self.sm.transition.direction = 'up'
        self.sm.current = 'settings'

    def show_leaderboard(self):
        self.sm.transition.direction = 'left'
        self.sm.current = 'leaderboard'
        self.sm.get_screen('leaderboard').fetch_leaderboard()

    def show_login(self):
        self.sm.transition.direction = 'up'
        self.sm.current = 'login'

    def show_main_menu(self):
        self.sm.transition.direction = 'right'
        self.sm.current = 'menu'

    def show_tutorial(self):
        self.sm.transition.direction = 'left'
        self.sm.current = 'tutorial'

    def show_pause_menu(self):
        self.sm.transition.direction = 'down'
        self.sm.current = 'pause'

    def show_difficulty_screen(self):
        self.sm.transition.direction = 'left'
        self.sm.current = 'difficulty'

    def show_achievements(self):
        self.sm.transition.direction = 'left'
        self.sm.current = 'achievements'

    def resume_game(self):
        self.sm.transition.direction = 'up'
        self.sm.current = 'game'
        self.sm.get_screen('game').resume_game()

    def show_game_over(self, score):
        self.last_score = score
        self.sm.get_screen('gameover').set_score(score)
        self.sm.current = 'gameover'

    def register(self, username, password):
        def on_success(result):
            print("Registration successful")
            login_screen = self.sm.get_screen('login')
            login_screen.update_message("Registration successful! You can now log in.")

        def on_failure(error):
            print(f"Registration failed: {error}")
            login_screen = self.sm.get_screen('login')
            login_screen.update_message(f"Registration failed: {error}")

        self.server_comm.register(username, password, on_success, on_failure)

    def login(self, username, password):
        def on_success(result):
            self.is_logged_in = True
            self.username = username
            print("Login successful")
            self.show_main_menu()

        def on_failure(error):
            print(f"Login failed: {error}")
            login_screen = self.sm.get_screen('login')
            login_screen.update_message(f"Login failed: {error}")

        self.server_comm.login(username, password, on_success, on_failure)

    def submit_score(self, score):
        if self.is_logged_in:
            self.server_comm.submit_score(score, self.on_score_submitted)

    def on_score_submitted(self, result):
        if result.get('success'):
            print("Score submitted successfully")
        else:
            print("Failed to submit score:", result.get('error'))

    def apply_settings(self):
        if self.graphics_quality == 0:
            self.device_optimizer.device_tier = 'low'
        elif self.graphics_quality == 1:
            self.device_optimizer.device_tier = 'medium'
        else:
            self.device_optimizer.device_tier = 'high'
        
        self.sound_manager.set_music_volume(self.music_volume)
        self.sound_manager.set_sfx_volume(self.sfx_volume)

        game_screen = self.sm.get_screen('game')
        if game_screen and game_screen.game:
            game_screen.game.particle_system.update_particle_count()
            game_screen.game.update_background_particles()

if __name__ == '__main__':
    TwisterApp().run()