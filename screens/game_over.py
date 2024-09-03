from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.app import App

class GameOverScreen(Screen):
    def __init__(self, **kwargs):
        super(GameOverScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        self.score_label = Label(text="Game Over", font_size='30sp')
        self.layout.add_widget(self.score_label)
        self.layout.add_widget(Button(text="Play Again", on_press=self.play_again))
        self.layout.add_widget(Button(text="Main Menu", on_press=self.main_menu))
        self.add_widget(self.layout)

    def on_enter(self):
        app = App.get_running_app()
        if app.is_logged_in:
            app.submit_score(app.last_score)

    def set_score(self, score):
        self.score_label.text = f"Game Over\nFinal Score: {score}"

    def play_again(self, instance):
        App.get_running_app().sound_manager.play_menu_click()
        App.get_running_app().start_game()

    def main_menu(self, instance):
        App.get_running_app().sound_manager.play_menu_click()
        App.get_running_app().show_main_menu()