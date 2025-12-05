from abc import ABC, abstractmethod

class LogHistorico(ABC):
    
    @abstractmethod
    def save_log(self, filename: str):
        pass
