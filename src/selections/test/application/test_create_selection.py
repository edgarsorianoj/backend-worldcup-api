from src.selections.application.create_selection import (
    CreateSelection,
    CreateSelectionCommand,
)
from src.selections.domain.models import Selection
from src.selections.domain.repositories import SelectionRepository


class FakeSelectionRepository(SelectionRepository):

    def __init__(self):
        self._selections = []

    def create(self, selection: Selection) -> None:
        self._selections.append(selection)

    def get_all(self) -> list[Selection]:
        return self._selections

    def get_by_id(self, id: int) -> Selection | None:
        return None

    def update(self, selection: Selection) -> None:
        pass

    def delete(self, id: int) -> None:
        pass


class TestCreateSelection:

    def test_create_selection(self) -> None:
        repository = FakeSelectionRepository()

        CreateSelection(repository).execute(
            CreateSelectionCommand(
                country="Spain",
                confederation="UEFA",
                captain="Rodri",
                coach="Luis de la Fuente",
                world_cups=1,
                flag="https://example.com/spain.png",
            )
        )

        selections = repository.get_all()

        assert len(selections) == 1
        assert selections[0].country() == "Spain"