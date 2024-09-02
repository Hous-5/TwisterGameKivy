from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.app import App

class MainMenu(Screen):
    def __init__(self, **kwargs):
        super(MainMenu, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(Label(text='Twister Game'))
        layout.add_widget(Button(text='Start Game', on_press=self.start_game))
        layout.add_widget(Button(text='Settings', on_press=self.show_settings))
        layout.add_widget(Button(text='Leaderboard', on_press=self.show_leaderboard))
        layout.add_widget(Button(text='Login', on_press=self.show_login))
        layout.add_widget(Button(text='Quit', on_press=self.quit_game))
        self.add_widget(layout)

    def start_game(self, instance):
        App.get_running_app().sound_manager.play_menu_click()
        App.get_running_app().start_game()

    def show_settings(self, instance):
        App.get_running_app().sound_manager.play_menu_click()
        App.get_running_app().show_settings()

    def show_leaderboard(self, instance):
        App.get_running_app().sound_manager.play_menu_click()
        App.get_running_app().show_leaderboard()

    def show_login(self, instance):
        App.get_running_app().sound_manager.play_menu_click()
        App.get_running_app().show_login()

    def quit_game(self, instance):
        App.get_running_app().sound_manager.play_menu_click()
        App.get_running_app().stop()