class Session:
    def __init__(self, transport):
        self.transport = transport
        self.handle = None

    def start(self):
        self.handle = self.transport.open()

    def process(self, payload):
        if self.handle is None:
            raise RuntimeError("Session not started")
        return self.transport.send(self.handle, payload)

    def finish(self):
        if self.handle is not None:
            self.transport.close(self.handle)
            self.handle = None
