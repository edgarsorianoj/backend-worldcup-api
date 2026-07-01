from src.selections.domain.models import Selection
from src.selections.domain.repositories import SelectionRepository


class UpdateSelection:

    def __init__(self, repository: SelectionRepository):
        self.repository = repository

    def execute(
        self,
        id: int,
        country: str,
        confederation: str,
        captain: str,
        coach: str,
        world_cups: int,
        flag: str,
    ) -> Selection | None:

        selection = self.repository.get_by_id(id)

        if selection is None:
            return None

        selection.update(
            country=country,
            confederation=confederation,
            captain=captain,
            coach=coach,
            world_cups=world_cups,
            flag=flag,
        )

        self.repository.update(selection)

        return selection