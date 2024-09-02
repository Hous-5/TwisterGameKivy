from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from game.twister_game import TwisterGame
from kivy.app import App

class GameScreen(Screen):
    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self.game = None

    def on_enter(self):
        if not self.game:
            self.create_game()

    def create_game(self):
        app = App.get_running_app()
        self.game = TwisterGame(
            sound_manager=app.sound_manager,
            asset_manager=app.asset_manager,
            device_optimizer=app.device_optimizer,
            size=(Window.width, Window.height)
        )
        self.add_widget(self.game)

    def start_game(self):
        if not self.game:
            self.create_game()
        self.game.start_game()

    def on_leave(self):
        if self.game:
            self.remove_widget(self.game)
            self.game = None