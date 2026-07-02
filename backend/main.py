from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.selections.domain.exception import SelectionFlagNotValid
from src.selections.infraestructure.api import router as selections_router


app = FastAPI()


app.include_router(selections_router)


@app.exception_handler(SelectionFlagNotValid)
async def selection_flag_exception_handler(
    request: Request,
    exc: SelectionFlagNotValid,
):
    return JSONResponse(
        status_code=400,
        content={
            "detail": "Invalid flag URL"
        },
    )


@app.get("/")
async def root():
    return {"msg": "World Cup 2026 API"}