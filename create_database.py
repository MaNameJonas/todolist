"""Create Database Connection"""

import sqlalchemy
from datamodel import Base, todo_list #, todo_item


def connect_database():
    db_connection = sqlalchemy.create_engine("sqlite:///C:\\SEW_practice\\todolist\\todolist\\todolist_database.db")
    Base.metadata.create_all(db_connection)
    session_factory = sqlalchemy.orm.sessionmaker()
    session_factory.configure(bind=db_connection)

    if input() == "test":
        with session_factory() as session:
                new_event = todo_list(title="Brush teeth",
                                      colour="red")
                session.add(new_event)
                session.commit()

connect_database()
