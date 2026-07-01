from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from src.selections.application.create_selection import (
    CreateSelection,
    CreateSelectionCommand,
)
from src.selections.application.get_all_selections import GetAllSelections
from src.selections.application.get_selection_by_id import GetSelectionById
from src.selections.application.update_selection import UpdateSelection
from src.selections.infraestructure.repositories import InMemorySelectionRepository


router = APIRouter(prefix="/selections")


repository = InMemorySelectionRepository()


class SelectionPayload(BaseModel):
    country: str
    confederation: str
    captain: str
    coach: str
    world_cups: int
    flag: str


class SelectionResponse(BaseModel):
    id: int | None
    country: str
    confederation: str
    captain: str
    coach: str
    world_cups: int
    flag: str


def selection_to_response(selection):
    return SelectionResponse(
        id=selection.id(),
        country=selection.country(),
        confederation=selection.confederation(),
        captain=selection.captain(),
        coach=selection.coach(),
        world_cups=selection.world_cups(),
        flag=selection.flag(),
    )


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_selection(payload: SelectionPayload):

    selection = CreateSelection(repository).execute(
        CreateSelectionCommand(
            country=payload.country,
            confederation=payload.confederation,
            captain=payload.captain,
            coach=payload.coach,
            world_cups=payload.world_cups,
            flag=payload.flag,
        )
    )

    return selection_to_response(selection)


@router.get("/")
async def get_all_selections():

    selections = GetAllSelections(repository).execute()

    return [
        selection_to_response(selection)
        for selection in selections
    ]


@router.get("/{id}")
async def get_selection(id: int):

    selection = GetSelectionById(repository).execute(id)

    if selection is None:
        raise HTTPException(
            status_code=404,
            detail="Selection not found"
        )

    return selection_to_response(selection)


@router.put("/{id}")
async def update_selection(id: int, payload: SelectionPayload):

    selection = UpdateSelection(repository).execute(
        id=id,
        country=payload.country,
        confederation=payload.confederation,
        captain=payload.captain,
        coach=payload.coach,
        world_cups=payload.world_cups,
        flag=payload.flag,
    )

    if selection is None:
        raise HTTPException(
            status_code=404,
            detail="Selection not found"
        )

    return selection_to_response(selection)