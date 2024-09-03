from kivy.uix.popup import Popup
from kivy.uix.label import Label
import config

class Achievement:
    def __init__(self, name, description, condition):
        self.name = name
        self.description = description
        self.condition = condition
        self.unlocked = False

class AchievementSystem:
    def __init__(self):
        self.achievements = [Achievement(**achievement) for achievement in config.ACHIEVEMENTS]

    def check_achievements(self, game_state):
        for achievement in self.achievements:
            if not achievement.unlocked and achievement.condition(game_state):
                achievement.unlocked = True
                self.show_achievement_popup(achievement)

    def show_achievement_popup(self, achievement):
        content = Label(text=f"Achievement Unlocked!\n{achievement.name}\n{achievement.description}")
        popup = Popup(title='Achievement', content=content, size_hint=(None, None), size=(400, 200))
        popup.open()

    def get_unlocked_achievements(self):
        return [achievement for achievement in self.achievements if achievement.unlocked]

    def reset(self):
        for achievement in self.achievements:
            achievement.unlocked = False