from sqlalchemy import select
from routers.users import get_db, get_current_user # Always import from the file you are creating the test for.
from .utils import *

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

# Test User Details
def test_read_user_details(test_user):
    response = client.get('/user/get-user/')

    response_data = response.json()

    assert response.status_code == status.HTTP_200_OK

    assert response_data.get('id') == test_user.id
    assert response_data.get('username') == test_user.username
    assert response_data.get('email') == test_user.email
    assert response_data.get('first_name') == test_user.first_name
    assert response_data.get('last_name') == test_user.last_name
    assert response_data.get('is_active') == test_user.is_active
    assert response_data.get('phone_number') == test_user.phone_number
    assert response_data.get('role') == test_user.role
    assert response_data.get('hashed_password') == test_user.hashed_password

# Test User Details No User Found
def test_read_user_details_not_found(test_user):

    app.dependency_overrides[get_current_user] = lambda: None
    try:
        response = client.get('/user/get-user/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {'detail': 'Failed to authenticate user.'}

    finally:
        app.dependency_overrides[get_current_user] = override_get_current_user


# Test User Update Details
def test_update_user_details(test_user):
    request_data = {
        "username": "shreyansh",
        "email": "shreyansh_2@example.com",
        "first_name": "Shreyansh",
        "last_name": "C. Jain",
        "is_active": True,
        "phone_number": "9901049003",
        "role": "admin"
    }

    response = client.put('/user/update-details/', json=request_data)

    response_data = response.json()

    assert response.status_code == status.HTTP_200_OK

    assert response_data.get('id') == test_user.id
    assert response_data.get('username') == request_data.get('username')
    assert response_data.get('email') == request_data.get('email')
    assert response_data.get('first_name') == request_data.get('first_name')
    assert response_data.get('last_name') == request_data.get('last_name')
    assert response_data.get('is_active') == request_data.get('is_active')
    assert response_data.get('phone_number') == request_data.get('phone_number')
    assert response_data.get('role') == request_data.get('role')
    assert response_data.get('hashed_password') == test_user.hashed_password

# Test User Update details with not found
def test_update_user_details_not_found(test_user):
    request_data = {
        "username": "shreyansh",
        "email": "shreyansh_3@example.com",
        "first_name": "Shreyansh",
        "last_name": "C. Jain",
        "is_active": True,
        "phone_number": "9901049003",
        "role": "admin"
    }

    app.dependency_overrides[get_current_user] = lambda: None

    try:
        response = client.put('/user/update-details/', json=request_data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {'detail': 'Failed to authenticate user.'}

    finally:
        app.dependency_overrides[get_current_user] = override_get_current_user


# Test Update Password
def test_update_password(test_user):
    request_form = {
        "password": "test1234",
        "new_password": "test12345"
    }
    response = client.put('/user/update-password/', json=request_form)

    old_hashed_password = test_user.hashed_password

    db = TestingSessionLocal()
    stmt = select(Users).where(Users.id ==1)
    user_model_data = db.scalars(statement=stmt).first()
    new_hashed_password = user_model_data.hashed_password # pyright: ignore[reportOptionalMemberAccess]
    db.close()

    assert response.status_code == status.HTTP_204_NO_CONTENT

    assert verify_password(request_form.get('password'), old_hashed_password) == True # pyright: ignore[reportArgumentType]
    assert verify_password(request_form.get('new_password'), new_hashed_password) == True # pyright: ignore[reportArgumentType]


# Test Update Password User Not Found
def test_update_password_not_found(test_user):
    request_form = {
        "password": "test1234",
        "new_password": "test12345"
    }

    app.dependency_overrides[get_current_user] = lambda: None

    try:
        response = client.put('/user/update-password/', json=request_form)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {'detail': 'Failed to authenticate user.'}

    finally:
        app.dependency_overrides[get_current_user] = override_get_current_user
        

# Test Delete User
def test_delete_user(test_user):
    new_user_data = Users(
        email='tithi@example.com',
        username='tithi',
        first_name='Tithi',
        last_name='Dam',
        hashed_password=hash_password('test1234'),
        role='user',
        is_active=True,
        phone_number='+2 22 222 2222'
    )

    db = TestingSessionLocal()
    db.add(new_user_data)
    db.commit()
    db.refresh(new_user_data)
    db.close()

    app.dependency_overrides[get_current_user] = lambda: {'username': 'tithi', 'id': 2, 'role': 'role'}
    try:
        response = client.delete('/user/delete-user/')
        response_data = response.json()
        

        assert response.status_code == status.HTTP_200_OK
        assert response_data.get('id') == new_user_data.id
        assert response_data.get('username') == new_user_data.username
        assert response_data.get('email') == new_user_data.email
        assert response_data.get('first_name') == new_user_data.first_name
        assert response_data.get('last_name') == new_user_data.last_name
        assert response_data.get('is_active') == new_user_data.is_active
        assert response_data.get('phone_number') == new_user_data.phone_number
        assert response_data.get('role') == new_user_data.role

    finally:
        app.dependency_overrides[get_current_user] = override_get_current_user
        response = client.get('/user/get-user/')

        response_data = response.json()

        assert response.status_code == status.HTTP_200_OK
        assert response_data.get('id') == test_user.id
        assert response_data.get('username') == test_user.username


# Test Delete User Not Fond
def test_delete_user_not_found(test_user):
    app.dependency_overrides[get_current_user] = lambda: None
    try:
        response = client.delete('/user/delete-user/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {'detail': 'Failed to Authenticate User'}

    finally:
        app.dependency_overrides[get_current_user] = override_get_current_user
        