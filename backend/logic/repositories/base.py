from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Optional, List

from modeller.dialects.defined import PythonDialect
from modeller import Evaluable, Dialect


__all__ = [
    'Repository',
    'MemoryRepository',
]


T = TypeVar('T')


class Repository(Generic[T], ABC):
    dialect: Dialect

    @abstractmethod
    def find_one(self, spec: Optional[Evaluable] = None) -> T: ...

    @abstractmethod
    def find(self, spec: Optional[Evaluable] = None) -> List[T]: ...

    @abstractmethod
    def save(self, model: T) -> T: ...

    @abstractmethod
    def delete(self, model: T) -> None: ...


class MemoryRepository(Repository[T]):
    dialect = PythonDialect()

    def __init__(self, primary_key: str):
        self._primary_key = primary_key
        self._cache: List[T] = []

    def find_one(self, spec: Optional[Evaluable] = None) -> T:
        result = self.find(spec)

        return result[0] if result else None

    def find(self, spec: Optional[Evaluable] = None) -> List[T]:
        return self._cache if spec is None else list(filter(self.dialect.make(spec), self._cache))

    def save(self, model: T) -> T:
        stored_model = self._get_stored_by_model(model)

        if stored_model:
            self._cache.remove(stored_model)

        self._cache.append(model)
        return model

    def delete(self, model: T) -> None:
        stored_model = self._get_stored_by_model(model)

        if stored_model:
            self._cache.remove(stored_model)

    def _get_stored_by_model(self, model: T) -> Optional[T]:
        result = list(
            filter(
                lambda value: getattr(value, self._primary_key) == getattr(model, self._primary_key),
                self._cache
            )
        )

        return result[0] if result else None
