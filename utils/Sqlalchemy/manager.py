
class BaseManager:
    def __init__(self, model, session_factory):
        self.model = model
        self.session_factory = session_factory
