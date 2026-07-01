from src.selections.domain.repositories import SelectionRepository


class DeleteSelection:

    def __init__(self, repository: SelectionRepository):
        self.repository = repository

    def execute(self, id: int) -> None:
        self.repository.delete(id)