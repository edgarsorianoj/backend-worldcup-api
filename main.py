from fastapi import FastAPI

from src.selections.infraestructure.api import router as selections_router


app = FastAPI()


app.include_router(selections_router)


@app.get("/")
async def root():
    return {"msg": "World Cup 2026 API"}