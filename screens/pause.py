from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.app import App

class PauseMenu(Screen):
    def __init__(self, **kwargs):
        super(PauseMenu, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        layout.add_widget(Label(text='Paused'))
        layout.add_widget(Button(text='Resume', on_press=self.resume_game))
        layout.add_widget(Button(text='Settings', on_press=self.show_settings))
        layout.add_widget(Button(text='Quit to Main Menu', on_press=self.quit_to_main))
        self.add_widget(layout)

    def resume_game(self, instance):
        App.get_running_app().sound_manager.play_menu_click()
        App.get_running_app().resume_game()

    def show_settings(self, instance):
        App.get_running_app().sound_manager.play_menu_click()
        App.get_running_app().show_settings()

    def quit_to_main(self, instance):
        App.get_running_app().sound_manager.play_menu_click()
        App.get_running_app().show_main_menu()