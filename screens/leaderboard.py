from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.app import App

class LeaderboardMenu(Screen):
    def __init__(self, **kwargs):
        super(LeaderboardMenu, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.layout.add_widget(Label(text='Leaderboard'))
        self.leaderboard_widget = Label(text='Loading...')
        self.layout.add_widget(self.leaderboard_widget)
        self.layout.add_widget(Button(text='Back', on_press=self.go_back))
        self.add_widget(self.layout)

    def on_enter(self):
        self.fetch_leaderboard()

    def fetch_leaderboard(self):
        App.get_running_app().server_comm.get_leaderboard(self.display_leaderboard)

    def display_leaderboard(self, leaderboard):
        self.leaderboard_widget.text = '\n'.join([f"{entry['name']}: {entry['score']}" for entry in leaderboard])

    def go_back(self, instance):
        App.get_running_app().show_main_menu()