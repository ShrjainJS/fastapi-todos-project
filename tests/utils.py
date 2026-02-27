# This file is to accomodate for re-usability function.
from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from database.database import Base
from fastapi.testclient import TestClient
from fastapi import status, HTTPException
import pytest
from main import app
from models.db_models import Todos, Users
from utils.auth_utils import hash_password, verify_password

SQLALCHEMY_TEST_DB_URL_SQLite = "sqlite:///./testdb.db"

engine = create_engine(
    url=SQLALCHEMY_TEST_DB_URL_SQLite,
    connect_args={'check_same_thread': False},
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# print("\n-----\n", Base.metadata.tables.keys(), "\n-----\n")

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_current_user():
    return {'username': 'shreyansh', 'id': 1, 'role': 'admin'}

client = TestClient(app)

@pytest.fixture
def test_todo():
    todo = Todos(
        title='Learn PyTest',
        description='Learn PyTest Integration Testing',
        priority=5,
        complete=False,
        owner_id=1
    )
    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo

    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos"))
        connection.commit()

@pytest.fixture
def test_user():
    user = Users(
        email='shreyansh@example.com',
        username='shreyansh',
        first_name='Shreyansh',
        last_name='Jain',
        hashed_password=hash_password('test1234'),
        role='admin',
        is_active=True,
        phone_number='+1 11 111 1111'
    )

    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    db.refresh(user)
    yield user

    with engine.connect() as connection:
        connection.execute(text('DELETE FROM users'))
        connection.commit()