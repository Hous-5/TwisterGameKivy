from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.app import App
from kivy.core.window import Window

class AchievementsScreen(Screen):
    def __init__(self, **kwargs):
        super(AchievementsScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.add_widget(self.layout)

    def on_enter(self):
        self.update_achievements()

    def update_achievements(self):
        self.layout.clear_widgets()
        app = App.get_running_app()
        if hasattr(app, 'achievement_system'):
            achievement_system = app.achievement_system
            for achievement in achievement_system.achievements:
                status = "Unlocked" if achievement.unlocked else "Locked"
                self.layout.add_widget(Label(text=f"{achievement.name}: {status}\n{achievement.description}"))
        else:
            self.layout.add_widget(Label(text="Achievements not available"))
        
        back_button = Button(text="Back to Main Menu", size_hint=(None, None), size=(200, 50))
        back_button.bind(on_press=self.go_to_main_menu)
        self.layout.add_widget(back_button)

    def go_to_main_menu(self, instance):
        App.get_running_app().show_main_menu()