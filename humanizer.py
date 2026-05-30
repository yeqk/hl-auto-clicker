import random
import time
from typing import Tuple

class Humanizer:
    def __init__(self, timing_variance: float = 0.15, position_jitter: int = 3, pause_chance: float = 0.02):
        """
        timing_variance: float (0.0 to 1.0) - Max percentage to vary click timings. e.g. 0.15 = ±15% variation.
        position_jitter: int - Max pixel radius to offset coordinates. e.g. 3 = coordinate ±3 pixels.
        pause_chance: float (0.0 to 1.0) - Chance to introduce a random extra micro-pause during execution.
        """
        self.timing_variance = timing_variance
        self.position_jitter = position_jitter
        self.pause_chance = pause_chance

    def jitter_delay(self, delay: float) -> float:
        """Applies random percentage variance to the delay and checks for micro-pauses."""
        if delay <= 0:
            return 0.0
        
        # Calculate random variance
        variance_factor = random.uniform(-self.timing_variance, self.timing_variance)
        jittered = delay * (1.0 + variance_factor)
        
        # Ensure it doesn't become negative
        jittered = max(0.001, jittered)
        
        # Check for occasional micro-pause
        if random.random() < self.pause_chance:
            # 50ms to 250ms extra pause
            micro_pause = random.uniform(0.05, 0.25)
            jittered += micro_pause
            
        return jittered

    def jitter_position(self, x: int, y: int) -> Tuple[int, int]:
        """Applies a small physical offset to mimic human click inaccuracy."""
        if self.position_jitter <= 0:
            return x, y
            
        dx = random.randint(-self.position_jitter, self.position_jitter)
        dy = random.randint(-self.position_jitter, self.position_jitter)
        
        # Make sure values don't go out of bounds (handled safely or left as is; desktop coordinate margins are huge)
        return max(0, x + dx), max(0, y + dy)
