from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Rectangle, Line
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.label import Label
from kivy.app import App
from kivy.core.window import Window
import math
import random

from game.player import KivyPlayer
from game.dot import KivyDot
from game.twister import KivyTwister
from game.power_up import KivyPowerUpManager
from game.particle import KivyParticleSystem
from game.background_particle import KivyBackgroundParticle
from utils.haptic_feedback import HapticFeedback

class TwisterGame(Widget):
    def __init__(self, sound_manager, asset_manager, device_optimizer, **kwargs):
        super(TwisterGame, self).__init__(**kwargs)
        self.sound_manager = sound_manager
        self.asset_manager = asset_manager
        self.device_optimizer = device_optimizer
        self.haptic_feedback = HapticFeedback()
        
        self.game_started = False
        self.game_over = False
        self.score = 0  # Initialize score here
        self.elapsed_time = 0
        
        self.load_textures()
        Clock.schedule_once(self.create_game_objects, 0)
        Clock.schedule_once(self.create_ui_elements, 0)

    def load_textures(self):
        self.twister_texture = self.asset_manager.get_texture('Center_Sun.png')
        self.player_texture = self.asset_manager.get_texture('Player.png')
        
        if self.twister_texture is None or self.player_texture is None:
            print("Warning: Textures not loaded properly")
            self.twister_texture = None
            self.player_texture = None

    def create_ui_elements(self, dt):
        self.score_label = Label(
            text="Score: 0",
            font_size=dp(20),
            size_hint=(None, None),
            pos=(dp(10), Window.height - dp(40))
        )
        self.add_widget(self.score_label)

        self.time_label = Label(
            text="Time: 0:00",
            font_size=dp(20),
            size_hint=(None, None),
            pos=(Window.width / 2 - dp(40), Window.height - dp(40))
        )
        self.add_widget(self.time_label)

    def create_game_objects(self, dt):
        self.center_x = self.width / 2
        self.center_y = self.height / 2
        self.scale_factor = min(self.width, self.height) / 848
        self.ring_radius = min(self.width, self.height) // 3
        self.ring_thickness = max(2, int(3 * self.scale_factor))

        self.clockwise = True
        self.difficulty_multiplier = 1
        self.frames_since_last_spawn = 0
        self.time = 0
        self.dots = []

        self.twister = KivyTwister(self.center_x, self.center_y, self.twister_texture)
        self.player = KivyPlayer(self.center_x, self.center_y, self.ring_radius, self.scale_factor, self.player_texture)
        self.power_up_manager = KivyPowerUpManager(self.center_x, self.center_y, self.ring_radius, self.device_optimizer)
        self.particle_system = KivyParticleSystem(self.scale_factor, self.device_optimizer)

        self.background_particles = [
            KivyBackgroundParticle(self.width, self.height) 
            for _ in range(self.device_optimizer.get_background_particle_count())
        ]

        print("Game objects created successfully")

    def start_game(self):
        if not self.game_started:
            self.game_started = True
            self.game_over = False
            self.score = 0
            self.elapsed_time = 0
            self.update_score_label()
            self.update_time_label()
            Clock.schedule_interval(self.update, 1.0/60.0)  # Start the game loop
            print("Game started!")

    def update_score_label(self):
        if hasattr(self, 'score_label'):
            self.score_label.text = f"Score: {self.score}"
            self.score_label.texture_update()
            self.score_label.size = self.score_label.texture_size
            self.score_label.pos = (dp(10), Window.height - self.score_label.height - dp(10))

    def update_time_label(self):
        if hasattr(self, 'time_label'):
            minutes = int(self.elapsed_time // 60)
            seconds = int(self.elapsed_time % 60)
            self.time_label.text = f"Time: {minutes}:{seconds:02d}"
            self.time_label.texture_update()
            self.time_label.size = self.time_label.texture_size
            self.time_label.pos = (Window.width / 2 - self.time_label.width / 2, Window.height - self.time_label.height - dp(10))

    def update(self, dt):
        if self.game_started and not self.game_over:
            self.elapsed_time += dt
            self.player.move(self.clockwise, self.difficulty_multiplier)
            self.update_dots()
            self.spawn_new_dot()
            self.difficulty_multiplier *= 1.0002
            self.power_up_manager.update(self.player, self.difficulty_multiplier, dt)
            self.particle_system.update(dt)
            self.twister.update(dt)

            for particle in self.background_particles:
                particle.move()

            self.update_score_label()
            self.update_time_label()

        self.canvas.clear()
        with self.canvas:
            self.draw_background()
            self.draw_ring()
            for dot in self.dots:
                dot.draw()
            self.power_up_manager.draw()
            self.particle_system.draw()
            self.twister.draw(self.canvas)
            self.player.draw(self.canvas)

        # Ensure labels are on top
        self.remove_widget(self.score_label)
        self.remove_widget(self.time_label)
        self.add_widget(self.score_label)
        self.add_widget(self.time_label)

        # Ensure labels are on top
        self.remove_widget(self.score_label)
        self.remove_widget(self.time_label)
        self.add_widget(self.score_label)
        self.add_widget(self.time_label)

    def draw_background(self):
        Color(0.12, 0.12, 0.12)  # Dark gray background
        Rectangle(pos=self.pos, size=self.size)
        for particle in self.background_particles:
            particle.draw()

    def draw_ring(self):
        Color(1, 1, 1)  # White color for the ring
        Line(circle=(self.center_x, self.center_y, self.ring_radius), width=self.ring_thickness)

    def spawn_new_dot(self):
        self.frames_since_last_spawn += 1
        if self.frames_since_last_spawn >= 60:  # Spawn a new dot every second (assuming 60 FPS)
            self.dots.append(KivyDot(self.center_x, self.center_y, self.ring_radius, self.scale_factor))
            self.frames_since_last_spawn = 0

    def update_dots(self):
        for dot in self.dots[:]:
            dot.move(self.difficulty_multiplier)
            if dot.distance > self.ring_radius + 20:  # Remove dots that are too far
                self.dots.remove(dot)
            elif self.player.collides_with(dot):
                if dot.good:
                    self.score += int(1 * self.player.get_score_multiplier())  # Update score here
                    self.player.increase_combo()
                    self.sound_manager.play_collect()
                    self.particle_system.create_particles(dot.x, dot.y, (0, 1, 0, 1))  # Green particles
                    self.dots.remove(dot)
                else:
                    self.game_over = True
                    self.particle_system.create_particles(dot.x, dot.y, (1, 0, 0, 1))  # Red particles
                    self.sound_manager.play_game_over()
                    Clock.schedule_once(self.end_game, 2)  # End the game after 2 seconds

    def end_game(self, dt):
        App.get_running_app().show_game_over(self.score)

    def on_touch_down(self, touch):
        if self.game_started and not self.game_over and self.collide_point(*touch.pos):
            self._touch_start_pos = touch.pos
            self._touch_start_time = touch.time_start
            return True
        return super(TwisterGame, self).on_touch_down(touch)

    def on_touch_up(self, touch):
        if self.game_started and not self.game_over and self.collide_point(*touch.pos) and hasattr(self, '_touch_start_pos'):
            distance = math.hypot(touch.x - self._touch_start_pos[0], touch.y - self._touch_start_pos[1])
            duration = touch.time_end - self._touch_start_time

            if distance < dp(30) and duration < 0.3:
                self.clockwise = not self.clockwise
                self.power_up_manager.check_powerup_collection(touch.pos, self.player)
                self.haptic_feedback.vibrate()

            self._touch_start_pos = None
            self._touch_start_time = None
            return True
        return super(TwisterGame, self).on_touch_up(touch)

    def pause_game(self):
        if self.game_started and not self.game_over:
            Clock.unschedule(self.update)
            print("Game paused")

    def resume_game(self):
        if self.game_started and not self.game_over:
            Clock.schedule_interval(self.update, 1.0/60.0)
            print("Game resumed")

    def on_size(self, *args):
        # Update label positions when window size changes
        self.update_score_label()
        self.update_time_label()

    def reset_game(self):
        self.game_started = False
        self.game_over = False
        self.score = 0
        self.elapsed_time = 0
        self.clockwise = True
        self.difficulty_multiplier = 1
        self.frames_since_last_spawn = 0
        self.dots.clear()
        self.player.reset()
        self.power_up_manager.reset()
        self.particle_system.reset()
        self.update_score_label()
        self.update_time_label()
        print("Game reset")

