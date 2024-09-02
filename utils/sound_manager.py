class SoundManager:
    def __init__(self, asset_manager):
        self.asset_manager = asset_manager
        self.music = self.asset_manager.get_sound('endlessmotion.mp3')
        self.collect_sound = self.asset_manager.get_sound('collect.wav')
        self.game_over_sound = self.asset_manager.get_sound('game_over.wav')
        self.menu_select_sound = self.asset_manager.get_sound('click.wav')
        self.menu_click_sound = self.asset_manager.get_sound('click.wav')

        self.master_volume = 0.75
        self.music_volume = 0.03
        self.sfx_volume = 0.3

        if self.music:
            self.music.loop = True
            self.music.play()

        self.update_volumes()

    def update_volumes(self):
        if self.music:
            self.music.volume = self.master_volume * self.music_volume
        for sound in [self.collect_sound, self.game_over_sound, self.menu_select_sound, self.menu_click_sound]:
            if sound:
                sound.volume = self.master_volume * self.sfx_volume

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

    def set_master_volume(self, volume):
        self.master_volume = max(0, min(1, volume))
        self.update_volumes()

    def set_music_volume(self, volume):
        self.music_volume = max(0, min(1, volume))
        if self.music:
            self.music.volume = self.master_volume * self.music_volume

    def set_sfx_volume(self, volume):
        self.sfx_volume = max(0, min(1, volume))
        for sound in [self.collect_sound, self.game_over_sound, self.menu_select_sound, self.menu_click_sound]:
            if sound:
                sound.volume = self.master_volume * self.sfx_volume


    def stop_music(self):
        if self.music:
            self.music.stop()