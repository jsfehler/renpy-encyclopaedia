"""renpy
init -85 python:
"""
from typing import Callable


CALLBACK_TYPE = Callable[['EventEmitter'], None]


class EventEmitter:
    def __init__(self) -> None:
        self.callbacks: dict[str, list[CALLBACK_TYPE]] = {}

    def on(self, ev_name: str) -> Callable[[CALLBACK_TYPE], CALLBACK_TYPE]:
        """Decorator to register a new callback function to an event."""

        def wrapper(callback: CALLBACK_TYPE) -> CALLBACK_TYPE:
            self.callbacks[ev_name] = self.callbacks.get(ev_name, [])
            self.callbacks[ev_name].append(callback)

            return callback

        return wrapper

    def emit(self, ev_name: str) -> None:
        """Emit an event and trigger every callback registered to it."""
        for callback in self.callbacks[ev_name]:
            callback(self)
