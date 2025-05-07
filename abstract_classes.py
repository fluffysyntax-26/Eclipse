from abc import ABC, abstractmethod

class AbstractPlayer(ABC):
    @abstractmethod
    def ask_choice(self):
        pass

    @abstractmethod
    def save_game(self):
        pass

    @abstractmethod
    def load_saved_game(self):
        pass

    @abstractmethod
    def pause_menu(self):
        pass

class AbstractInventory(ABC):
    @abstractmethod
    def add_item(self, item):
        pass

    @abstractmethod
    def remove_item(self, item):
        pass

    @abstractmethod
    def has_item(self, item):
        pass

    @abstractmethod
    def list_items(self):
        pass
