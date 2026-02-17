from fastapi import APIRouter, Depends, HTTPException, status, Path
from typing import Annotated, List
from sqlalchemy.orm import Session # This it to get the type for Dependency injection
from sqlalchemy import select

from passlib.context import CryptContext

from models.db_models import Users
from models.user_req_models import UpdateUserRequest, UpdatePasswordRequest
from models.response_models import UserReturn
from database.database import SessionLocal

router = APIRouter(
    prefix='/user',
    tags = ['User Data']
)

bycrpt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

# APIs to Create
# 1. Get All Users
# 2. Get User Details by id
# 3. Get User Details by username 

# 4. Update User Details by id
# 5. Update User Details by username
# 6. Update Password by id
# 7. Update Password by username

# 8. Delete User by id
# 9. Delete User by username

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[UserReturn])
async def get_all_users(db: db_dependency):
    sql_stmt = select(Users)

    return db.scalars(sql_stmt).all()

@router.get("/id/{user_id}", status_code=status.HTTP_200_OK, response_model=UserReturn)
async def get_user_by_id(db: db_dependency, user_id: int = Path(gt=0)):
    sql_stmt = select(Users).where(Users.id == user_id)

    user_model_result = db.scalars(statement=sql_stmt).first()

    if user_model_result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User Not Found.')
    
    return user_model_result

@router.get("/username/{username}", status_code=status.HTTP_200_OK, response_model=UserReturn)
async def get_user_by_username(db: db_dependency, username: str = Path(min_length=3)):
    sql_stmt = select(Users).where(Users.username == username)

    user_model_result = db.scalars(statement=sql_stmt).first()

    if user_model_result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User Not Found.')
    
    return user_model_result

@router.put("/id/{user_id}", status_code=status.HTTP_200_OK, response_model=UserReturn)
async def update_user_by_id(db: db_dependency, update_request: UpdateUserRequest, user_id: int = Path(gt=0)):
    print('I am here in ID.')
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


    db.commit()

    db.refresh(user_model_result)

    return user_model_result

@router.put("/username/{username}", status_code=status.HTTP_200_OK, response_model=UserReturn)
async def update_user_by_username(db: db_dependency, update_request: UpdateUserRequest, username: str = Path(min_length=3)):
    print('I am here in Username')
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


    db.commit()

    db.refresh(user_model_result)

    return user_model_result

@router.put("/password/id/{user_id}", status_code=status.HTTP_200_OK, response_model=UserReturn)
async def update_password_by_id(db: db_dependency, update_request: UpdatePasswordRequest, user_id: int = Path(gt=0)):
    sql_stmt = select(Users).where(Users.id == user_id)

    user_model_result = db.scalars(statement=sql_stmt).first()

    if user_model_result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User Not Found.')
    
    user_model_result.hashed_password = bycrpt_context.hash(update_request.new_password)

    db.commit()

    db.refresh(user_model_result)

    return user_model_result

@router.put("/password/username/{username}", status_code=status.HTTP_200_OK, response_model=UserReturn)
async def update_password_by_username(db: db_dependency, update_request: UpdatePasswordRequest, username: str = Path(min_length=3)):
    sql_stmt = select(Users).where(Users.username == username)

    user_model_result = db.scalars(statement=sql_stmt).first()

    if user_model_result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User Not Found.')
    
    user_model_result.hashed_password = bycrpt_context.hash(update_request.new_password)

    db.commit()

    db.refresh(user_model_result)

    return user_model_result

@router.delete("/id/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_by_id(db: db_dependency, user_id: int = Path(gt=0)):
    sql_stmt = select(Users).where(Users.id == user_id)

    user_model_result = db.scalars(statement=sql_stmt).first()

    if user_model_result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User Not Found.')
    
    db.delete(user_model_result)

    db.commit()

@router.delete("/username/{username}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_by_username(db: db_dependency, username: str = Path(min_length=3)):
    sql_stmt = select(Users).where(Users.id == username)

    user_model_result = db.scalars(statement=sql_stmt).first()

    if user_model_result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User Not Found.')
    
    db.delete(user_model_result)

    db.commit()
