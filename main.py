from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (
    QApplication
)

from pages.Welcome import WelcomeScreen
import sys

app = QApplication(sys.argv)
welcome = WelcomeScreen()
widget = QtWidgets.QStackedWidget()
widget.addWidget(welcome)

if __name__ == '__main__':
    widget.show()
    sys.exit(app.exec_())

