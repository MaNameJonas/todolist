# import PyQt5 as qt
from PyQt5.QtWidgets import QApplication, QLabel

window = QApplication([])

label = QLabel('Hello World!')
label.show()
label.size()

window.exec()