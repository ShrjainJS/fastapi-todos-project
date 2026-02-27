from sqlalchemy import select
from routers.admin import get_db, get_current_user # Always import from the file you are creating the test for.
from .utils import *

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

# Test Admin user details
def test_user_detail(test_user):
    response = client.get('/admin/admin-user/')

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

# Test User Details Non Admin User
def test_user_detail_non_admin(test_user):

    app.dependency_overrides[get_current_user] = lambda: {'username': 'tithi', 'id': 2, 'role': 'user'}
    try:
        response = client.get('/admin/admin-user/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {'detail': 'Unauthorize access.'}

    finally:
        app.dependency_overrides[get_current_user] = override_get_current_user

# Test User Details No User Found
def test_user_detail_not_found(test_user):

    app.dependency_overrides[get_current_user] = lambda: None
    try:
        response = client.get('/admin/admin-user/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {'detail': 'Unauthorize access.'}

    finally:
        app.dependency_overrides[get_current_user] = override_get_current_user

# Test Get All User Details
def test_all_user_details(test_user):
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

    response = client.get('/admin/all-users/')

    response_data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response_data, list)
    assert len(response_data) > 0
    assert set([1,2]).issubset(set([user_data_in_response.get('id') for user_data_in_response in response_data]))

# Test Get All User Details - Non Admin
def test_all_user_details_non_admin(test_user):
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

    app.dependency_overrides[get_current_user] = lambda: {'username': 'tithi', 'id': 2, 'role': 'user'}
    try:
        response = client.get('/admin/all-users/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {'detail': 'Unauthorize access.'}
    finally:
        app.dependency_overrides[get_current_user] = override_get_current_user

# Test Get All User Details - No User
def test_all_user_details_not_found(test_user):

    app.dependency_overrides[get_current_user] = lambda: None
    try:
        response = client.get('/admin/all-users/')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {'detail': 'Unauthorize access.'}
    finally:
        app.dependency_overrides[get_current_user] = override_get_current_user

# Test Get User Details by ID - Admin
def test_user_details_by_id(test_user):
    new_user_password = 'test1234'
    new_user_data = Users(
        email='tithi@example.com',
        username='tithi',
        first_name='Tithi',
        last_name='Dam',
        hashed_password=hash_password(new_user_password),
        role='user',
        is_active=True,
        phone_number='+2 22 222 2222'
    )

    db = TestingSessionLocal()
    db.add(new_user_data)
    db.commit()
    db.refresh(new_user_data)
    db.close()

    response = client.get('/admin/user-by-id/2')

    response_data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response_data, dict)
    assert response_data.get('id') == new_user_data.id
    assert response_data.get('username') == new_user_data.username
    assert response_data.get('email') == new_user_data.email
    assert response_data.get('first_name') == new_user_data.first_name
    assert response_data.get('last_name') == new_user_data.last_name
    assert response_data.get('role') == new_user_data.role
    assert response_data.get('is_active') == new_user_data.is_active
    assert response_data.get('phone_number') == new_user_data.phone_number
    assert verify_password(new_user_password, new_user_data.hashed_password)

# Test Get User Details by ID - Non Admin
def test_user_details_by_id_non_admin(test_user):

    app.dependency_overrides[get_current_user] = lambda: {'username': 'tithi', 'id': 2, 'role': 'user'}
    try:
        response = client.get('/admin/user-by-id/2')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {'detail': 'Unauthorize access.'}
    
    finally:
        app.dependency_overrides[get_current_user] = override_get_current_user

# Test Get User Details by ID - No User
def test_user_details_by_id_not_found(test_user):

    app.dependency_overrides[get_current_user] = lambda: None
    try:
        response = client.get('/admin/user-by-id/2')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {'detail': 'Unauthorize access.'}
    
    finally:
        app.dependency_overrides[get_current_user] = override_get_current_user

# Test Get User Details by username - Admin
def test_user_details_by_username(test_user):
    new_user_password = 'test1234'
    new_user_data = Users(
        email='tithi@example.com',
        username='tithi',
        first_name='Tithi',
        last_name='Dam',
        hashed_password=hash_password(new_user_password),
        role='user',
        is_active=True,
        phone_number='+2 22 222 2222'
    )

    db = TestingSessionLocal()
    db.add(new_user_data)
    db.commit()
    db.refresh(new_user_data)
    db.close()

    response = client.get('/admin/user-by-username/tithi')

    response_data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response_data, dict)
    assert response_data.get('id') == new_user_data.id
    assert response_data.get('username') == new_user_data.username
    assert response_data.get('email') == new_user_data.email
    assert response_data.get('first_name') == new_user_data.first_name
    assert response_data.get('last_name') == new_user_data.last_name
    assert response_data.get('role') == new_user_data.role
    assert response_data.get('is_active') == new_user_data.is_active
    assert response_data.get('phone_number') == new_user_data.phone_number
    assert verify_password(new_user_password, new_user_data.hashed_password)

