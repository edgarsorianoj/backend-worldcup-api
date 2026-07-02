from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from src.selections.domain.exception import SelectionFlagNotValid
from src.selections.infraestructure.api import router as selections_router


app = FastAPI()



# CORS CONFIGURATION

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # en producción se restringe, aquí está bien para proyecto académico
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# ROUTES

app.include_router(selections_router)



# EXCEPTION HANDLER

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


# =========================
# ROOT
# =========================
@app.get("/")
async def root():
    return {"msg": "World Cup 2026 API"}