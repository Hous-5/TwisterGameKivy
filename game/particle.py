from kivy.graphics import Color, Ellipse
import random
import math
import config

class KivyParticle:
    def __init__(self, x, y, color, scale_factor, particle_type='default'):
        self.x = x
        self.y = y
        self.color = color
        self.scale_factor = scale_factor
        self.particle_type = particle_type
        self.radius = random.uniform(1, 3) * self.scale_factor
        self.speed = random.uniform(*config.PARTICLE_SPEED_RANGE) * self.scale_factor
        self.angle = random.uniform(0, 2 * math.pi)
        self.lifetime = random.uniform(*config.PARTICLE_LIFETIME_RANGE)
        self.alpha = 1.0
        
        if particle_type == 'trail':
            self.speed *= 0.5
            self.lifetime *= 2
        elif particle_type == 'explosion':
            self.speed *= 2
            self.lifetime *= 0.5

    def update(self, dt):
        self.x += math.cos(self.angle) * self.speed * dt
        self.y += math.sin(self.angle) * self.speed * dt
        self.lifetime -= dt
        self.alpha = max(0, self.alpha - dt / 2)
        self.radius = max(0, self.radius - dt * self.scale_factor)
        
        if self.particle_type == 'trail':
            self.alpha = max(0, self.alpha - dt)
        elif self.particle_type == 'explosion':
            self.speed *= 0.95

    def draw(self):
        Color(*self.color[:3], self.alpha)
        Ellipse(pos=(self.x - self.radius, self.y - self.radius), size=(self.radius * 2, self.radius * 2))

class KivyParticleSystem:
    def __init__(self, scale_factor, device_optimizer):
        self.scale_factor = scale_factor
        self.device_optimizer = device_optimizer
        self.particles = []
        self.max_particles = self.device_optimizer.get_particle_count()

    def create_particles(self, x, y, color, particle_type='default'):
        for _ in range(min(self.max_particles - len(self.particles), 10)):
            self.particles.append(KivyParticle(x, y, color, self.scale_factor, particle_type))

    def create_trail(self, x, y, color):
        if len(self.particles) < self.max_particles:
            self.particles.append(KivyParticle(x, y, color, self.scale_factor, 'trail'))

    def create_explosion(self, x, y, color):
        for _ in range(min(self.max_particles - len(self.particles), 20)):
            self.particles.append(KivyParticle(x, y, color, self.scale_factor, 'explosion'))

    def update(self, dt):
        for particle in self.particles[:]:
            particle.update(dt)
            if particle.lifetime <= 0:
                self.particles.remove(particle)

    def draw(self):
        for particle in self.particles:
            particle.draw()

    def update_particle_count(self):
        self.max_particles = self.device_optimizer.get_particle_count()
        while len(self.particles) > self.max_particles:
            self.particles.pop(0)

    def reset(self):
        self.particles.clear()