"""Main File"""

import sqlalchemy as sql
import sqlalchemy.orm
from datamodel import Base, todo_list, todo_item

class Todolist():
    
    def __init__(self) -> None:
        db_connection = sqlalchemy.create_engine("sqlite:///C:\\SEW_practice\\todolist\\todolist\\todolist_database.db")
        Base.metadata.create_all(db_connection)
        self.session_factory = sqlalchemy.orm.sessionmaker()
        self.session_factory.configure(bind=db_connection)
    
    def create_todo_list(self, _title, _colour):
        with self.session_factory() as session:
            new_todo_list = todo_list(title =_title,
                                        colour =_colour)
            session.add(new_todo_list)
            session.commit()

    # def querytest(self, _list):
    #     session1 = self.session_factory()
    #     print(session1
    #           .query(todo_list)
    #           .filter(todo_list.title == _list)
    #           .first()
    #           .todo_list_id)

    def create_todo_item(self, _title, _description, _list):
        with self.session_factory() as session:
            new_todo_item = todo_item(title =_title,
                                      description = _description,
                                      todo_list_id = session
                                                     .query(todo_list)
                                                     .filter(todo_list.title == _list)
                                                     .first()
                                                     .todo_list_id,
                                      iscomplete = False)
            session.add(new_todo_item)
            session.commit()
    
    def delete(self, table, column, value):
        """Deletes any entry by giving the table to delete in, column and value to identify the entry to delete it."""
        session = self.session_factory()
        session.query(table).filter(getattr(table, column) == value).delete(synchronize_session='fetch')
        session.commit()

    def update(self, table, column, value, change_value, change_column):
        """Updates any entry by giving the table to update in, column and value to identify the entry, 
        the updated value and the column to update in."""

        session = self.session_factory()
        update = sql.update(table).where(getattr(table, column) == value).values({change_column: change_value})
        session.execute(update)
        session.commit()

    def select(self, table, column, value, *args):
        session = self.session_factory()
        columns = [getattr(table,col) for col in args]
        result = session.query(*columns).filter(getattr(table, column) == value).all()
        return result
    

if __name__ == "__main__":
    Kaufeinliste = Todolist()
    #Kaufeinliste.create_todo_list("Einkaufsliste", "rot") 
    #Kaufeinliste.create_todo_item("Brot", "Brot einkaufen", "Einkaufsliste")
    #Kaufeinliste.delete(todo_item, "todo_id", 1)
    #Kaufeinliste.update(todo_item, "todo_id", 2, "Brot einkaufen", "description")
    print(Kaufeinliste.select(todo_item, "todo_id", 2, "description", "title"))
