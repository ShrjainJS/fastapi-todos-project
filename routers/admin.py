from fastapi import APIRouter, Depends, HTTPException, status, Path
from typing import Annotated, List

from sqlalchemy.orm import Session
from sqlalchemy import select

from utils.auth_utils import hash_password

from database.database import SessionLocal
from models.db_models import Users, Todos
from models.user_req_models import UpdateUserRequest, UpdatePasswordRequest
from models.todo_models import TodoRequest
from models.response_models import UserReturn, TodoReturn
from .auth import get_current_user

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

router = APIRouter(
    prefix='/admin',
    tags=['Admin Controls']
)

db_dependency = Annotated[Session, Depends(get_db)]

user_dependency = Annotated[dict, Depends(get_current_user)]

@router.get("/admin-user", status_code=status.HTTP_200_OK, response_model=UserReturn)
async def get_user_detail(user: user_dependency, db: db_dependency):
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorize access.')
    
    if user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorize access.')
    
    sql_stmt = select(Users).where(Users.id == user.get('id'))

    return db.scalars(sql_stmt).first()

@router.get("/all-users", status_code=status.HTTP_200_OK, response_model=List[UserReturn])
async def get_all_user_details(user: user_dependency, db: db_dependency):
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorize access.')
    
    if user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorize access.')
    
    sql_stmt = select(Users)

    return db.scalars(sql_stmt).all()

@router.get("/user-by-id/{user_id}", status_code=status.HTTP_200_OK, response_model=UserReturn)
async def get_user_by_id(user: user_dependency, db: db_dependency, user_id: int = Path(gt=0)):

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorize access.')
    
    if user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorize access.')
    
    sql_stmt = select(Users).where(Users.id == user_id)

    user_model_result = db.scalars(statement=sql_stmt).first()

    if user_model_result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User Not Found.')
    
    return user_model_result

