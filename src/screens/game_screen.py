from kivy.uix.screenmanager import Screen
from kivy.properties import NumericProperty, ObjectProperty
from kivy.clock import Clock
from kivy.graphics import Color, Ellipse, Line
from kivy.core.audio import SoundLoader
from kivy.uix.label import Label
from kivy.animation import Animation

from src.models.player import Player
from src.models.dot import Dot
from src.models.twister import Twister
from src.models.power_up import PowerUp
from src.utils.achievements import AchievementManager
from src.constants import *
from src.audio_manager import audio_manager

import math
import random

class GameScreen(Screen):
    player = ObjectProperty(None)
    score = NumericProperty(0)
    time = NumericProperty(0)
    game_over = False
    difficulty_multiplier = 1
    
    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)
        self.player = Player()
        self.dots = []
        self.power_ups = []
        self.twister = Twister()
        self.score = 0
        self.time = 0
        self.game_over = False
        self.clockwise = True
        self.difficulty_multiplier = 1
        self.frames_since_last_spawn = 0
        self.collect_sound = SoundLoader.load('collect.wav')
        self.game_over_sound = SoundLoader.load('game_over.wav')
        self.achievement_manager = AchievementManager()
        self.score_label = Label(text="Score: 0", pos_hint={'top': 1, 'right': 1})
        self.add_widget(self.score_label)
        Clock.schedule_interval(self.update, 1.0/60.0)

    def on_size(self, *args):
        self.draw()
        self.player.update_position()
        self.twister.center = self.center
        for dot in self.dots:
            dot.update_position()
        for power_up in self.power_ups:
            power_up.update_position()

    def on_enter(self):
        self.reset_game()
        audio_manager.play_background_music()
        if not self.player.parent:
            self.add_widget(self.player)
        if not self.twister.parent:
            self.add_widget(self.twister)
        self.twister.center = self.center

    def on_leave(self):
        audio_manager.pause_background_music()

    def reset_game(self):
        self.player.reset()
        for dot in self.dots:
            self.remove_widget(dot)
        self.dots = []
        for power_up in self.power_ups:
            self.remove_widget(power_up)
        self.power_ups = []
        self.score = 0
        self.time = 0
        self.game_over = False
        self.clockwise = True
        self.difficulty_multiplier = 1
        self.frames_since_last_spawn = 0
        self.score_label.text = f"Score: {self.score}"

    def on_touch_down(self, touch):
        if not self.game_over:
            self.clockwise = not self.clockwise

    def get_property_value(self, obj, prop_name):
        prop = getattr(obj, prop_name)
        if isinstance(prop, (int, float)):
            return prop
        elif hasattr(prop, 'get'):
            return prop.get(obj)
        else:
            return getattr(obj, f'_{prop_name}', 0)

    def update(self, dt):
        if self.game_over:
            return

        self.time += dt
        self.player.move(self.clockwise, self.difficulty_multiplier)
        self.update_dots()
        self.update_power_ups()
        self.spawn_new_dot()
        self.spawn_new_power_up()
        self.twister.update(dt)
        self.difficulty_multiplier *= DIFFICULTY_INCREASE_RATE


        # Check for achievements
        unlocked_achievements = self.achievement_manager.update(self)
        for achievement in unlocked_achievements:
            self.show_achievement_notification(achievement)

    def spawn_new_dot(self):
        self.frames_since_last_spawn += 1
        if self.frames_since_last_spawn >= DOT_SPAWN_RATE:
            new_dot = Dot()
            self.add_widget(new_dot)
            self.dots.append(new_dot)
            self.frames_since_last_spawn = 0

    def update_dots(self):
        for dot in self.dots[:]:
            dot.move(self.difficulty_multiplier)
            if dot.distance > RING_RADIUS + DOT_RADIUS:
                self.remove_widget(dot)
                self.dots.remove(dot)
            elif self.collides(self.player, dot):
                if dot.good:
                    audio_manager.play_sound('collect')
                    self.score += 1
                    self.player.increase_combo()
                    self.remove_widget(dot)
                    self.dots.remove(dot)
                else:
                    audio_manager.play_sound('game_over')
                    self.game_over = True

    def collides(self, obj1, obj2):
        obj1_x = self.get_property_value(obj1, 'center_x')
        obj1_y = self.get_property_value(obj1, 'center_y')
        obj2_x = self.get_property_value(obj2, 'center_x')
        obj2_y = self.get_property_value(obj2, 'center_y')
        obj1_radius = self.get_property_value(obj1, 'radius')
        obj2_radius = self.get_property_value(obj2, 'radius')

        distance = math.hypot(obj1_x - obj2_x, obj1_y - obj2_y)
        return distance < obj1_radius + obj2_radius

    def update_positions(self):
        # Update positions of game elements based on new screen size
        self.ring_pos = (self.width / 2, self.height / 2)
        self.player.update_position()
        for dot in self.dots:
            dot.update_position()
        for power_up in self.power_ups:
            power_up.update_position()
        self.twister.pos = self.ring_pos

    def spawn_new_power_up(self):
        if random.random() < POWER_UP_SPAWN_CHANCE:
            new_power_up = PowerUp()
            self.add_widget(new_power_up)
            self.power_ups.append(new_power_up)

    def update_power_ups(self):
        for power_up in self.power_ups[:]:
            power_up.move(self.difficulty_multiplier)
            if power_up.distance > RING_RADIUS + POWER_UP_RADIUS:
                self.remove_widget(power_up)
                self.power_ups.remove(power_up)
            elif self.collides(self.player, power_up):
                power_up.activate(self.player)
                self.remove_widget(power_up)
                self.power_ups.remove(power_up)

    def draw(self):
        self.canvas.clear()
        with self.canvas:
            # Draw ring
            Color(1, 1, 1)
            Line(circle=(self.center_x, self.center_y, RING_RADIUS), width=2)

            # Draw twister
            self.twister.draw()

            # Draw player
            self.player.draw()

            # Draw dots
            for dot in self.dots:
                dot.draw()

            # Draw power-ups
            for power_up in self.power_ups:
                power_up.draw()