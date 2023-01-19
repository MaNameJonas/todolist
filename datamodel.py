import sqlalchemy
import sqlalchemy.ext.declarative
from sqlalchemy.orm import relationship

Base = sqlalchemy.ext.declarative.declarative_base()

class todo_item(Base):
    """Datamodel creation for Todo Item Table (1/2)"""

    __tablename__ = "todo_item"
    todo_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    title = sqlalchemy.Column(sqlalchemy.String)
    description = sqlalchemy.Column(sqlalchemy.String)
    iscomplete = sqlalchemy.Column(sqlalchemy.Boolean)
    todo_list_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("todo_list.todo_list_id"))


class todo_list(Base):
    """Datamodel creation for Todo List Table (2/2)"""

    __tablename__ = "todo_list"
    todo_list_id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    title = sqlalchemy.Column(sqlalchemy.String)
    colour = sqlalchemy.Column(sqlalchemy.String)
    todo_item = relationship("todo_item")
