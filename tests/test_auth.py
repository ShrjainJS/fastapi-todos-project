from .utils import *
from sqlalchemy import select
from routers.auth import get_db, authenticate_user, create_access_token, ALGORITHM, SECRET_KEY, get_current_user
from jose import jwt
from datetime import timedelta
import pytest

app.dependency_overrides[get_db] = override_get_db

# test creating a user
def test_create_user(test_user):
    request_data = {
        "username": "tithi",
        "email": "tithi@example.com",
        "first_name": "Tithi",
        "last_name": "Dam",
        "password": "test12345",
        "role": "user",
        "phone_number": "+1 11 111 1111"
    }

    response = client.post('/auth/', json=request_data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() != {}

    db = TestingSessionLocal()
    stmt = select(Users).where(Users.id == 2)
    user_model_result = db.scalars(statement=stmt).first()
    db.close()

    assert user_model_result.username == request_data.get('username') # pyright: ignore[reportOptionalMemberAccess]
    assert user_model_result.email == request_data.get('email') # pyright: ignore[reportOptionalMemberAccess]
    assert user_model_result.first_name == request_data.get('first_name') # pyright: ignore[reportOptionalMemberAccess]
    assert user_model_result.last_name == request_data.get('last_name') # pyright: ignore[reportOptionalMemberAccess]
    assert user_model_result.role == request_data.get('role') # pyright: ignore[reportOptionalMemberAccess]
    assert user_model_result.phone_number == request_data.get('phone_number') # pyright: ignore[reportOptionalMemberAccess]
    assert verify_password(request_data.get('password'), user_model_result.hashed_password ) == True # pyright: ignore[reportArgumentType, reportOptionalMemberAccess]

# test token generation
def test_token_generation(test_user):
    formdata = {
        "username": "shreyansh",
        "password": "test1234"
    }

    response = client.post("/auth/token", data=formdata)
    print("\n----\nhere I am:\n",response.json(), "\n----\n")

    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()

# Test Authenticate user function
def test_authenticate_user(test_user):
    db = TestingSessionLocal()

    authenticated_user = authenticate_user(test_user.username, 'test1234', db=db)
    assert authenticated_user is not None
    assert authenticated_user.username == test_user.username # pyright: ignore[reportAttributeAccessIssue]
    
    non_existent_user = authenticate_user('wrong_username', 'wrong_password', db=db)
    assert non_existent_user is False

    non_password_user = authenticate_user(test_user.username, 'wrong_password', db=db)
    assert non_password_user is False

# Test Token creation function
def test_create_access_token(test_user):
    username = 'testuser'
    user_id = 1
    role = 'user'
    expires_delta=timedelta(days=1)

    access_token = create_access_token(username, user_id, role, expires_delta)

    decoded_token = jwt.decode(
            token=access_token,
            key=SECRET_KEY,
            algorithms=[ALGORITHM],
            options={'verify_signature': False}
        )
    
    assert decoded_token['sub'] == username
    assert decoded_token['id'] == user_id
    assert decoded_token['role'] == role


# Test for current user function
@pytest.mark.asyncio
async def test_get_current_user(test_user):
    test_user_claims = {
        'sub': 'test_user',
        'id': '1',
        'role': 'user'
    }

    token = jwt.encode(claims=test_user_claims, algorithm=ALGORITHM, key=SECRET_KEY)

    current_user_value = await get_current_user(token)

    assert current_user_value['username'] == test_user_claims['sub']
    assert current_user_value['id'] == test_user_claims['id']
    assert current_user_value['role'] == test_user_claims['role']


@pytest.mark.asyncio
async def test_get_current_user_missing_payload():
    test_user_claims = {
        'sub': 'test_user'
    }

    with pytest.raises(HTTPException) as excinfo:
        token = jwt.encode(claims=test_user_claims, key=SECRET_KEY, algorithm=ALGORITHM)

        await get_current_user(token=token)

    assert excinfo.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert excinfo.value.detail == 'Unauthorized access'



    

