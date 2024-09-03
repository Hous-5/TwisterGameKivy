import random
import math
from kivy.graphics import Color, Ellipse
import config

class KivyPowerUp:
    def __init__(self, center_x, center_y, ring_radius):
        self.center_x = center_x
        self.center_y = center_y
        self.angle = random.uniform(0, 2 * math.pi)
        self.distance = 50
        self.type = random.choice(config.POWER_UP_TYPES)
        self.radius = 8  # Adjust as needed
        self.duration = config.POWER_UP_DURATION
        self.update_position()

    def update_position(self):
        self.x = self.center_x + math.cos(self.angle) * self.distance
        self.y = self.center_y + math.sin(self.angle) * self.distance

    def move(self, difficulty_multiplier):
        speed = 3 * difficulty_multiplier  # Adjust base speed as needed
        self.angle += 0.02 * difficulty_multiplier
        self.distance += speed * 1.2
        self.update_position()

    def draw(self):
        Color(*config.POWER_UP_COLORS[self.type])
        Ellipse(pos=(self.x - self.radius, self.y - self.radius), size=(self.radius * 2, self.radius * 2))

class KivyPowerUpManager:
    def __init__(self, center_x, center_y, ring_radius, device_optimizer):
        self.center_x = center_x
        self.center_y = center_y
        self.ring_radius = ring_radius
        self.device_optimizer = device_optimizer
        self.power_ups = []
        self.active_power_up = None
        self.active_time = 0

    def spawn_power_up(self):
        if random.random() < config.POWER_UP_SPAWN_CHANCE:
            self.power_ups.append(KivyPowerUp(self.center_x, self.center_y, self.ring_radius))

    def update(self, player, difficulty_multiplier, dt):
        self.spawn_power_up()
        
        for power_up in self.power_ups[:]:
            power_up.move(difficulty_multiplier)
            if player.collides_with(power_up):
                self.activate_power_up(power_up, player)
                self.power_ups.remove(power_up)

        if self.active_power_up:
            self.active_time += dt
            if self.active_time >= self.active_power_up.duration:
                self.deactivate_power_up(player)

    def activate_power_up(self, power_up, player):
        self.active_power_up = power_up
        self.active_time = 0
        if power_up.type == "speed":
            player.speed_multiplier = config.PLAYER_SPEED_POWERUP_MULTIPLIER
        elif power_up.type == "score":
            player.score_multiplier = config.PLAYER_SCORE_POWERUP_MULTIPLIER
        elif power_up.type == "invincibility":
            player.activate_invincibility(power_up.duration)
        
        from kivy.app import App
        App.get_running_app().sound_manager.play_powerup()
        App.get_running_app().sm.get_screen('game').game.collect_powerup()

    def deactivate_power_up(self, player):
        if self.active_power_up.type == "speed":
            player.speed_multiplier = 1
        elif self.active_power_up.type == "score":
            player.score_multiplier = 1
        # Invincibility is handled by the player's own timer
        self.active_power_up = None

    def draw(self):
        for power_up in self.power_ups:
            power_up.draw()

    def check_powerup_collection(self, touch_pos, player):
        for powerup in self.power_ups[:]:
            if math.hypot(touch_pos[0] - powerup.x, touch_pos[1] - powerup.y) < powerup.radius:
                self.activate_power_up(powerup, player)
                self.power_ups.remove(powerup)

    def reset(self):
        self.power_ups.clear()
        self.active_power_up = None
        self.active_time = 0