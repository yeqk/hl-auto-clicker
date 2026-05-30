import time
import threading
from typing import List, Callable, Optional
import pyautogui
from models import ClickEvent
from humanizer import Humanizer

class Player:
    def __init__(self, humanizer: Optional[Humanizer] = None, 
                 on_loop_complete: Optional[Callable[[int], None]] = None,
                 on_stopped: Optional[Callable[[], None]] = None):
        self.events: List[ClickEvent] = []
        self.humanizer = humanizer if humanizer is not None else Humanizer()
        self.on_loop_complete = on_loop_complete
        self.on_stopped = on_stopped
        self.is_playing = False
        self.loop_delay = 2.0  # Customizable delay between loops (in seconds)
        self.thread: Optional[threading.Thread] = None
        
        # PyAutoGUI safety configuration
        pyautogui.FAILSAFE = True  # Drag mouse to upper-left corner to abort
        pyautogui.PAUSE = 0.0  # Remove pyautogui's default latency between actions

    def start(self, events: List[ClickEvent]):
        if self.is_playing or not events:
            return
            
        self.events = events
        self.is_playing = True
        self.thread = threading.Thread(target=self._run_loop, daemon=True)
        self.thread.start()

    def stop(self):
        self.is_playing = False
        # Do not join here as it might block the main UI thread if called from it.
        # The background loop will exit naturally upon checking self.is_playing.

    def _run_loop(self):
        loop_count = 0
        try:
            while self.is_playing:
                for idx, event in enumerate(self.events):
                    if not self.is_playing:
                        break

                    # 1. Apply Jitter to delay
                    # If it's the very first event in the FIRST loop, delay might be zero.
                    # On subsequent runs of the loop, the first click has a delay to space it from the previous click sequence end.
                    # We can use the recorded delay.
                    delay = event.delay
                    # If this is the start of the loop (not first loop) and it's the first click,
                    # we use the customizable loop delay to space iterations.
                    if idx == 0 and loop_count > 0:
                        delay = max(delay, self.loop_delay)

                    jittered_delay = self.humanizer.jitter_delay(delay)
                    if jittered_delay > 0:
                        time.sleep(jittered_delay)

                    # 2. Apply Jitter to coordinates
                    jittered_x, jittered_y = self.humanizer.jitter_position(event.x, event.y)

                    # 3. Simulate Click action (press or release)
                    button = event.button.lower()
                    if button not in ['left', 'right', 'middle']:
                        button = 'left'

                    try:
                        if event.action == 'press':
                            pyautogui.mouseDown(x=jittered_x, y=jittered_y, button=button)
                        elif event.action == 'release':
                            pyautogui.mouseUp(x=jittered_x, y=jittered_y, button=button)
                    except pyautogui.FailSafeException:
                        # User triggered failsafe by throwing mouse to top-left corner
                        self.is_playing = False
                        break

                loop_count += 1
                if self.on_loop_complete and self.is_playing:
                    self.on_loop_complete(loop_count)
                    
        except Exception as e:
            print(f"Playback error: {e}")
        finally:
            self.is_playing = False
            if self.on_stopped:
                self.on_stopped()
