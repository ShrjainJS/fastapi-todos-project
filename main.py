from fastapi import FastAPI, status, Request

from models import db_models
from database.database import engine
from routers import todos, auth, users, admin
# from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from pathlib import Path

app = FastAPI()

db_models.Base.metadata.create_all(bind=engine)

BASE_DIR_TEMPLATE = Path(__file__).resolve().parent
# templates = Jinja2Templates(directory="templates")
# templates = Jinja2Templates(directory=str(BASE_DIR_TEMPLATE/"templates"))

# 1st Argument: is a URL prefix for the browser - Purpose is API design and organisation
# 2nd Argument: StaticFiles is a static file serving engine which serves static files (with directory specifying where static files are) when browser hits url as identified in 1st argument.
# 3rd Argument: Used by Python + Jinja to use variable name for "url_for()" method which is the standard way to add links to the files from the project using Jinja templating engine 
app.mount("/static", StaticFiles(directory=str(BASE_DIR_TEMPLATE/"static")), name="static")

@app.get("/")
def test(request: Request):
    # return templates.TemplateResponse("home.html", {"request": request})
    return RedirectResponse(url="/todos/todo-page", status_code=status.HTTP_302_FOUND)

@app.get("/healthy", status_code=status.HTTP_200_OK, include_in_schema=False)
def health_check():
    return {'message': 'OK'}


app.include_router(router=auth.router)
app.include_router(router=todos.router)
app.include_router(router=users.router)
app.include_router(router=admin.router)
