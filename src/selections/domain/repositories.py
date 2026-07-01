from abc import ABC, abstractmethod
from src.selections.domain.models import Selection


class SelectionRepository(ABC):

    @abstractmethod
    def create(self, selection: Selection) -> None:
        pass

    @abstractmethod
    def get_all(self) -> list[Selection]:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Selection | None:
        pass

    @abstractmethod
    def update(self, selection: Selection) -> None:
        pass

    @abstractmethod
    def delete(self, id: int) -> None:
        pass