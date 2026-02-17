from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, status, Path
from typing import Annotated, List
from sqlalchemy.orm import Session # This it to get the type for Dependency injection
from sqlalchemy import select

from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm

from models.db_models import Users
from models.user_req_models import CreateUserRequest, UpdateUserRequest
from models.response_models import UserReturn
from database.database import SessionLocal

router = APIRouter(
    prefix='/auth',
    tags = ['Authentication']
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
# 1. Create User

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserReturn)
async def create_user(db: db_dependency, create_request: CreateUserRequest):
    new_user_model = Users(
        email=create_request.email,
        username=create_request.username,
        first_name=create_request.first_name,
        last_name=create_request.last_name,
        hashed_password=bycrpt_context.hash(create_request.password),
        role=create_request.role,
        is_active=True
    )

    db.add(new_user_model)

    db.commit()

    db.refresh(new_user_model)

    return new_user_model
