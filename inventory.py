from abstract_classes import AbstractInventory

class Inventory(AbstractInventory):
    def __init__(self, items=None):
        if items is not None:
            self.items = items
        else:
            self.items = []
            
    def add_item(self, item):
        self.items.append(item)

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)
            return True
        return False

    def has_item(self, item):
        return item in self.items

    def list_items(self):
        if not self.items:
            return "Inventory is empty."
        return "Inventory: " + ", ".join(self.items)

    def to_list(self):
        return self.items

    def from_list(self, items):
        self.items = items
