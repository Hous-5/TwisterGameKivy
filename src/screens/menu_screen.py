from kivy.uix.screenmanager import Screen

class MenuScreen(Screen):
    def start_game(self):
        self.manager.current = 'game'

    def open_settings(self):
        self.manager.current = 'settings'

    def open_leaderboard(self):
        self.manager.current = 'leaderboard'