from fastapi import FastAPI
import logging_config

from models.base import Base
from database import engine

from routers.public_router import router as public_router
from routers.user_router import router as user_router
from routers.task_router import router as task_router


app = FastAPI(
    title="Task Manager API",
    version="1.0.0",
)


@app.on_event("startup")
async def startup():

    async with engine.begin() as conn:

        await conn.run_sync(
            Base.metadata.create_all
        )

print("\n========== REGISTERED ROUTES ==========")
for route in app.routes:
    print(f"{route.path} --> {route.methods}")

print("=======================================\n")
app.include_router(public_router)

app.include_router(user_router)

app.include_router(task_router)

print(">>> USER ROUTER LOADED <<<")
@app.get("/")
async def root():

    return {
        "message": "Task Manager API is running."
    }