# Test Get User Details by username - Non Admin
def test_user_details_by_username_non_admin(test_user):

    app.dependency_overrides[get_current_user] = lambda: {'username': 'tithi', 'id': 2, 'role': 'user'}
    try:
        response = client.get('/admin/user-by-username/tithi')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {'detail': 'Unauthorize access.'}
    
    finally:
        app.dependency_overrides[get_current_user] = override_get_current_user

# Test Get User Details by username - No User
def test_user_details_by_username_not_found(test_user):

    app.dependency_overrides[get_current_user] = lambda: None
    try:
        response = client.get('/admin/user-by-username/tithi')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {'detail': 'Unauthorize access.'}
    
    finally:
        app.dependency_overrides[get_current_user] = override_get_current_user

# Test Update User Details by ID - Admin
def test_update_user_details_by_id(test_user):
    request_data = {
        "username": "shreyansh",
        "email": "shreyansh@example.com",
        "first_name": "Shreyansh",
        "last_name": "C. Jain",
        "is_active": True,
        "role": "admin",
        "phone_number": "9873798987"
    }

    response = client.put("/admin/user-by-id/1", json=request_data)

    response_data = response.json()

    assert response.status_code == status.HTTP_200_OK
    
    assert response_data.get('id') == test_user.id
    assert response_data.get('username') == request_data.get('username') # pyright: ignore[reportAttributeAccessIssue]
    assert response_data.get('email') == request_data.get('email') # pyright: ignore[reportAttributeAccessIssue]
    assert response_data.get('first_name') == request_data.get('first_name') # pyright: ignore[reportAttributeAccessIssue]
    assert response_data.get('last_name') == request_data.get('last_name') # pyright: ignore[reportAttributeAccessIssue]
    assert response_data.get('is_active') == request_data.get('is_active') # pyright: ignore[reportAttributeAccessIssue]
    assert response_data.get('phone_number') == request_data.get('phone_number') # pyright: ignore[reportAttributeAccessIssue]
    assert response_data.get('role') == request_data.get('role') # pyright: ignore[reportAttributeAccessIssue]

