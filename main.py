from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivy.core.window import Window
from screens.menu import MainMenu
from screens.game import GameScreen
from screens.settings import SettingsMenu
from screens.pause import PauseMenu
from screens.leaderboard import LeaderboardMenu
from screens.login import LoginMenu
from screens.game_over import GameOverScreen
from utils.sound_manager import SoundManager
from utils.server_communication import ServerCommunication
from utils.asset_manager import AssetManager
from utils.device_optimizer import DeviceOptimizer

class TwisterApp(App):
    def build(self):
        self.asset_manager = AssetManager()
        self.sound_manager = SoundManager(self.asset_manager)
        self.server_comm = ServerCommunication("http://localhost:5000/api")
        self.device_optimizer = DeviceOptimizer()
        self.is_logged_in = False
        self.username = ""
        self.last_score = 0
        self.graphics_quality = 1
        self.music_volume = 0.03  # Default music volume
        self.sfx_volume = 0.3    # Default SFX volume
        self.vibration_enabled = True

        self.sm = ScreenManager(transition=FadeTransition())
        self.sm.add_widget(MainMenu(name='menu'))
        self.sm.add_widget(GameScreen(name='game'))
        self.sm.add_widget(SettingsMenu(name='settings'))
        self.sm.add_widget(PauseMenu(name='pause'))
        self.sm.add_widget(LeaderboardMenu(name='leaderboard'))
        self.sm.add_widget(LoginMenu(name='login'))
        self.sm.add_widget(GameOverScreen(name='gameover'))

        Window.bind(on_keyboard=self.on_keyboard)

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
        self.sm.get_screen('game').game.__init__()
        self.sm.current = 'game'

    def show_settings(self):
        self.sm.current = 'settings'

    def show_leaderboard(self):
        self.sm.current = 'leaderboard'
        self.sm.get_screen('leaderboard').fetch_leaderboard()

    def show_login(self):
        self.sm.current = 'login'

    def pause_game(self):
        self.sm.current = 'pause'

    def resume_game(self):
        self.sm.current = 'game'

    def show_game_over(self, score):
        self.last_score = score
        self.sm.get_screen('gameover').set_score(score)
        self.sm.current = 'gameover'

    def show_main_menu(self):
        self.sm.current = 'menu'

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