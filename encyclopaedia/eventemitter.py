class EventEmitter:
    def __init__(self) -> None:
        self.callbacks: dict[str, list] = {}

    def on(self, ev_name: str):
        """Decorator to register a new callback function to an event."""
        def wrapper(callback):
            self.callbacks[ev_name] = self.callbacks.get(ev_name, [])
            self.callbacks[ev_name].append(callback)

        return wrapper

    def emit(self, ev_name: str) -> None:
        """Emit an event, triggered every callback registered to it."""
        for callback in self.callbacks[ev_name]:
            callback(self)
