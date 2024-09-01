from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

class LeaderboardScreen(Screen):
    def __init__(self, **kwargs):
        super(LeaderboardScreen, self).__init__(**kwargs)
        self.populate_leaderboard()

    def populate_leaderboard(self):
        # This would typically be populated from a database or API
        scores = [("Player1", 100), ("Player2", 90), ("Player3", 80)]
        
        leaderboard_layout = self.ids.leaderboard_layout
        for idx, (player, score) in enumerate(scores, start=1):
            entry = BoxLayout(size_hint_y=None, height='40dp')
            entry.add_widget(Label(text=f"{idx}. {player}: {score}", font_size='20sp'))
            leaderboard_layout.add_widget(entry)

    def go_back(self):
        self.manager.current = 'menu'