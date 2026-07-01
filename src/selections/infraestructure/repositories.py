from src.selections.domain.models import Selection
from src.selections.domain.repositories import SelectionRepository


class InMemorySelectionRepository(SelectionRepository):

    def __init__(self):
        self._selections: list[Selection] = []

    def create(self, selection: Selection) -> None:
        self._selections.append(selection)

    def get_all(self) -> list[Selection]:
        return list(self._selections)

    def get_by_id(self, id: int) -> Selection | None:
        for selection in self._selections:
            if selection.id() == id:
                return selection

        return None

    def update(self, selection: Selection) -> None:
        for index, item in enumerate(self._selections):
            if item.id() == selection.id():
                self._selections[index] = selection
                return

    def delete(self, id: int) -> None:
        self._selections = [
            selection
            for selection in self._selections
            if selection.id() != id
        ]