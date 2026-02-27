from sqlalchemy import select
from routers.todos import get_db, get_current_user
from .utils import *

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user
        
# Test Get All Todos
def test_read_all_authenticated(test_todo):
    response = client.get('/todos/')
    sample_data_list = [{'id': 1, 'title': 'Learn PyTest', 'description': 'Learn PyTest Integration Testing', 'priority': 5, 'complete': False}]

    assert response.status_code == status.HTTP_200_OK
    assert response.json() != []
    assert response.json() == sample_data_list

# Test Get One Todo
def test_read_one_authenticated(test_todo):
    response = client.get("/todos/1")
    sample_data = {'id': 1, 'title': 'Learn PyTest', 'description': 'Learn PyTest Integration Testing', 'priority': 5, 'complete': False}

    assert response.status_code == status.HTTP_200_OK
    assert response.json() != []
    assert response.json() == sample_data

# Test Not Found as valid response for invalid todo_id
def test_read_one_authenticated_not_found():
    response = client.get("/todos/999")

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Could not find task requested.'}

# Test Creating a note
def test_create_todo(test_todo):
    request_data = {
        "title": "New ToDo in Test",
        "description": "Lorem ipsum dolor sit amet.",
        "priority": 4,
        "complete": False
    }

    response = client.post('/todos/', json=request_data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() != {}

    db = TestingSessionLocal()
    stmt = select(Todos).where(Todos.id == 2)
    todo_data_model = db.scalars(statement=stmt).first()

    db.close()

    assert isinstance(todo_data_model, Todos) == True
    assert todo_data_model.title == request_data.get('title') # pyright: ignore[reportOptionalMemberAccess]
    assert todo_data_model.description == request_data.get('description') # pyright: ignore[reportOptionalMemberAccess]
    assert todo_data_model.priority == request_data.get('priority') # pyright: ignore[reportOptionalMemberAccess]
    assert todo_data_model.complete == request_data.get('complete') # pyright: ignore[reportOptionalMemberAccess]

# Test Updating a note
def test_update_todo(test_todo):
    request_data = {
        "title": "Learn PyTest",
        "description": 'Learn PyTest Integration Testing',
        "priority": 4,
        "complete": True # This value has been changed
    }

    response = client.put('/todos/1', json=request_data)

    assert response.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()
    stmt = select(Todos).where(Todos.id == 1)
    todo_data_model = db.scalars(statement=stmt).first()
    db.close()

    assert todo_data_model.priority == request_data.get('priority') # pyright: ignore[reportOptionalMemberAccess]

# Test Updating a note with Not Found
def test_update_todo_not_found(test_todo):
    request_data = {
        "title": "Learn PyTest",
        "description": 'Learn PyTest Integration Testing',
        "priority": 4,
        "complete": True # This value has been changed
    }

    response = client.put('/todos/999', json=request_data)

    assert response.status_code == status.HTTP_404_NOT_FOUND

    assert response.json() == {'detail': 'requested Task does not exist.'}

# Test deleting a note
def test_delete_todo(test_todo):
    request_data = {
        "title": "New ToDo in Test to delete.",
        "description": "Lorem ipsum dolor sit amet.",
        "priority": 4,
        "complete": False
    }

    response = client.post('/todos/', json=request_data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() != {}

    db = TestingSessionLocal()
    stmt = select(Todos).where(Todos.id == 2)
    todo_data_model = db.scalars(statement=stmt).first()


    assert todo_data_model.title == request_data.get('title') # pyright: ignore[reportOptionalMemberAccess]

    response_del = client.delete('/todos/2')

    assert response_del.status_code == status.HTTP_204_NO_CONTENT
    
    stmt = select(Todos).where(Todos.id == 2)
    todo_data_model = db.scalars(statement=stmt).first()
    
    assert isinstance(todo_data_model, type(None)) == True
    
    db.close()

# Test deleting a note and not found
def test_delete_todo_not_found(test_todo):
    request_data = {
        "title": "New ToDo in Test to delete.",
        "description": "Lorem ipsum dolor sit amet.",
        "priority": 4,
        "complete": False
    }

    response = client.post('/todos/', json=request_data)

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() != {}

    db = TestingSessionLocal()
    stmt = select(Todos).where(Todos.id == 2)
    todo_data_model = db.scalars(statement=stmt).first()
    db.close()


    assert todo_data_model.title == request_data.get('title') # pyright: ignore[reportOptionalMemberAccess]

    response_del = client.delete('/todos/999')

    assert response_del.status_code == status.HTTP_404_NOT_FOUND
    assert response_del.json() == {'detail': 'Task not found.'}
     
