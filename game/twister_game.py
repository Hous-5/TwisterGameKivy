from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Rectangle, Line, PushMatrix, PopMatrix, Rotate
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.label import Label
from game.player import KivyPlayer
from game.dot import KivyDot
from game.twister import KivyTwister
from game.power_up import KivyPowerUpManager
from game.particle import KivyParticleSystem
from game.background_particle import KivyBackgroundParticle
from utils.haptic_feedback import HapticFeedback
from utils.sound_manager import SoundManager
from utils.asset_manager import AssetManager
from utils.device_optimizer import DeviceOptimizer
from kivy.app import App
import math
import random

class TwisterGame(Widget):
    def __init__(self, sound_manager, asset_manager, device_optimizer, **kwargs):
        super(TwisterGame, self).__init__(**kwargs)
        self.sound_manager = sound_manager
        self.asset_manager = asset_manager
        self.device_optimizer = device_optimizer
        self.haptic_feedback = HapticFeedback()  # Initialize HapticFeedback
        
        self.bind(size=self.setup_game)
        self.setup_game()

    def setup_game(self, *args):
        self.center_x = self.width / 2
        self.center_y = self.height / 2
        self.scale_factor = min(self.width, self.height) / 848
        self.ring_radius = min(self.width, self.height) // 3
        self.ring_thickness = max(2, int(3 * self.scale_factor))
        self.score = 0
        self.game_over = False
        self.clockwise = True
        self.difficulty_multiplier = 1
        self.frames_since_last_spawn = 0
        self.time = 0

        if hasattr(self, 'player'):
            self.remove_widget(self.player)
        self.player = KivyPlayer(self.center_x, self.center_y, self.ring_radius, self.scale_factor, self.asset_manager)
        self.add_widget(self.player)

        self.dots = []

        if hasattr(self, 'twister'):
            self.remove_widget(self.twister)
        self.twister = KivyTwister(self.center_x, self.center_y, self.asset_manager)
        self.add_widget(self.twister)
        
        self.power_up_manager = KivyPowerUpManager(self.center_x, self.center_y, self.ring_radius, self.device_optimizer)
        self.particle_system = KivyParticleSystem(self.scale_factor, self.device_optimizer)

        if hasattr(self, 'score_label'):
            self.remove_widget(self.score_label)
        self.score_label = Label(
            text="Score: 0",
            font_size=dp(20 * self.scale_factor),
            pos_hint={'center_x': 0.5, 'top': 0.95},
            size_hint=(None, None)
        )
        self.add_widget(self.score_label)

        self.background_particles = [KivyBackgroundParticle(self.width, self.height) 
                                     for _ in range(self.device_optimizer.get_background_particle_count())]

        if not hasattr(self, '_update_scheduled'):
            Clock.schedule_interval(self.update, 1.0/60.0)  # 60 FPS
            self._update_scheduled = True

    def on_touch_down(self, touch):
        if not self.game_over:
            self._touch_start_pos = touch.pos
            self._touch_start_time = touch.time_start
        return super(TwisterGame, self).on_touch_down(touch)

    def on_touch_up(self, touch):
        if not self.game_over and hasattr(self, '_touch_start_pos'):
            distance = math.hypot(touch.x - self._touch_start_pos[0], touch.y - self._touch_start_pos[1])
            duration = touch.time_end - self._touch_start_time

            if distance < dp(30) and duration < 0.3:
                self.clockwise = not self.clockwise
                self.power_up_manager.check_powerup_collection(touch.pos)
                self.haptic_feedback.vibrate()  # This should now work correctly

            self._touch_start_pos = None
            self._touch_start_time = None
        return super(TwisterGame, self).on_touch_up(touch)

    def spawn_new_dot(self):
        self.frames_since_last_spawn += 1
        if self.frames_since_last_spawn >= 10:  # Adjust as needed
            self.dots.append(KivyDot(self.center_x, self.center_y, self.ring_radius, self.scale_factor))
            self.frames_since_last_spawn = 0

    def update(self, dt):
        if not self.game_over:
            self.time += dt
            self.player.move(self.clockwise, self.difficulty_multiplier)
            self.update_dots()
            self.spawn_new_dot()
            self.difficulty_multiplier *= 1.0002  # Adjust as needed
            self.power_up_manager.update(self.player, self.difficulty_multiplier, dt)
            self.particle_system.update(dt)
            self.twister.update(dt)

            for particle in self.background_particles:
                particle.move()

        self.canvas.clear()
        with self.canvas:
            # Draw background
            Color(0.12, 0.12, 0.12)
            Rectangle(pos=self.pos, size=self.size)
            
            # Draw background particles
            for particle in self.background_particles:
                particle.draw()

            # Draw ring
            Color(1, 1, 1)
            Line(circle=(self.center_x, self.center_y, self.ring_radius), width=self.ring_thickness)
            
            # Draw power-ups
            self.power_up_manager.draw()
            
            # Draw dots
            for dot in self.dots:
                dot.draw()
            
            # Draw particles
            self.particle_system.draw()

        # Update score label
        self.score_label.text = f"Score: {self.score}"
        self.score_label.texture_update()
        self.score_label.size = self.score_label.texture_size

    def update_dots(self):
        for dot in self.dots[:]:
            dot.move(self.difficulty_multiplier)
            if dot.distance > self.ring_radius + 8:  # Adjust radius as needed
                self.dots.remove(dot)
            elif self.player.collides_with(dot):
                if dot.good:
                    self.score += int(1 * self.player.get_score_multiplier())
                    self.player.increase_combo()
                    self.app.sound_manager.play_collect()
                    self.particle_system.create_particles(dot.x, dot.y, (0, 1, 0, 1))  # Green particles
                    self.dots.remove(dot)
                else:
                    self.game_over = True
                    self.particle_system.create_particles(dot.x, dot.y, (1, 0, 0, 1))  # Red particles
                    self.app.sound_manager.play_game_over()
                    self.app.show_game_over(self.score)

    def update_background_particles(self):
        count = self.device_optimizer.get_background_particle_count()
        self.background_particles = [KivyBackgroundParticle(self.width, self.height) for _ in range(count)]