# Test Update User Details by ID - Non Admin
def test_update_user_details_by_id_non_admin(test_user):
    app.dependency_overrides[get_current_user] = lambda: {'username': 'tithi', 'id': 2, 'role': 'user'}
    try:
        request_data = {
            "username": "shreyansh",
            "email": "shreyansh@example.com",
            "first_name": "Shreyansh",
            "last_name": "C. Jain",
            "is_active": True,
            "role": "admin",
            "phone_number": "9873798987"
        }

        response = client.put("/admin/user-by-id/1", json=request_data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {'detail': 'Unauthorize access.'}

    finally:
        app.dependency_overrides[get_current_user] = override_get_current_user

# Test Update User Details by ID - No User
def test_update_user_details_by_id_not_found(test_user):
    app.dependency_overrides[get_current_user] = lambda: None
    try:
        request_data = {
            "username": "shreyansh",
            "email": "shreyansh@example.com",
            "first_name": "Shreyansh",
            "last_name": "C. Jain",
            "is_active": True,
            "role": "admin",
            "phone_number": "9873798987"
        }

        response = client.put("/admin/user-by-id/1", json=request_data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {'detail': 'Unauthorize access.'}

    finally:
        app.dependency_overrides[get_current_user] = override_get_current_user

# Test Update User Details by username - Admin
def test_update_user_details_by_username(test_user):
    request_data = {
        "username": "shreyansh",
        "email": "shreyansh@example.com",
        "first_name": "Shreyansh",
        "last_name": "C. Jain",
        "is_active": True,
        "role": "admin",
        "phone_number": "9610098987"
    }

    response = client.put("/admin/user-by-username/shreyansh", json=request_data)

    response_data = response.json()

    assert response.status_code == status.HTTP_200_OK
    
    assert response_data.get('id') == test_user.id
    assert response_data.get('username') == request_data.get('username') # pyright: ignore[reportAttributeAccessIssue]
    assert response_data.get('email') == request_data.get('email') # pyright: ignore[reportAttributeAccessIssue]
    assert response_data.get('first_name') == request_data.get('first_name') # pyright: ignore[reportAttributeAccessIssue]
    assert response_data.get('last_name') == request_data.get('last_name') # pyright: ignore[reportAttributeAccessIssue]
    assert response_data.get('is_active') == request_data.get('is_active') # pyright: ignore[reportAttributeAccessIssue]
    assert response_data.get('phone_number') == request_data.get('phone_number') # pyright: ignore[reportAttributeAccessIssue]
    assert response_data.get('role') == request_data.get('role') # pyright: ignore[reportAttributeAccessIssue]

# Test Update User Details by Username - Non Admin
def test_update_user_details_by_username_non_admin(test_user):
    app.dependency_overrides[get_current_user] = lambda: {'username': 'tithi', 'id': 2, 'role': 'user'}
    try:
        request_data = {
            "username": "shreyansh",
            "email": "shreyansh@example.com",
            "first_name": "Shreyansh",
            "last_name": "C. Jain",
            "is_active": True,
            "role": "admin",
            "phone_number": "9873798987"
        }

        response = client.put("/admin/user-by-username/shreyansh", json=request_data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {'detail': 'Unauthorize access.'}

    finally:
        app.dependency_overrides[get_current_user] = override_get_current_user

# Test Update User Details by Username - No User
def test_update_user_details_by_username_not_found(test_user):
    app.dependency_overrides[get_current_user] = lambda: None
    try:
        request_data = {
            "username": "shreyansh",
            "email": "shreyansh@example.com",
            "first_name": "Shreyansh",
            "last_name": "C. Jain",
            "is_active": True,
            "role": "admin",
            "phone_number": "9873798987"
        }

        response = client.put("/admin/user-by-username/shreyansh", json=request_data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {'detail': 'Unauthorize access.'}

    finally:
        app.dependency_overrides[get_current_user] = override_get_current_user

# Test Update Password by ID - Admin
def test_update_user_password_by_id(test_user):
    request_form = {
        "password": "test1234",
        "new_password": "test12345"
    }

    old_hashed_password = test_user.hashed_password

    response = client.put('/admin/user-by-id/password/1', json=request_form)

    db = TestingSessionLocal()
    stmt = select(Users).where(Users.id ==1)
    user_model_data = db.scalars(statement=stmt).first()
    new_hashed_password = user_model_data.hashed_password # pyright: ignore[reportOptionalMemberAccess]
    db.close()

    assert response.status_code == status.HTTP_200_OK

    assert verify_password(request_form.get('password'), old_hashed_password) # pyright: ignore[reportArgumentType]
    assert verify_password(request_form.get('new_password'), new_hashed_password) # pyright: ignore[reportArgumentType]

# Test Update password by ID - Non Admin
def test_update_user_password_by_id_non_admin(test_user):
    app.dependency_overrides[get_current_user] = lambda: {'username': 'tithi', 'id': 2, 'role': 'user'}

    try:
        request_form = {
            "password": "test1234",
            "new_password": "test12345"
        }

        response = client.put('/admin/user-by-id/password/1', json=request_form)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {'detail': 'Unauthorize access.'}

    finally:
        app.dependency_overrides[get_current_user] = override_get_current_user 

# Test Update password by ID - No User
def test_update_user_password_by_id_not_found(test_user):
    app.dependency_overrides[get_current_user] = lambda: None

    try:
        request_form = {
            "password": "test1234",
            "new_password": "test12345"
        }

        response = client.put('/admin/user-by-id/password/1', json=request_form)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {'detail': 'Unauthorize access.'}

    finally:
        app.dependency_overrides[get_current_user] = override_get_current_user 

# Test Update Password by Username - Admin
def test_update_user_password_by_username(test_user):
    request_form = {
        "password": "test1234",
        "new_password": "test12345"
    }

    old_hashed_password = test_user.hashed_password

    response = client.put('/admin/user-by-username/password/shreyansh', json=request_form)

    db = TestingSessionLocal()
    stmt = select(Users).where(Users.id ==1)
    user_model_data = db.scalars(statement=stmt).first()
    new_hashed_password = user_model_data.hashed_password # pyright: ignore[reportOptionalMemberAccess]
    db.close()

    assert response.status_code == status.HTTP_200_OK

    assert verify_password(request_form.get('password'), old_hashed_password) # pyright: ignore[reportArgumentType]
    assert verify_password(request_form.get('new_password'), new_hashed_password) # pyright: ignore[reportArgumentType]

# Test Update password by username - Non Admin
def test_update_user_password_by_username_non_admin(test_user):
    app.dependency_overrides[get_current_user] = lambda: {'username': 'tithi', 'id': 2, 'role': 'user'}

    try:
        request_form = {
            "password": "test1234",
            "new_password": "test12345"
        }

        response = client.put('/admin/user-by-username/password/shreyansh', json=request_form)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {'detail': 'Unauthorize access.'}

    finally:
        app.dependency_overrides[get_current_user] = override_get_current_user 

# Test Update password by username - No User
def test_update_user_password_by_username_not_found(test_user):
    app.dependency_overrides[get_current_user] = lambda: None

    try:
        request_form = {
            "password": "test1234",
            "new_password": "test12345"
        }

        response = client.put('/admin/user-by-username/password/shreyansh', json=request_form)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {'detail': 'Unauthorize access.'}

    finally:
        app.dependency_overrides[get_current_user] = override_get_current_user 

# Test Delete User - Admin
def test_delete_user_by_id(test_user):
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

    try:
        response = client.delete('/admin/user-by-id/2')

        assert response.status_code == status.HTTP_204_NO_CONTENT
        

    finally:
        app.dependency_overrides[get_current_user] = override_get_current_user

# Test Delete User - Non Admin
def test_delete_user_by_id_non_admin(test_user):
    new_user_data_list = [
        Users(
            email='tithi@example.com',
            username='tithi',
            first_name='Tithi',
            last_name='Dam',
            hashed_password=hash_password('test1234'),
            role='user',
            is_active=True,
            phone_number='+2 22 222 2222'
        ),
        Users(
            email='sonu@example.com',
            username='sonu',
            first_name='Sonu',
            last_name='Bohara',
            hashed_password=hash_password('test1234'),
            role='user',
            is_active=True,
            phone_number='+3 33 333 3333'
        )
    ]

    db = TestingSessionLocal()
    db.add_all(new_user_data_list)
    db.commit()
    [db.refresh(each_user) for each_user in new_user_data_list]
    db.close()

    try:
        app.dependency_overrides[get_current_user] = lambda: {'username': 'tithi', 'id': 2, 'role': 'role'}
        response = client.delete('/admin/user-by-id/3')
    
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {'detail': 'Unauthorize access.'}
        

    finally:
        app.dependency_overrides[get_current_user] = override_get_current_user

# Test Delete User - No User
def test_delete_user_by_id_not_found(test_user):
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

    try:
        app.dependency_overrides[get_current_user] = lambda: None
        response = client.delete('/admin/user-by-id/2')
    
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {'detail': 'Unauthorize access.'}
        

    finally:
        app.dependency_overrides[get_current_user] = override_get_current_user

# Test Get All Task - Admin
def test_get_all_tasks(test_user, test_todo):
    response = client.get("/admin/all-todos/")

    sample_data_list = [{'id': 1, 'title': 'Learn PyTest', 'description': 'Learn PyTest Integration Testing', 'priority': 5, 'complete': False}]

    assert response.status_code == status.HTTP_200_OK
    assert response.json() != []
    assert response.json() == sample_data_list

# Test Get All Task - Non Admin
def test_get_all_tasks_non_admin(test_user, test_todo):
    app.dependency_overrides[get_current_user] = lambda: {'username': 'tithi', 'id': 2, 'role': 'role'}
    
    try:
        response = client.get("/admin/all-todos/")


        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {'detail': 'Unauthorize access.'}
    finally:
        app.dependency_overrides[get_current_user] = override_get_current_user

# Test Get All Task - No User
def test_get_all_tasks_not_found(test_user, test_todo):
    app.dependency_overrides[get_current_user] = lambda: None
    
    try:
        response = client.get("/admin/all-todos/")


        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {'detail': 'Unauthorize access.'}
    finally:
        app.dependency_overrides[get_current_user] = override_get_current_user

# Test create todo - Admin
def test_create_todo(test_todo):
    request_data = {
        "title": "New ToDo in Test",
        "description": "Lorem ipsum dolor sit amet.",
        "priority": 4,
        "complete": False
    }

    response = client.post('/admin/todos/', json=request_data)

    db = TestingSessionLocal()

    stmt = select(Todos).where(Todos.id == 2)
    todo_data_model = db.scalars(statement=stmt).first()
    db.refresh(todo_data_model)
    db.close()


    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() != {}

    assert todo_data_model.title == request_data.get('title') # pyright: ignore[reportOptionalMemberAccess]
    assert todo_data_model.description == request_data.get('description') # pyright: ignore[reportOptionalMemberAccess]
    assert todo_data_model.priority == request_data.get('priority') # pyright: ignore[reportOptionalMemberAccess]
    assert todo_data_model.complete == request_data.get('complete') # pyright: ignore[reportOptionalMemberAccess]

# Test create todo - Non Admin
def test_create_todo_non_admin(test_user, test_todo):
    request_data = {
        "title": "New ToDo in Test",
        "description": "Lorem ipsum dolor sit amet.",
        "priority": 4,
        "complete": False
    }


    db = TestingSessionLocal()

    stmt = select(Todos).where(Todos.id == 2)
    todo_data_model = db.scalars(statement=stmt).first()
    
    db.close()

    app.dependency_overrides[get_current_user] = lambda: {'username': 'tithi', 'id': 2, 'role': 'role'}
    
    try:

        response = client.post('/admin/todos/', json=request_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {'detail': 'Unauthorize access.'}
    
    finally:
        app.dependency_overrides[get_current_user] = override_get_current_user

# Test create todo - No User
def test_create_todo_not_found(test_user, test_todo):
    request_data = {
        "title": "New ToDo in Test",
        "description": "Lorem ipsum dolor sit amet.",
        "priority": 4,
        "complete": False
    }


    db = TestingSessionLocal()

    stmt = select(Todos).where(Todos.id == 2)
    todo_data_model = db.scalars(statement=stmt).first()
    
    db.close()

    app.dependency_overrides[get_current_user] = lambda: None
    
    try:

        response = client.post('/admin/todos/', json=request_data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {'detail': 'Unauthorize access.'}
    
    finally:
        app.dependency_overrides[get_current_user] = override_get_current_user

# Test Get One Todo - admin
def test_read_one_todo(test_todo, test_user):
    response = client.get("/admin/todos/1")
    sample_data = {'id': 1, 'title': 'Learn PyTest', 'description': 'Learn PyTest Integration Testing', 'priority': 5, 'complete': False}

    assert response.status_code == status.HTTP_200_OK
    assert response.json() != []
    assert response.json() == sample_data

# Test Get One Todo - Non Admin
def test_read_one_todo_non_admin(test_user, test_todo):
    app.dependency_overrides[get_current_user] = lambda: {'username': 'tithi', 'id': 2, 'role': 'role'}
    
    try:

        response = client.get('/admin/todos/1')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {'detail': 'Unauthorize access.'}
    
    finally:
        app.dependency_overrides[get_current_user] = override_get_current_user

# Test Get One Todo - No User
def test_read_one_todo_not_found(test_user, test_todo):
    app.dependency_overrides[get_current_user] = lambda: None
    
    try:

        response = client.get('/admin/todos/1')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {'detail': 'Unauthorize access.'}
    
    finally:
        app.dependency_overrides[get_current_user] = override_get_current_user

# Test Updating a note - Admin
def test_update_todo(test_user, test_todo):
    request_data = {
        "title": "Learn PyTest",
        "description": 'Learn PyTest Integration Testing',
        "priority": 4,
        "complete": True # This value has been changed
    }

    response = client.put('/admin/todos/1', json=request_data)

    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    stmt = select(Todos).where(Todos.id == 1)
    todo_data_model = db.scalars(statement=stmt).first()
    db.close()

    assert todo_data_model.priority == request_data.get('priority') # pyright: ignore[reportOptionalMemberAccess]

# Test updating a note - Non Admin
def test_update_todo_non_admin(test_user, test_todo):
    app.dependency_overrides[get_current_user] = lambda: {'username': 'tithi', 'id': 2, 'role': 'role'}

    try:
        request_data = {
            "title": "Learn PyTest",
            "description": 'Learn PyTest Integration Testing',
            "priority": 4,
            "complete": True # This value has been changed
        }

        response = client.put('/admin/todos/1', json=request_data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {'detail': 'Unauthorize access.'}
    
    finally:
        app.dependency_overrides[get_current_user] = override_get_current_user

# Test updating a note - No User
def test_update_todo_not_found(test_user, test_todo):
    app.dependency_overrides[get_current_user] = lambda: None

    try:
        request_data = {
            "title": "Learn PyTest",
            "description": 'Learn PyTest Integration Testing',
            "priority": 4,
            "complete": True # This value has been changed
        }

        response = client.put('/admin/todos/1', json=request_data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {'detail': 'Unauthorize access.'}
    
    finally:
        app.dependency_overrides[get_current_user] = override_get_current_user


# Test deleting a note
def test_delete_todo(test_todo):
    request_data = {
        "title": "New ToDo in Test to delete.",
        "description": "Lorem ipsum dolor sit amet.",
        "priority": 4,
        "complete": False
    }

    response = client.post('/admin/todos/', json=request_data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() != {}

    db = TestingSessionLocal()
    stmt = select(Todos).where(Todos.id == 2)
    todo_data_model = db.scalars(statement=stmt).first()


    assert todo_data_model.title == request_data.get('title') # pyright: ignore[reportOptionalMemberAccess]

    response_del = client.delete('/admin/todos/2')

    assert response_del.status_code == status.HTTP_204_NO_CONTENT
    
    stmt = select(Todos).where(Todos.id == 2)
    todo_data_model = db.scalars(statement=stmt).first()
    
    assert isinstance(todo_data_model, type(None)) == True
    
    db.close()

# Test deleting a note - Non Admin
def test_delete_todo_non_admin(test_todo):
    app.dependency_overrides[get_current_user] = lambda: {'username': 'tithi', 'id': 2, 'role': 'role'}

    try:
        response = client.delete('/admin/todos/1')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {'detail': 'Unauthorize access.'}

    finally:
        app.dependency_overrides[get_current_user] = override_get_current_user

# Test deleting a note - No User
def test_delete_todo_not_found(test_todo):
    app.dependency_overrides[get_current_user] = lambda: None

    try:
        response = client.delete('/admin/todos/1')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json() == {'detail': 'Unauthorize access.'}

    finally:
        app.dependency_overrides[get_current_user] = override_get_current_user



