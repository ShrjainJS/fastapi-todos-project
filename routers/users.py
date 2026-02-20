from fastapi import APIRouter, Depends, HTTPException, status, Path
from typing import Annotated, List
from sqlalchemy.orm import Session # This it to get the type for Dependency injection
from sqlalchemy import select

from utils.auth_utils import hash_password

from models.db_models import Users
from models.user_req_models import UpdateUserRequest, UpdatePasswordRequest
from models.response_models import UserReturn
from database.database import SessionLocal
from .auth import get_current_user

router = APIRouter(
    prefix='/user',
    tags = ['User Details Data']
)

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

user_dependecy = Annotated[dict, Depends(get_current_user)]

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

@router.get("/get-user", status_code=status.HTTP_200_OK, response_model=UserReturn)
async def get_user_detail(user: user_dependecy, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Failed to authenticate user.')
    
    sql_stmt = select(Users).where(Users.id == user.get('id'))

    return db.scalars(sql_stmt).first()

@router.put("/update-details", status_code=status.HTTP_200_OK, response_model=UserReturn)
async def update_user_details(user: user_dependecy, db: db_dependency, update_request: UpdateUserRequest):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Failed to authenticate user.')

    sql_stmt = select(Users).where(Users.id == user.get('id'))

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

@router.put("/update-password", status_code=status.HTTP_204_NO_CONTENT)
async def update_password(user: user_dependecy, db: db_dependency, update_request: UpdatePasswordRequest):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Failed to authenticate user.')
    
    sql_stmt = select(Users).where(Users.id == user.get('id'))

    user_model_result = db.scalars(statement=sql_stmt).first()

    if user_model_result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User Not Found.')
    
    user_model_result.hashed_password = hash_password(update_request.new_password)

    db.commit()

@router.delete("/delete-user", status_code=status.HTTP_200_OK, response_model=UserReturn)
async def delete_user(user: user_dependecy, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Failed to Authenticate User')
    
    sql_stmt = select(Users).where(Users.id == user.get('id'))

    user_model_result = db.scalars(statement=sql_stmt).first()

    if user_model_result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User Not Found.')
    
    db.delete(user_model_result)

    db.commit()

    return user_model_result
