from abc import ABC, abstractmethod
from typing import Any

class BaseParser(ABC):
    def __init__(self):
        self.cache = {}
        
    @abstractmethod
    def setup(self, **kwargs) -> None:
        pass
        
    @abstractmethod
    def parse(self, data: Any) -> Any:
        pass

    @abstractmethod
    def parse_file(self, file_path: str) -> bool:
        pass
    
    
    
    