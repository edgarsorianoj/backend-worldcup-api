from src.selections.domain.models import Selection
from src.selections.domain.repositories import SelectionRepository


class GetAllSelections:

    def __init__(self, repository: SelectionRepository):
        self.repository = repository

    def execute(self) -> list[Selection]:
        return self.repository.get_all()