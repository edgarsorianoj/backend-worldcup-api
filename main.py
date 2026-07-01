from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"msg": "World Cup 2026 API"}