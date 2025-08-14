from abc import ABC, abstractmethod

import pandas as pd


class DataSource(ABC):
    @abstractmethod
    def fetch(self, **kwargs) -> pd.DataFrame: ...

    @abstractmethod
    def transform(self, df: pd.DataFrame) -> pd.DataFrame: ...

    @abstractmethod
    def name(self) -> str: ...