@router.get("/user-by-username/{username}", status_code=status.HTTP_200_OK, response_model=UserReturn)
async def get_user_by_username(user: user_dependency, db: db_dependency, username: str = Path(min_length=3)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorize access.')
    
    if user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorize access.')
    
    sql_stmt = select(Users).where(Users.username == username)

    user_model_result = db.scalars(statement=sql_stmt).first()

    if user_model_result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User Not Found.')
    
    return user_model_result

@router.put("/user-by-id/{user_id}", status_code=status.HTTP_200_OK, response_model=UserReturn)
async def update_user_by_id(user: user_dependency, db: db_dependency, update_request: UpdateUserRequest, user_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorize access.')
    
    if user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorize access.')
    
    sql_stmt = select(Users).where(Users.id == user_id)

    user_model_result = db.scalars(statement=sql_stmt).first()

    if user_model_result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User Not Found.')
    
    user_model_result.username = update_request.username
    user_model_result.email = update_request.email
    user_model_result.first_name = update_request.first_name
    user_model_result.last_name = update_request.last_name
    user_model_result.is_active = update_request.is_active
    user_model_result.role = update_request.role
    user_model_result.phone_number = update_request.phone_number


    db.commit()

    db.refresh(user_model_result)

    return user_model_result

@router.put("/user-by-username/{username}", status_code=status.HTTP_200_OK, response_model=UserReturn)
async def update_user_by_username(user: user_dependency, db: db_dependency, update_request: UpdateUserRequest, username: str = Path(min_length=3)):
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorize access.')
    
    if user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorize access.')
    
    sql_stmt = select(Users).where(Users.username == username)

    user_model_result = db.scalars(statement=sql_stmt).first()

    if user_model_result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User Not Found.')
    
    user_model_result.username = update_request.username
    user_model_result.email = update_request.email
    user_model_result.first_name = update_request.first_name
    user_model_result.last_name = update_request.last_name
    user_model_result.is_active = update_request.is_active
    user_model_result.role = update_request.role
    user_model_result.phone_number = update_request.phone_number


    db.commit()

    db.refresh(user_model_result)

    return user_model_result

@router.put("/user-by-id/password/{user_id}", status_code=status.HTTP_200_OK, response_model=UserReturn)
async def update_password_by_id(user: user_dependency, db: db_dependency, update_request: UpdatePasswordRequest, user_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorize access.')
    
    if user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorize access.')
    
    sql_stmt = select(Users).where(Users.id == user_id)

    user_model_result = db.scalars(statement=sql_stmt).first()

    if user_model_result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User Not Found.')
    
    user_model_result.hashed_password = hash_password(update_request.new_password)

    db.commit()

    db.refresh(user_model_result)

    return user_model_result

@router.put("/user-by-username/password/{username}", status_code=status.HTTP_200_OK, response_model=UserReturn)
async def update_password_by_username(user: user_dependency, db: db_dependency, update_request: UpdatePasswordRequest, username: str = Path(min_length=3)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorize access.')
    
    if user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorize access.')
    
    sql_stmt = select(Users).where(Users.username == username)

    user_model_result = db.scalars(statement=sql_stmt).first()

    if user_model_result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User Not Found.')
    
    user_model_result.hashed_password = hash_password(update_request.new_password)

    db.commit()

    db.refresh(user_model_result)

    return user_model_result

@router.delete("/user-by-id/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_by_id(user: user_dependency, db: db_dependency, user_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorize access.')
    
    if user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorize access.')
    
    sql_stmt = select(Users).where(Users.id == user_id)

    user_model_result = db.scalars(statement=sql_stmt).first()

    if user_model_result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User Not Found.')
    
    db.delete(user_model_result)

    db.commit()

@router.delete("/user-by-username/{username}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_by_username(user: user_dependency, db: db_dependency, username: str = Path(min_length=3)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorize access.')
    
    if user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorize access.')
    
    sql_stmt = select(Users).where(Users.id == username)

    user_model_result = db.scalars(statement=sql_stmt).first()

    if user_model_result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User Not Found.')
    
    db.delete(user_model_result)

    db.commit()

@router.get('/all-todos', status_code=status.HTTP_200_OK, response_model=List[TodoReturn])
async def get_all_tasks(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorize access.')
    
    if user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorize access.')
    
    sql_stmt = select(Todos)

    return db.scalars(statement=sql_stmt).all()

@router.get('/todos/{todo_id}', status_code=status.HTTP_200_OK, response_model=TodoReturn)
async def get_todo_by_id(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorize access.')
    
    if user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorize access.')
    
    sql_stmt = select(Todos).where(Todos.id == todo_id)

    task_model_result = db.scalars(statement=sql_stmt).first()

    if task_model_result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Could not find task requested.')
    
    return task_model_result

@router.put('/todos/{todo_id}', status_code=status.HTTP_200_OK, response_model=TodoReturn)
async def update_todo_by_id(user: user_dependency, db: db_dependency, todo_request: TodoRequest, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorize access.')
    
    if user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorize access.')

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

@router.post('/todos', status_code=status.HTTP_201_CREATED, response_model=TodoReturn)
async def create_todo(user: user_dependency, db: db_dependency, todo_request: TodoRequest):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorize access.')
    
    if user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorize access.')
    
    new_task_to_add_to_db = Todos(**todo_request.model_dump(), owner_id=user.get('id'))

    db.add(new_task_to_add_to_db)
    db.commit()
    db.refresh(new_task_to_add_to_db)

    return new_task_to_add_to_db

@router.delete('/todos/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_note_by_id(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorize access.')
    
    if user.get('role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorize access.')
    
    sql_stmt = select(Todos).where(Todos.owner_id == user.get('id')).where(Todos.id == todo_id)

    task_model_result = db.scalars(statement=sql_stmt).first()

    if task_model_result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Task not found.')
    
    db.delete(task_model_result)

    db.commit()

