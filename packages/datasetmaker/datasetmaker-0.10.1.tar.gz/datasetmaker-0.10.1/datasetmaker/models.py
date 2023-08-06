from pathlib import Path
from typing import Union
from abc import ABC, abstractmethod
import pandas as pd


class Client(ABC):
    @abstractmethod
    def get(self) -> Union[pd.DataFrame, dict, list]:
        pass

    @abstractmethod
    def save(self,
             path: Union[Path, str],
             recursive_concepts: bool = True,
             **kwargs: str) -> None:
        pass
