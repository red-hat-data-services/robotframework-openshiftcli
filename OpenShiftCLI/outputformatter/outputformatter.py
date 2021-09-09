from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union


class OutputFormatter(ABC):

    @abstractmethod
    def format(self,
               output: Union[Dict[str, Any], List[Dict[str, Any]]],
               message: Optional[str] = "" ,
               type: Optional[str] = None) -> str:
        pass
