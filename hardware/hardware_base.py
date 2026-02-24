from abc import ABC, abstractmethod

class BaseSensor(ABC):
    @abstractmethod
    def read(self):
        """Read sensor data."""
        pass

class BaseFeedback(ABC):
    @abstractmethod
    def alert(self, message=None):
        """Trigger feedback."""
        pass

    @abstractmethod
    def stop(self):
        """Stop feedback."""
        pass
