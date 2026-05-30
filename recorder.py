import time
from typing import List, Callable, Optional
from pynput import mouse
from models import ClickEvent

class Recorder:
    def __init__(self, on_event_callback: Optional[Callable[[ClickEvent], None]] = None):
        self.events: List[ClickEvent] = []
        self.listener: Optional[mouse.Listener] = None
        self.last_event_time: Optional[float] = None
        self.on_event_callback = on_event_callback
        self.is_recording = False

    def _on_click(self, x: int, y: int, button: mouse.Button, pressed: bool):
        if not self.is_recording:
            return False  # Stops listener if recording is false

        current_time = time.time()
        
        # Calculate delay since last click
        if self.last_event_time is None:
            delay = 0.0
        else:
            delay = current_time - self.last_event_time
            
        self.last_event_time = current_time

        # Map pynput Button to string representation
        btn_str = button.name  # 'left', 'right', etc.
        action_str = 'press' if pressed else 'release'

        event = ClickEvent(
            x=x,
            y=y,
            button=btn_str,
            action=action_str,
            delay=delay
        )
        
        self.events.append(event)

        # Notify callback in UI thread context
        if self.on_event_callback:
            self.on_event_callback(event)

    def start(self):
        if self.is_recording:
            return
            
        self.is_recording = True
        self.last_event_time = None
        
        # Start a new non-blocking listener thread
        self.listener = mouse.Listener(on_click=self._on_click)
        self.listener.start()

    def stop(self):
        self.is_recording = False
        if self.listener:
            self.listener.stop()
            self.listener = None

    def clear(self):
        self.events.clear()
        self.last_event_time = None
