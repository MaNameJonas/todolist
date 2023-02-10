# import sys
# sys.path.append("C:\SEW_practice\todolist\test")
# sys.path.append("C:\SEW_practice\todolist")

import sqlalchemy
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
    # Arrange
    title = "Test List"
    colour = "red"
    db_file = tmpdir.join("todolist_database.db")
    db_connection = sqlalchemy.create_engine(f"sqlite:///{db_file}")
    Base.metadata.create_all(db_connection)
    session_factory = sqlalchemy.orm.sessionmaker(bind=db_connection)
    todo_list_repo = Todolist()

    # Act
    todo_list_repo.create_todo_list(title, colour)

    # Assert
    with session_factory() as session:
        result = session.query(todolist.todo_list).filter_by(title=title).first()
        assert result is not None
        assert result.title == title
        assert result.colour == colour
