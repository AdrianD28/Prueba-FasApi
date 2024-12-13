from fastapi import FastAPI
from app.routers import events, stories, tests

app = FastAPI()

app.include_router(events.router, prefix="/api/v1/events", tags=["events"])
app.include_router(stories.router, prefix="/api/v1/stories", tags=["stories"])
app.include_router(tests.router, prefix="/api/v1/tests", tags=["tests"])

@app.get("/")
async def root():
    return {"message": "Bienvenido a la API de Bugster"}