# import PyQt5 as qt
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
from todolist.todo_list import Todolist
from todolist.datamodel import todo_list

todolist_1 = Todolist()


class Window(QWidget):
    def __init__(self):
        super().__init__()
        vBox = QVBoxLayout()
        vBox.setContentsMargins(50, 50, 50, 50)
        vBox.setAlignment(Qt.AlignTop)
        self.setWindowTitle("Todo List")
        width = 650
        height = 800
        self.setGeometry(0, 0, width, height)
        self.label_1 = QLabel("All To Do Lists", self)
        self.label_1.setFixedHeight(30)
        # self.setCentralWidget(self.label_1)
        self.label_1.setStyleSheet("color: white; background-color: #292b2f; text-align: center;")
        # self.label_1.resize(200, 50)
        self.label_1.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        vBox.addWidget(self.label_1)
        all_todolists = todolist_1.get_todolists()
        for i in range(len(all_todolists)):
            button = Button(all_todolists[i].title)
            vBox.addWidget(button)

        self.setStyleSheet("background-color: #36393e")
        self.setLayout(vBox)
        #self.label_1.setStyleSheet("")
        self.show()


class Button(QPushButton):
    def __init__(self, text, *args, **kwargs):
        self.text = text
        super(Button, self).__init__(*args, **kwargs)
        super().clicked.connect(self.action)
        self.setText(self.text)

    def action(self):
        self.window = TaskWindow(self.text)
        self.window.show()


class TaskWindow(QWidget):
    def __init__(self, text):
        super().__init__()
        vBox = QVBoxLayout()
        vBox.setContentsMargins(50, 50, 50, 50)
        vBox.setAlignment(Qt.AlignTop)
        self.text = text
        self.setWindowTitle(text)
        width = 400
        height = 400
        self.setGeometry(0, 0, width, height)
        self.label_1 = QLabel(text, self)
        self.label_1.setFixedHeight(30)
        vBox.addWidget(self.label_1)
        self.setLayout(vBox)
        table_id = todolist_1.get_todolist_id("title", "Einkaufsliste")
        all_todo_items = todolist_1.get_todo_items("todo_list_id", table_id[0].todo_list_id)
        for i in range(len(all_todo_items)):
            print(i)
            label = TaskLabel(all_todo_items[i].title)
            vBox.addWidget(label)


class TaskLabel(QCheckBox):
    def __init__(self, text):
        self.text = text
        super(TaskLabel, self).__init__()
        self.setText(self.text)
        super().stateChanged.connect(self.action)

    def action(self):
        print("test")


App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec())
