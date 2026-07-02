from src.selections.domain.models import Selection
from src.selections.domain.repositories import SelectionRepository


class GetSelectionById:

    def __init__(self, repository: SelectionRepository):
        self.repository = repository

    def execute(self, id: int) -> Selection | None:
        return self.repository.get_by_id(id)