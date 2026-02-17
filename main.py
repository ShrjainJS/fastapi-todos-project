from fastapi import FastAPI

from models import db_models
from database.database import engine
from routers import todos

app = FastAPI()

db_models.Base.metadata.create_all(bind=engine)

app.include_router(router=todos.router)

