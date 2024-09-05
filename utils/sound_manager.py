class SoundManager:
    def __init__(self, asset_manager):
        self.asset_manager = asset_manager
        self.music = self.asset_manager.get_sound('background_music.mp3')
        self.collect_sound = self.asset_manager.get_sound('collect.wav')
        self.game_over_sound = self.asset_manager.get_sound('game_over.wav')
        self.menu_select_sound = self.asset_manager.get_sound('select.wav')
        self.menu_click_sound = self.asset_manager.get_sound('click.wav')
        self.powerup_sound = self.asset_manager.get_sound('powerup.wav')
        self.direction_change_sound = self.asset_manager.get_sound('direction_change.wav')

        self.master_volume = 0.75
        self.music_volume = 0.03
        self.sfx_volume = 0.3

        if self.music:
            self.music.loop = True

        self.update_volumes()

    def start_background_music(self):
        if self.music:
            self.music.play()

    def stop_background_music(self):
        if self.music:
            self.music.stop()

    def play_collect(self):
        if self.collect_sound:
            self.collect_sound.play()

    def play_game_over(self):
        if self.game_over_sound:
            self.game_over_sound.play()

    def play_menu_select(self):
        if self.menu_select_sound:
            self.menu_select_sound.play()

    def play_menu_click(self):
        if self.menu_click_sound:
            self.menu_click_sound.play()

    def play_powerup(self):
        if self.powerup_sound:
            self.powerup_sound.play()

    def play_direction_change(self):
        if self.direction_change_sound:
            self.direction_change_sound.play()

    def update_volumes(self):
        if self.music:
            self.music.volume = self.master_volume * self.music_volume
        for sound in [self.collect_sound, self.game_over_sound, self.menu_select_sound, self.menu_click_sound, self.powerup_sound, self.direction_change_sound]:
            if sound:
                sound.volume = self.master_volume * self.sfx_volume

    def set_master_volume(self, volume):
        self.master_volume = max(0, min(1, volume))
        self.update_volumes()

    def set_music_volume(self, volume):
        self.music_volume = max(0, min(1, volume))
        self.update_volumes()

    def set_sfx_volume(self, volume):
        self.sfx_volume = max(0, min(1, volume))
        self.update_volumes()