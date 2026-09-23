class Screen:
    def open(self, app):
        app.tasks.append(app.spawn(self.poll))

    async def poll(self):
        ...

    def close(self):
        pass
