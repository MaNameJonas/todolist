# import sys
# sys.path.append("C:\SEW_practice\todolist\test")
# sys.path.append("C:\SEW_practice\todolist")

import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
import todolist
from todolist.todo_list import Todolist
from todolist.datamodel import Base, todo_list, todo_item
# from todolist.todo_list import Todolist
# import pytest


def test_000_module_import():
    # assert None
    import todolist.datamodel
    assert todolist.datamodel


def test_001_create_todo_list(tmpdir):
    title = "Test List"
    colour = "red"
    db_file = tmpdir.join("test_todolist_database.db")
    db_connection = sqlalchemy.create_engine(f'sqlite:///{db_file}', echo=True)
    Base.metadata.create_all(db_connection)
    session_factory = sqlalchemy.orm.sessionmaker()
    session_factory.configure(bind=db_connection)
    mock_todo_list = Todolist()

    mock_todo_list.create_todo_list(title, colour)

    assert mock_todo_list.select(todo_list, "colour", colour, "title") is not None
    assert title in [row[0] for row in mock_todo_list.select(todo_list, "colour", colour, "title")]
    assert colour in [row[0] for row in mock_todo_list.select(todo_list, "title", title, "colour")]

    mock_todo_list.delete(todo_list, "title", title)


def test_002_create_todo_item():
    title = "Test Todo Item"
    description = "This is a test todo item"
    list_title = "Test Todo List"

    db_connection = sqlalchemy.create_engine('sqlite:///:memory:', echo=True)
    Base.metadata.create_all(db_connection)
    session_factory = sqlalchemy.orm.sessionmaker()
    session_factory.configure(bind=db_connection)
    todo_list1 = Todolist()
    todo_list1.create_todo_list("Test Todo List", "red")

    todo_list1.create_todo_item(title, description, list_title)

    assert todo_list1.select(todo_item, "title", title, "description") is not None
    assert title in [row[0] for row in todo_list1.select(todo_item, "description", description, "title")]
    assert description in [row[0] for row in todo_list1.select(todo_item, "title", title, "description")]
    assert False in [row[0] for row in todo_list1.select(todo_item, "title", title, "iscomplete")]
    # assert id = id

    todo_list1.delete(todo_item, "title", title)


def test_003_delete(tmpdir):
    title = "Test List"
    colour = "test_colour"
    db_file = tmpdir.join("test_todolist_database.db")
    db_connection = sqlalchemy.create_engine(f'sqlite:///{db_file}', echo=True)
    Base.metadata.create_all(db_connection)
    session_factory = sqlalchemy.orm.sessionmaker()
    session_factory.configure(bind=db_connection)
    mock_todo_list = Todolist()

    mock_todo_list.create_todo_list(title, colour)
    mock_todo_list.delete(todo_list, "title", title)
    assert mock_todo_list.check_existence(todo_list, "title", title) is False


def test_004_update(tmpdir):
    title = "Test List"
    new_title = "Change_Test_Title"
    colour = "test_colour"
    db_file = tmpdir.join("test_todolist_database.db")
    db_connection = sqlalchemy.create_engine(f'sqlite:///{db_file}', echo=True)
    Base.metadata.create_all(db_connection)
    session_factory = sqlalchemy.orm.sessionmaker()
    session_factory.configure(bind=db_connection)
    mock_todo_list = Todolist()

    mock_todo_list.create_todo_list(title, colour)

    assert mock_todo_list.select(todo_list, "colour", colour, "title") is not None
    mock_todo_list.update(todo_list, "title", title, new_title, "title")
    assert new_title in [row[0] for row in mock_todo_list.select(todo_list, "colour", colour, "title")]

    mock_todo_list.delete(todo_list, "title", new_title)


def test_005_select(tmpdir):
    title = "Test List"
    colour = "test_colour"
    db_file = tmpdir.join("test_todolist_database.db")
    db_connection = sqlalchemy.create_engine(f'sqlite:///{db_file}', echo=True)
    Base.metadata.create_all(db_connection)
    session_factory = sqlalchemy.orm.sessionmaker()
    session_factory.configure(bind=db_connection)
    mock_todo_list = Todolist()
    new_session = session_factory()
    column = "title"

    mock_todo_list.create_todo_list(title, colour)

    assert mock_todo_list.select(todo_list, "colour", colour, "title") is not None
    mock_todo_list_title = mock_todo_list.select(todo_list, "colour", colour, "title")
    with new_session as session:
        assert mock_todo_list_title[0] == session.query(todo_list).filter(getattr(todo_list, column) == title).all()

    mock_todo_list.delete(todo_list, "title", title)
