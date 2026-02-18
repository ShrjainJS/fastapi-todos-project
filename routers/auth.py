from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from sqlalchemy.orm import Session # This it to get the type for Dependency injection
from sqlalchemy import select

from utils.auth_utils import hash_password, verify_password
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError

from models.db_models import Users
from models.user_req_models import CreateUserRequest
from models.response_models import UserReturn, Token
from database.database import SessionLocal

router = APIRouter(
    prefix='/auth',
    tags = ['Authentication']
)

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

# Authenticate the User with Username and Password - Match against Hash
def authenticate_user(username: str, password: str, db: Session):
    sql_stmt = select(Users).where(Users.username == username)

    user_model_result = db.scalars(statement=sql_stmt).first()

    if user_model_result is None:
        return False
    
    if not verify_password(password_passed=password, hashed_password=user_model_result.hashed_password):
        return False
    
    return user_model_result

# Below is implementation for Authorization and Bearer Token

SECRET_KEY = '2fcd69a94397faf86a7f5ea855a18890f7adc497f1313162ef86e94aac33f724'

ALGORITHM = 'HS256'

# Create dependency for Auth
# Keep the url same as what you keep for using login to create access token url "current: /login API path"(see below)
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

# Create access_token
def create_access_token(username: str, user_id: int, role: str | None, expires_delta: timedelta):
    
    claims_encode = {
        'sub': username,    # standard claim
        'id': user_id,      # custom claim
        'role': role        # custom claim
    }

    expires = datetime.now(timezone.utc) + expires_delta

    claims_encode.update({
        'exp': expires      # standard claim
    })

    return jwt.encode(claims=claims_encode, algorithm=ALGORITHM, key=SECRET_KEY)

# Define a function to get current user
async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(
            token=token,
            key=SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        username: str | None = payload.get('sub')
        user_id: int | None = payload.get('id')
        user_role: str | None = payload.get('role')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized access')

        return {'username': username, 'id': user_id, 'role': user_role}
    
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized access')

db_dependency = Annotated[Session, Depends(get_db)]

# APIs to Create
# 1. Create User
# 2. Login User

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserReturn)
async def create_user(db: db_dependency, create_request: CreateUserRequest):
    new_user_model = Users(
        email=create_request.email,
        username=create_request.username,
        first_name=create_request.first_name,
        last_name=create_request.last_name,
        hashed_password=hash_password(create_request.password),
        role=create_request.role,
        is_active=True
    )

    db.add(new_user_model)

    db.commit()

    db.refresh(new_user_model)

    return new_user_model

@router.post("/token", status_code=status.HTTP_200_OK, response_model=Token)
async def login_user_for_token(db: db_dependency, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(username=form_data.username, password=form_data.password, db=db)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Failed to Authenticate')
    
    user_jwt_token = create_access_token(
        username=user.username,
        user_id=user.id,
        role=user.role,
        expires_delta=timedelta(minutes=20)
    )

    return {'access_token': user_jwt_token, 'token_type': 'bearer'}

