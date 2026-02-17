from fastapi import APIRouter, Depends, Path, HTTPException, status

from typing import Annotated, Generator, List

from sqlalchemy import select
from sqlalchemy.orm import Session

from models.response_models import TodoReturn
from models.todo_models import TodoRequest
from models.db_models import Todos
from database.database import SessionLocal

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

# APIs to build:
# 1. Read All tasks
# 2. Read 1 task by id
# 3. Create 1 task
# 4. Update 1 task
# 5. Delete 1 task


# API Path for reading all the todos in the document
@router.get("/", status_code=status.HTTP_200_OK, response_model=List[TodoReturn])
async def get_all_todos(db: db_dependency):
    sql_stmt = select(Todos)

    return db.scalars(statement=sql_stmt).all()

# API Path to read task by id
@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK, response_model=TodoReturn)
async def get_todo_by_id(db: db_dependency, todo_id: int = Path(gt=0)):
    sql_stmt = select(Todos).where(Todos.id == todo_id)

    task_model_result = db.scalars(statement=sql_stmt).first()

    if task_model_result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Could not find task requested.')
    
    return task_model_result

# API Path to add task
@router.post("/todo", status_code=status.HTTP_201_CREATED, response_model=TodoReturn)
async def create_todo(db: db_dependency, todo_request: TodoRequest):
    new_task_to_add_to_db = Todos(**todo_request.model_dump(), owner_id=1)

    db.add(new_task_to_add_to_db)
    db.commit()
    db.refresh(new_task_to_add_to_db)

    return new_task_to_add_to_db

# API Path to update a task
@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)#, response_model=TodoReturn)
async def update_todo_by_id(db: db_dependency, todo_request: TodoRequest, todo_id: int = Path(gt=0)):
    sql_stmt = select(Todos).where(Todos.id == todo_id)

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
@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo_by_id(db: db_dependency, todo_id: int = Path(gt=0)):
    sql_stmt = select(Todos).where(Todos.id == todo_id)

    task_model_result = db.scalars(statement=sql_stmt).first()

    if task_model_result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Task not found.')
    
    db.delete(task_model_result)

    db.commit()
