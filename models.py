import json
from dataclasses import dataclass, asdict
from typing import List, Dict, Any

@dataclass
class ClickEvent:
    x: int
    y: int
    button: str  # 'left', 'right', 'middle'
    action: str  # 'press' or 'release' (we usually care about click-down/click-up or full clicks. For a simplified auto clicker, a click event represents a completed click, or a down/up pair. Let's record down and up separately or just simplify to individual clicks. Pynput mouse captures press and release. Keeping track of down and up is very powerful, as it allows dragging or long-pressing!)
    delay: float  # time in seconds since the previous event (0.0 for first)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ClickEvent':
        return cls(
            x=data['x'],
            y=data['y'],
            button=data['button'],
            action=data['action'],
            delay=data['delay']
        )

class Sequence:
    def __init__(self, name: str = "Untitled Sequence", events: List[ClickEvent] = None):
        self.name = name
        self.events: List[ClickEvent] = events if events is not None else []

    def clear(self):
        self.events.clear()

    def add_event(self, event: ClickEvent):
        self.events.append(event)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "events": [e.to_dict() for e in self.events]
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Sequence':
        seq = cls(name=data.get("name", "Untitled Sequence"))
        seq.events = [ClickEvent.from_dict(e) for e in data.get("events", [])]
        return seq

    def save_to_file(self, filepath: str):
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=4)

    @classmethod
    def load_from_file(cls, filepath: str) -> 'Sequence':
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return cls.from_dict(data)
