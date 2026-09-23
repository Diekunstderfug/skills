class Cart:
    def __init__(self, items):
        self.items = list(items)
        self.item_count = len(items)

    def remove(self, item):
        self.items.remove(item)
