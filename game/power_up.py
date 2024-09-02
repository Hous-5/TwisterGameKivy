from kivy.graphics import Color, Ellipse
import random
import math

class KivyPowerUp:
    def __init__(self, center_x, center_y, ring_radius):
        self.center_x = center_x
        self.center_y = center_y
        self.angle = random.uniform(0, 2 * math.pi)
        self.distance = 50
        self.type = random.choice(["speed", "score", "invincibility"])
        self.radius = 8  # Adjust as needed
        self.duration = 5  # seconds
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
        if self.type == "speed":
            Color(0, 0, 1)  # Blue
        elif self.type == "score":
            Color(0.5, 0, 0.5)  # Purple
        else:  # invincibility
            Color(1, 0.5, 0)  # Orange
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
        if random.random() < 0.02:  # 2% chance to spawn a power-up each frame
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
            player.speed_multiplier = 2
        elif power_up.type == "score":
            player.score_multiplier = 2
        elif power_up.type == "invincibility":
            player.invincible = True

    def deactivate_power_up(self, player):
        if self.active_power_up.type == "speed":
            player.speed_multiplier = 1
        elif self.active_power_up.type == "score":
            player.score_multiplier = 1
        elif self.active_power_up.type == "invincibility":
            player.invincible = False
        self.active_power_up = None

    def draw(self):
        for power_up in self.power_ups:
            power_up.draw()

    def check_powerup_collection(self, touch_pos):
        for powerup in self.power_ups[:]:
            if math.hypot(touch_pos[0] - powerup.x, touch_pos[1] - powerup.y) < powerup.radius:
                self.activate_power_up(powerup, self.game.player)
                self.power_ups.remove(powerup)