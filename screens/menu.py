from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.metrics import dp

class MainMenu(Screen):
    def __init__(self, **kwargs):
        super(MainMenu, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        
        # Title
        title = Button(text='Twister Game', size_hint_y=None, height=dp(60), background_color=(0.5, 0.7, 1, 1))
        title.bind(on_press=lambda x: None)  # Make it non-clickable
        layout.add_widget(title)
        
        # Start Game button
        start_button = Button(text='Start Game', on_press=self.start_game)
        layout.add_widget(start_button)
        
        # Settings button
        settings_button = Button(text='Settings', on_press=self.show_settings)
        layout.add_widget(settings_button)
        
        # Leaderboard button
        leaderboard_button = Button(text='Leaderboard', on_press=self.show_leaderboard)
        layout.add_widget(leaderboard_button)
        
        # Login button
        login_button = Button(text='Login', on_press=self.show_login)
        layout.add_widget(login_button)
        
        # Quit button
        quit_button = Button(text='Quit', on_press=self.quit_game)
        layout.add_widget(quit_button)
        
        self.add_widget(layout)

    def start_game(self, instance):
        app = App.get_running_app()
        app.sound_manager.play_menu_click()
        app.start_game()

    def show_settings(self, instance):
        app = App.get_running_app()
        app.sound_manager.play_menu_click()
        app.show_settings()

    def show_leaderboard(self, instance):
        app = App.get_running_app()
        app.sound_manager.play_menu_click()
        app.show_leaderboard()

    def show_login(self, instance):
        app = App.get_running_app()
        app.sound_manager.play_menu_click()
        app.show_login()

    def quit_game(self, instance):
        app = App.get_running_app()
        app.sound_manager.play_menu_click()
        app.stop()