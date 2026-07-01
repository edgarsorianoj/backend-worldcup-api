from src.selections.domain.models import Selection
from src.selections.domain.repositories import SelectionRepository


class InMemorySelectionRepository(SelectionRepository):

    def __init__(self):
        self._selections: list[Selection] = []
        self._next_id = 1

    def create(self, selection: Selection) -> None:
        selection.set_id(self._next_id)
        self._next_id += 1

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
        selection = self.get_by_id(id)

        if selection is not None:
            self._selections.remove(selection)