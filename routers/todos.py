from fastapi import APIRouter, Depends, Path, HTTPException, status, Request

from typing import Annotated, Generator, List

from sqlalchemy import select
from sqlalchemy.orm import Session

from models.response_models import TodoReturn
from models.todo_models import TodoRequest
from models.db_models import Todos
from database.database import SessionLocal
from .auth import get_current_user

from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path as pagePath

BASE_DIR_TEMPLATE = pagePath(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR_TEMPLATE/"templates"))

router = APIRouter(
    prefix = "/todos",
    tags = ['todos']
)

# This function is defined to handle DB Connection for each SQL Request and securly close it before the next session.
def get_db() -> Generator[Session, None]:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

# Next with above being used across each and every API call, needs to be added as dependency for each of the path callables.
db_dependency = Annotated[Session, Depends(get_db)]

user_dependency = Annotated[dict, Depends(get_current_user)]

# APIs to build:
# 1. Read All tasks
# 2. Read 1 task by id
# 3. Create 1 task
# 4. Update 1 task
# 5. Delete 1 task

def redirect_to_login():
    redirect_response = RedirectResponse(url="/auth/login-page", status_code=status.HTTP_302_FOUND)
    redirect_response.delete_cookie(key='access_token')
    return redirect_response

### Pages
@router.get("/todo-page")
async def render_todo_page(request: Request, db: db_dependency):
    try:
        user = await get_current_user(request.cookies.get('access_token')) # pyright: ignore[reportArgumentType]
        if user is None:
            return redirect_to_login()
        
        stmt = select(Todos).where(Todos.owner_id == user.get('id'))

        all_todos = db.scalars(statement=stmt).all()

        return templates.TemplateResponse("todo.html", {"request": request, "todos": all_todos, "user": user})

    except:
        return redirect_to_login()
 
@router.get("/add-todo-page")
async def render_add_todo_page(request: Request):
    try:
        user = await get_current_user(request.cookies.get('access_token')) # pyright: ignore[reportArgumentType]
        if user is None:
            return redirect_to_login()
        
        return templates.TemplateResponse("add-todo.html", {"request": request, "user": user})
    
    except:
        return redirect_to_login()

@router.get("/edit-todo-page/{todo_id}")
async def render_edit_todo_page(request: Request, todo_id: int, db: db_dependency):
    try:
        user = await get_current_user(request.cookies.get('access_token')) # pyright: ignore[reportArgumentType]

        if user is None:
            return redirect_to_login()
        
        stmt = select(Todos).where(Todos.owner_id == user.get('id')).where(Todos.id == todo_id)

        get_todo = db.scalars(statement=stmt).first()

        return templates.TemplateResponse("edit-todo.html", {"request": request, "user": user, "todo": get_todo})
    except:

        return redirect_to_login()

### Endpoints -> 
# API Path for reading all the todos in the document
@router.get("/", status_code=status.HTTP_200_OK, response_model=List[TodoReturn])
async def get_all_todos(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not able to verify user credentials.')
    
    sql_stmt = select(Todos).where(Todos.owner_id == user.get('id'))

    all_todos = db.scalars(statement=sql_stmt).all()

    return all_todos

# API Path to read task by id
@router.get("/{todo_id}", status_code=status.HTTP_200_OK, response_model=TodoReturn)
async def get_todo_by_id(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not able to verify user credentials.')
    
    sql_stmt = select(Todos).where(Todos.owner_id == user.get('id')).where(Todos.id == todo_id)

    task_model_result = db.scalars(statement=sql_stmt).first()

    if task_model_result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Could not find task requested.')
    
    return task_model_result

# API Path to add task
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=TodoReturn)
async def create_todo(user: user_dependency, db: db_dependency, todo_request: TodoRequest):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not able to verify user credentials.')
    
    new_task_to_add_to_db = Todos(**todo_request.model_dump(), owner_id=user.get('id'))

    db.add(new_task_to_add_to_db)
    db.commit()
    db.refresh(new_task_to_add_to_db)

    return new_task_to_add_to_db

# API Path to update a task
@router.put("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)#, response_model=TodoReturn)
async def update_todo_by_id(user: user_dependency, db: db_dependency, todo_request: TodoRequest, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not able to verify user credentials.')
    
    sql_stmt = select(Todos).where(Todos.owner_id == user.get('id')).where(Todos.id == todo_id)

    task_model_result = db.scalars(statement=sql_stmt).first()

    if task_model_result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='requested Task does not exist.')

    if task_model_result is not None:
        task_model_result.title = todo_request.title
        task_model_result.description = todo_request.description
        task_model_result.priority = todo_request.priority
        task_model_result.complete = todo_request.complete

        db.commit()
 
# API Path to delete a task
@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo_by_id(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not able to verify user credentials.')
    
    sql_stmt = select(Todos).where(Todos.owner_id == user.get('id')).where(Todos.id == todo_id)

    task_model_result = db.scalars(statement=sql_stmt).first()

    if task_model_result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Task not found.')
    
    db.delete(task_model_result)

    db.commit()
