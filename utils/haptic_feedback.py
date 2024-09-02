from kivy.utils import platform

class HapticFeedback:
    def __init__(self):
        self.vibrator = None
        if platform == 'android':
            from android.vibrator import vibrate
            self.vibrate = vibrate
        elif platform == 'ios':
            from pyobjus import autoclass
            self.UIImpactFeedbackGenerator = autoclass('UIImpactFeedbackGenerator').alloc().initWithStyle_(0)

    def vibrate(self, duration=50):
        if platform == 'android':
            self.vibrate(duration / 1000.0)  # Android expects seconds
        elif platform == 'ios':
            self.UIImpactFeedbackGenerator.impactOccurred()
        else:
            print(f"Vibration not supported on {platform}")