from abc import ABC, abstractmethod
from typing import Any

class BaseParser(ABC):

    def __init__(self, **kwargs) -> None:
        self.setup(**kwargs)
        
    @abstractmethod
    def setup(self, **kwargs) -> None:
        pass
        
    @abstractmethod
    def parse(self, data: Any) -> Any:
        pass