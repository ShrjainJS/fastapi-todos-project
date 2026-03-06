from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
# from sqlalchemy.ext.declarative import declarative_base

# SQLALCHEMY_DB_URL_SQLite = "sqlite:///./todosapp.db"
SQLALCHEMY_DB_URL_POSTGRESQL = os.environ.get("DATABASE_URL") # This is to check with render
# SQLALCHEMY_DB_URL_POSTGRESQL = "postgresql://postgres:postgres@localhost/TodoApplicationDatabase"

# connect_args is needed for SQLite only
# engine = create_engine(url=SQLALCHEMY_DB_URL_SQLite, connect_args={'check_same_thread': False})
engine = create_engine(url=SQLALCHEMY_DB_URL_POSTGRESQL, connect_args={"sslmode": "require"}) # pyright: ignore[reportArgumentType]
# engine = create_engine(url=SQLALCHEMY_DB_URL_POSTGRESQL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base=declarative_base()
