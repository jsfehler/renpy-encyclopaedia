class MockPersistent(object):
    """Mock Ren'Py Persistent"""
    def __getattr__(self, attr):
        # Undefined attributes return None.
        if attr.startswith("__") and attr.endswith("__"):
            raise AttributeError("Persistent object has no attribute %r", attr)

        return None


persistent = MockPersistent()
