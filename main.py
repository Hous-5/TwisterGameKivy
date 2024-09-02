from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.core.window import Window
from screens.menu import MainMenu
from screens.game import GameScreen
from screens.settings import SettingsMenu
from screens.leaderboard import LeaderboardMenu
from screens.login import LoginMenu
from screens.game_over import GameOverScreen
from utils.sound_manager import SoundManager
from utils.server_communication import ServerCommunication
from utils.asset_manager import AssetManager
from utils.device_optimizer import DeviceOptimizer

class TwisterApp(App):
    def build(self):
        # Initialize managers and settings
        self.asset_manager = AssetManager()
        self.sound_manager = SoundManager(self.asset_manager)
        self.server_comm = ServerCommunication("http://localhost:5000/api")
        self.device_optimizer = DeviceOptimizer()
        self.is_logged_in = False
        self.username = ""
        self.last_score = 0
        self.graphics_quality = 1
        self.music_volume = 0.03
        self.sfx_volume = 0.3
        self.vibration_enabled = True

        # Create ScreenManager
        self.sm = ScreenManager(transition=FadeTransition())

        # Create and add all screens
        screens = [
            MainMenu(name='menu'),
            GameScreen(name='game'),
            SettingsMenu(name='settings'),
            LeaderboardMenu(name='leaderboard'),
            LoginMenu(name='login'),
            GameOverScreen(name='gameover')
        ]

        for screen in screens:
            self.sm.add_widget(screen)
            print(f"Added screen: {screen.name}")  # Debug print

        # Set initial screen
        self.sm.current = 'menu'

        return self.sm

    def on_keyboard(self, window, key, *args):
        if key == 27:  # ESC key
            if self.sm.current == 'game':
                self.pause_game()
                return True
            elif self.sm.current == 'pause':
                self.resume_game()
                return True
        return False

    def start_game(self):
        self.sm.get_screen('game').start_game()
        self.sm.current = 'game'

    def show_settings(self):
        self.sm.current = 'settings'

    def show_leaderboard(self):
        self.sm.current = 'leaderboard'
        self.sm.get_screen('leaderboard').fetch_leaderboard()

    def show_login(self):
        self.sm.current = 'login'

    def show_main_menu(self):
        self.sm.current = 'menu'

    def pause_game(self):
        self.sm.current = 'pause'

    def resume_game(self):
        self.sm.current = 'game'

    def show_game_over(self, score):
        print(f"Attempting to show game over screen with score: {score}")  # Debug print
        self.last_score = score
        gameover_screen = self.sm.get_screen('gameover')
        if gameover_screen:
            gameover_screen.set_score(score)
            self.sm.current = 'gameover'
        else:
            print("Error: GameOverScreen not found")  # Debug print

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

    def on_score_submitted(self, request, result):
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
        
        # Update sound settings
        self.sound_manager.set_music_volume(self.music_volume)
        self.sound_manager.set_sfx_volume(self.sfx_volume)

        # Update game settings if the game is currently running
        game_screen = self.sm.get_screen('game')
        if game_screen and game_screen.game:
            game_screen.game.particle_system.update_particle_count()
            game_screen.game.update_background_particles()

    def on_stop(self):
        self.sound_manager.stop_music()
        self.asset_manager.unload_unused_assets()

if __name__ == '__main__':
    TwisterApp().run()