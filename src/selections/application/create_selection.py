from dataclasses import dataclass

from src.selections.domain.models import Selection
from src.selections.domain.repositories import SelectionRepository


@dataclass
class CreateSelectionCommand:
    country: str
    confederation: str
    captain: str
    coach: str
    world_cups: int
    flag: str


class CreateSelection:

    def __init__(self, repository: SelectionRepository):
        self.repository = repository

    def execute(self, command: CreateSelectionCommand) -> Selection:

        selection = Selection(
            country=command.country,
            confederation=command.confederation,
            captain=command.captain,
            coach=command.coach,
            world_cups=command.world_cups,
            flag=command.flag,
        )

        self.repository.create(selection)

        return selection