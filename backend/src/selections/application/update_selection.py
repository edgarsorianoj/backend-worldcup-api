from dataclasses import dataclass

from src.selections.domain.models import Selection
from src.selections.domain.repositories import SelectionRepository
from src.selections.domain.value_objects import SelectionFlag


@dataclass
class UpdateSelectionCommand:
    id: int
    country: str
    confederation: str
    captain: str
    coach: str
    world_cups: int
    flag: str


class UpdateSelection:

    def __init__(self, repository: SelectionRepository):
        self.repository = repository

    def execute(
        self,
        command: UpdateSelectionCommand,
    ) -> Selection | None:

        selection = self.repository.get_by_id(command.id)

        if selection is None:
            return None

        selection.update(
            country=command.country,
            confederation=command.confederation,
            captain=command.captain,
            coach=command.coach,
            world_cups=command.world_cups,
            flag=SelectionFlag(value=command.flag),
        )

        self.repository.update(selection)

        return selection