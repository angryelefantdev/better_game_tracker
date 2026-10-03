from fastapi import FastAPI

from database import Base, engine
from models.games import Games
from models.users import Users

from routers import auth, users, games


Base.metadata.create_all(engine)


app = FastAPI()


app.include_router(
    auth.router,
    prefix="/auth",
    tags=["Authentication"]
)

app.include_router(
    users.router,
    prefix="/users",
    tags=["Users"]
)

app.include_router(
    games.router,
    prefix="/games",
    tags=["Games"]
)