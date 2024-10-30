from abc import ABC, abstractmethod
from typing import Any

class BaseParser(ABC):


    @abstractmethod
    def parse(self, data: Any) -> Any:
        pass