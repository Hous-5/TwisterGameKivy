from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Line
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.app import App
import math

from .player import KivyPlayer
from .dot import KivyDot
from .twister import KivyTwister
from .power_up import KivyPowerUpManager
from .particle import KivyParticleSystem
from .background_particle import KivyBackgroundParticle
from .achievement_system import AchievementSystem
from utils.haptic_feedback import HapticFeedback
import config

class TwisterGame(Widget):
    def __init__(self, sound_manager, asset_manager, device_optimizer, **kwargs):
        super(TwisterGame, self).__init__(**kwargs)
        self.sound_manager = sound_manager
        self.asset_manager = asset_manager
        self.device_optimizer = device_optimizer
        self.haptic_feedback = HapticFeedback()
        
        self.game_started = False
        self.game_over = False
        self.score = 0
        self.elapsed_time = 0
        
        self.load_textures()
        
        Clock.schedule_once(self.create_game_objects, 0)
        Clock.schedule_once(self.create_ui_elements, 0)

        self.achievement_system = AchievementSystem()
        self.powerups_collected = 0
        self.difficulty = 'normal'

    def load_textures(self):
        self.twister_texture = self.asset_manager.get_texture('Center_Sun.png')
        self.player_texture = self.asset_manager.get_texture('Player.png')
        
        if self.twister_texture is None or self.player_texture is None:
            print("Warning: Textures not loaded properly")
            self.twister_texture = None
            self.player_texture = None

    def create_ui_elements(self, dt):
        # Existing UI elements (score and time labels) remain unchanged
        self.score_label = Label(
            text="Score: 0",
            font_size=dp(20),
            size_hint=(None, None),
            pos=(dp(10), self.height - dp(40))
        )
        self.add_widget(self.score_label)

        self.time_label = Label(
            text="Time: 0:00",
            font_size=dp(20),
            size_hint=(None, None),
            pos=(self.width / 2 - dp(40), self.height - dp(40))
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

    def set_difficulty(self, difficulty):
        self.difficulty = difficulty
        difficulty_settings = config.DIFFICULTY_LEVELS[difficulty]
        self.difficulty_multiplier = difficulty_settings['multiplier']
        self.spawn_rate = difficulty_settings['spawn_rate']

    def start_game(self):
        if not self.game_started:
            self.set_difficulty(self.difficulty)
            self.game_started = True
            self.game_over = False
            self.score = 0
            self.elapsed_time = 0
            self.powerups_collected = 0
            self.update_score_label()
            self.update_time_label()
            Clock.schedule_interval(self.update, 1.0/60.0)
            self.sound_manager.start_background_music()

    def update_score_label(self):
        if hasattr(self, 'score_label'):
            self.score_label.text = f"Score: {self.score}"
            self.score_label.texture_update()
            self.score_label.size = self.score_label.texture_size
            self.score_label.pos = (dp(10), self.height - self.score_label.height - dp(10))

    def update_time_label(self):
        if hasattr(self, 'time_label'):
            minutes = int(self.elapsed_time // 60)
            seconds = int(self.elapsed_time % 60)
            self.time_label.text = f"Time: {minutes}:{seconds:02d}"
            self.time_label.texture_update()
            self.time_label.size = self.time_label.texture_size
            self.time_label.pos = (self.width / 2 - self.time_label.width / 2, self.height - self.time_label.height - dp(10))

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
            self.particle_system.create_trail(self.player.center_x, self.player.center_y, (1, 1, 1, 0.5))

            for particle in self.background_particles:
                particle.move()

            self.update_score_label()
            self.update_time_label()

            game_state = {
                'score': self.score,
                'combo': self.player.combo,
                'time': self.elapsed_time,
                'powerups': self.powerups_collected,
                'lives': 3  # Assuming the game has lives, adjust as needed
            }
            self.achievement_system.check_achievements(game_state)

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
            self.draw_combo()
            self.draw_active_power_up()

        # Ensure labels are on top
        self.remove_widget(self.score_label)
        self.remove_widget(self.time_label)
        self.add_widget(self.score_label)
        self.add_widget(self.time_label)

    def draw_background(self):
        Color(*config.BACKGROUND_COLOR)
        Rectangle(pos=self.pos, size=self.size)
        for particle in self.background_particles:
            particle.draw()

    def draw_ring(self):
        Color(*config.RING_COLOR)
        Line(circle=(self.center_x, self.center_y, self.ring_radius), width=self.ring_thickness)

    def spawn_new_dot(self):
        self.frames_since_last_spawn += 1
        if self.frames_since_last_spawn >= self.spawn_rate:
            self.dots.append(KivyDot(self.center_x, self.center_y, self.ring_radius, self.scale_factor))
            self.frames_since_last_spawn = 0

    def update_dots(self):
        for dot in self.dots[:]:
            dot.move(self.difficulty_multiplier)
            if dot.distance > self.ring_radius + 20:  # Remove dots that are too far
                self.dots.remove(dot)
            elif self.player.collides_with(dot):
                if dot.good:
                    self.score += int(1 * self.player.get_score_multiplier())
                    self.player.increase_combo()
                    self.sound_manager.play_collect()
                    self.particle_system.create_explosion(dot.x, dot.y, (0, 1, 0, 1))  # Green explosion
                    self.dots.remove(dot)
                else:
                    if not self.player.invincible:
                        self.game_over = True
                        self.particle_system.create_explosion(dot.x, dot.y, (1, 0, 0, 1))  # Red explosion
                        self.sound_manager.play_game_over()
                        Clock.schedule_once(self.end_game, 2)
                    else:
                        self.particle_system.create_explosion(dot.x, dot.y, (1, 0.5, 0, 1))  # Orange explosion for invincibility hit
                        self.dots.remove(dot)

    def end_game(self, dt):
        self.sound_manager.stop_background_music()
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
                self.sound_manager.play_direction_change()
                self.power_up_manager.check_powerup_collection(touch.pos, self.player)
                self.haptic_feedback.vibrate()

            self._touch_start_pos = None
            self._touch_start_time = None
            return True
        return super(TwisterGame, self).on_touch_up(touch)

    def pause_game(self, instance):
        if self.game_started and not self.game_over:
            Clock.unschedule(self.update)
            App.get_running_app().show_pause_menu()

    def show_settings(self, instance):
        if self.game_started and not self.game_over:
            Clock.unschedule(self.update)
        App.get_running_app().show_settings()

    def resume_game(self):
        if self.game_started and not self.game_over:
            Clock.schedule_interval(self.update, 1.0/60.0)


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
        self.powerups_collected = 0
        self.update_score_label()
        self.update_time_label()

    def draw_combo(self):
        if self.player.combo > 1:
            with self.canvas:
                Color(*config.COMBO_TEXT_COLOR)
                combo_text = f"Combo x{self.player.combo}"
                combo_label = Label(text=combo_text, font_size=dp(20))
                combo_label.texture_update()
                Rectangle(texture=combo_label.texture, pos=(self.player.center_x - combo_label.texture_size[0] / 2, 
                                                            self.player.center_y + self.player.radius * 2), 
                          size=combo_label.texture_size)

    def draw_active_power_up(self):
        if self.power_up_manager.active_power_up:
            with self.canvas:
                Color(*config.POWER_UP_COLORS[self.power_up_manager.active_power_up.type])
                power_up_text = f"{self.power_up_manager.active_power_up.type.capitalize()} Active!"
                power_up_label = Label(text=power_up_text, font_size=dp(18))
                power_up_label.texture_update()
                Rectangle(texture=power_up_label.texture, 
                          pos=(self.width - power_up_label.texture_size[0] - dp(10), 
                               self.height - power_up_label.texture_size[1] - dp(50)), 
                          size=power_up_label.texture_size)

    def collect_powerup(self):
        self.powerups_collected += 1

    def update_background_particles(self):
        new_count = self.device_optimizer.get_background_particle_count()
        current_count = len(self.background_particles)
        if new_count > current_count:
            for _ in range(new_count - current_count):
                self.background_particles.append(KivyBackgroundParticle(self.width, self.height))
        elif new_count < current_count:
            self.background_particles = self.background_particles[:new_count]