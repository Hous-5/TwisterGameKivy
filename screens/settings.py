from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.switch import Switch
from kivy.uix.button import Button
from kivy.app import App

class SettingsMenu(Screen):
    def __init__(self, **kwargs):
        super(SettingsMenu, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        self.layout.add_widget(Label(text='Graphics Quality'))
        self.quality_slider = Slider(min=0, max=2, step=1, value=1)
        self.layout.add_widget(self.quality_slider)
        
        self.layout.add_widget(Label(text='Music Volume'))
        self.music_slider = Slider(min=0, max=1, value=0.5)
        self.layout.add_widget(self.music_slider)
        
        self.layout.add_widget(Label(text='SFX Volume'))
        self.sfx_slider = Slider(min=0, max=1, value=0.5)
        self.layout.add_widget(self.sfx_slider)
        
        self.layout.add_widget(Label(text='Vibration'))
        self.vibration_switch = Switch(active=True)
        self.layout.add_widget(self.vibration_switch)
        
        self.save_button = Button(text='Save Settings', on_press=self.save_settings)
        self.layout.add_widget(self.save_button)
        
        self.add_widget(self.layout)

    def on_enter(self):
        app = App.get_running_app()
        self.quality_slider.value = app.graphics_quality
        self.music_slider.value = app.music_volume
        self.sfx_slider.value = app.sfx_volume
        self.vibration_switch.active = app.vibration_enabled

    def save_settings(self, instance):
        app = App.get_running_app()
        app.graphics_quality = int(self.quality_slider.value)
        app.music_volume = self.music_slider.value
        app.sfx_volume = self.sfx_slider.value
        app.vibration_enabled = self.vibration_switch.active
        app.apply_settings()
        app.show_main_menu()