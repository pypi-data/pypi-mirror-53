from abc import ABCMeta, abstractmethod
from enum import Enum, auto

from pandas import DataFrame


class AllergenState(Enum):
    CONTAIN = auto()  # 含む
    MAY_CONTAIN = auto()  # 製造工程で混入する可能性あり
    NOT_CONTAIN = auto()  # 含まない

    def __str__(self):
        return self.name


class BaseParser(metaclass=ABCMeta):
    @abstractmethod
    def parse(self, filename: str) -> DataFrame:
        raise NotImplementedError

    @abstractmethod
    def allergen_state_of(self, value: str) -> AllergenState:
        raise NotImplementedError
