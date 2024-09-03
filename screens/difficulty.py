from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.app import App
from kivy.core.window import Window

class DifficultyScreen(Screen):
    def __init__(self, **kwargs):
        super(DifficultyScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        layout.add_widget(Label(text="Select Difficulty", font_size='24sp'))
        
        difficulties = ['Easy', 'Normal', 'Hard']
        for diff in difficulties:
            btn = Button(text=diff, size_hint=(None, None), size=(200, 50))
            btn.bind(on_press=lambda x, d=diff.lower(): self.set_difficulty(d))
            layout.add_widget(btn)
        
        back_button = Button(text="Back", size_hint=(None, None), size=(200, 50))
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)
        
        self.add_widget(layout)

    def set_difficulty(self, difficulty):
        App.get_running_app().sm.get_screen('game').set_difficulty(difficulty)
        App.get_running_app().start_game()

    def go_back(self, instance):
        App.get_running_app().show_main_menu()