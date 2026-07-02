from sqlmodel import SQLModel, Field, Session, create_engine, select

from src.selections.domain.models import Selection
from src.selections.domain.repositories import SelectionRepository
from src.selections.domain.value_objects import SelectionFlag

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

class SelectionModel(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    country: str
    confederation: str
    captain: str
    coach: str
    world_cups: int
    flag: str


engine = create_engine("sqlite:///selections.db")

SQLModel.metadata.create_all(engine)


class SQLModelSelectionRepository(SelectionRepository):

    def create(self, selection: Selection) -> None:
        selection_model = SelectionModel(
            country=selection.country(),
            confederation=selection.confederation(),
            captain=selection.captain(),
            coach=selection.coach(),
            world_cups=selection.world_cups(),
            flag=selection.flag().value,
        )

        with Session(engine) as session:
            session.add(selection_model)
            session.commit()
            session.refresh(selection_model)

            selection.set_id(selection_model.id)

    def get_all(self) -> list[Selection]:
        with Session(engine) as session:
            selection_models = session.exec(
                select(SelectionModel)
            ).all()

        return [
            Selection(
                id=item.id,
                country=item.country,
                confederation=item.confederation,
                captain=item.captain,
                coach=item.coach,
                world_cups=item.world_cups,
                flag=SelectionFlag(value=item.flag),
            )
            for item in selection_models
        ]

    def get_by_id(self, id: int) -> Selection | None:
        with Session(engine) as session:
            item = session.get(SelectionModel, id)

        if item is None:
            return None

        return Selection(
            id=item.id,
            country=item.country,
            confederation=item.confederation,
            captain=item.captain,
            coach=item.coach,
            world_cups=item.world_cups,
            flag=SelectionFlag(value=item.flag),
        )

    def update(self, selection: Selection) -> None:
        with Session(engine) as session:
            item = session.get(SelectionModel, selection.id())

            if item is None:
                return

            item.country = selection.country()
            item.confederation = selection.confederation()
            item.captain = selection.captain()
            item.coach = selection.coach()
            item.world_cups = selection.world_cups()
            item.flag = selection.flag().value

            session.add(item)
            session.commit()

    def delete(self, id: int) -> None:
        with Session(engine) as session:
            item = session.get(SelectionModel, id)

            if item is None:
                return

            session.delete(item)
            session.commit()