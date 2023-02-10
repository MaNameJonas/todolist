"""Main File"""

import sqlalchemy as sql
import sqlalchemy.orm
from todolist.datamodel import Base, todo_list, todo_item


class Todolist():

    def __init__(self) -> None:
        db_connection = sqlalchemy.create_engine("sqlite:///todolist_database.db")
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
            new_todo_item = todo_item(title=_title,
                                      description=_description,
                                      todo_list_id=session
                                                   .query(todo_list)
                                                   .filter(todo_list.title == _list)
                                                   .first()
                                                   .todo_list_id,
                                      iscomplete=False)
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
        columns = [getattr(table, col) for col in args]
        result = session.query(*columns).filter(getattr(table, column) == value).all()
        return result

    def rowcount(self, table):
        session = self.session_factory()
        rows = session.query(table).count()
        return rows

    def get_todolists(self):
        session = self.session_factory()
        return session.query(todo_list).all()

    def get_todo_items(self, column, value):
        session = self.session_factory()
        return session.query(todo_item).filter(getattr(todo_item, column) == value).all()

    def get_todolist_id(self, column, value):
        session = self.session_factory()
        return session.query(todo_list).filter(getattr(todo_list, column) == value).all()

    def check_todo_item(self, column, value):
        session = self.session_factory()
        tmp = session.query(todo_item).filter(getattr(todo_item, column) == value).all()
        if tmp[0].iscomplete is False:
            self.update(todo_item, column, value, True, "iscomplete")

    def uncheck_todo_item(self, column, value):
        session = self.session_factory()
        tmp = session.query(todo_item).filter(getattr(todo_item, column) == value).all()
        if tmp[0].iscomplete is True:
            self.update(todo_item, column, value, True, "iscomplete")

    def change_checked_status(self, column, value):
        session = self.session_factory()
        tmp = session.query(todo_item).filter(getattr(todo_item, column) == value).all()
        if tmp[0].iscomplete is True:
            self.update(todo_item, column, value, False, "iscomplete")
            print(tmp[0].iscomplete)
        elif tmp[0].iscomplete is False:
            self.update(todo_item, column, value, True, "iscomplete")
            print(tmp[0].iscomplete)

if __name__ == "__main__":
    Kaufeinliste = Todolist()
    # Kaufeinliste.create_todo_list("Morgenroutine", "blau")
    # Kaufeinliste.create_todo_list("Hausputz", "grün")
    # Kaufeinliste.create_todo_item("Klo putzen", "Putzmittel kaufen!", "Hausputz")
    # Kaufeinliste.create_todo_item("Zähne putzen", "Mit Zahnpasta", "Morgenroutine")
    # Kaufeinliste.create_todo_item("Duschen", "Mit Wasser", "Morgenroutine")
    # Kaufeinliste.create_todo_item("Frühstücken", "Toast, Kaffe, Apfel", "Morgenroutine")
    # Kaufeinliste.delete(todo_item, "todo_id", 1)
    # Kaufeinliste.update(todo_item, "todo_id", 2, "Brot einkaufen", "description")
    # print(Kaufeinliste.select(todo_list, "title", "Morgenroutine", "todo_list_id"))
    # print(Kaufeinliste.get_todolist_id("title", "Einkaufsliste"))
    # print(Kaufeinliste.get_todo_items("todo_list_id", 3)[0].title)
    # print(Kaufeinliste.get_todolist_id())
    Kaufeinliste.change_checked_status("todo_list_id", 3)
    # print(Kaufeinliste.get_todolists())
