from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.app import App

class TutorialScreen(Screen):
    def __init__(self, **kwargs):
        super(TutorialScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        instructions = [
            "Welcome to Twister!",
            "1. Tap to change direction",
            "2. Collect green dots",
            "3. Avoid red dots",
            "4. Power-ups:",
            "   - Blue: Speed boost",
            "   - Purple: Score multiplier",
            "   - Orange: Invincibility",
            "5. Build combos for higher scores!"
        ]
        
        for instruction in instructions:
            layout.add_widget(Label(text=instruction, font_size='18sp'))
        
        start_button = Button(text="Start Game", size_hint=(None, None), size=(200, 50))
        start_button.bind(on_press=self.start_game)
        layout.add_widget(start_button)
        
        self.add_widget(layout)

    def start_game(self, instance):
        App.get_running_app().start_game()
