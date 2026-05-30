from typing import Callable, Optional
from pynput import keyboard

class HotkeyManager:
    def __init__(self, 
                 on_record_toggle: Callable[[], None], 
                 on_play_toggle: Callable[[], None]):
        self.on_record_toggle = on_record_toggle
        self.on_play_toggle = on_play_toggle
        self.listener: Optional[keyboard.Listener] = None

    def start(self):
        if self.listener is not None:
            return
            
        # Start the global key listener thread
        self.listener = keyboard.Listener(on_press=self._on_press)
        self.listener.start()

    def stop(self):
        if self.listener:
            self.listener.stop()
            self.listener = None

    def _on_press(self, key):
        try:
            # We want to match key presses of F6, F7
            if key == keyboard.Key.f6:
                self.on_record_toggle()
            elif key == keyboard.Key.f7:
                self.on_play_toggle()
        except AttributeError:
            # Non-special key pressed (does not have .name or similar)
            pass
        except Exception as e:
            print(f"Hotkey handler error: {e}")
