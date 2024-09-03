# Game settings
INITIAL_GRAPHICS_QUALITY = 1
INITIAL_MUSIC_VOLUME = 0.03
INITIAL_SFX_VOLUME = 0.3
INITIAL_VIBRATION_ENABLED = True

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
BACKGROUND_COLOR = (0.12, 0.12, 0.12, 1)
RING_COLOR = (1, 1, 1, 1)
COMBO_TEXT_COLOR = (1, 1, 0, 1)

# Game mechanics
DIFFICULTY_LEVELS = {
    'easy': {'multiplier': 0.99998, 'spawn_rate': 70},
    'normal': {'multiplier': 1.0, 'spawn_rate': 50},
    'hard': {'multiplier': 1.00002, 'spawn_rate': 30}
}

POWER_UP_TYPES = ['speed', 'score', 'invincibility']
POWER_UP_COLORS = {
    'speed': (0, 0, 1, 1),
    'score': (0.5, 0, 0.5, 1),
    'invincibility': (1, 0.5, 0, 1)
}

POWER_UP_DURATION = 5  # seconds
POWER_UP_SPAWN_CHANCE = 0.001

# Player settings
PLAYER_INITIAL_SPEED = 0.015
PLAYER_SPEED_POWERUP_MULTIPLIER = 1.5
PLAYER_SCORE_POWERUP_MULTIPLIER = 2

# Particle settings
PARTICLE_LIFETIME_RANGE = (0.5, 1.5)
PARTICLE_SPEED_RANGE = (50, 100)

# Achievement settings
ACHIEVEMENTS = [
    {
        'name': "Twister Novice",
        'description': "Score 100 points in a single game",
        'condition': lambda game_state: game_state['score'] >= 100
    },
    {
        'name': "Combo Master",
        'description': "Achieve a 10x combo",
        'condition': lambda game_state: game_state['combo'] >= 10
    },
    {
        'name': "Survivor",
        'description': "Play for 3 minutes in a single game",
        'condition': lambda game_state: game_state['time'] >= 180
    },
    {
        'name': "Power Player",
        'description': "Collect 5 power-ups in a single game",
        'condition': lambda game_state: game_state['powerups'] >= 5
    },
    {
        'name': "Perfect Run",
        'description': "Score 500 points without losing a life",
        'condition': lambda game_state: game_state['score'] >= 500 and game_state['lives'] == 3
    }
]