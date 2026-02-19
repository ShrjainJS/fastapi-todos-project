from fastapi import FastAPI, status

from models import db_models
from database.database import engine
from routers import todos, auth, users, admin

app = FastAPI()

db_models.Base.metadata.create_all(bind=engine)

@app.get("/healthy", status_code=status.HTTP_200_OK, include_in_schema=False)
def health_check():
    return {'message': 'OK'}


app.include_router(router=auth.router)
app.include_router(router=todos.router)
app.include_router(router=users.router)
app.include_router(router=admin.router)
