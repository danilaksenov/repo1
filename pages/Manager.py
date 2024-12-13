from PyQt5.QtWidgets import (
    QDialog,
    QPushButton,
    QTableWidget,
    QWidget
)
from otchet import Otchet
from pages.General import General

class Manager(QDialog):
    def __init__(self, QwidgetO, widget, stack, welc):
        super().__init__()
        self.QwidgetO = QwidgetO
        self.widget = widget
        self.stack = stack
        self.welc = welc
        widget1 = self.QwidgetO.findChild(QPushButton, 'pushButton_otchetsales')
        widget2 = self.QwidgetO.findChild(QPushButton, 'pushButton_tovar')
        widget1.clicked.connect(self.btn_otchetsales)
        widget2.clicked.connect(self.pushButton_tovar)

    def btn_otchetsales(self):
        self.QWidgetCon2 = self.welc.findChild(QWidget, 'page_Otchet')
        self.welc.stack.setCurrentWidget(self.welc.page_Otchet)
        self.ghgh = Otchet(self.QWidgetCon2, self.widget)

    def pushButton_tovar(self):
        self.table_widget = self.welc.findChild(QTableWidget, 'tableWidget_Consultant')
        self.QWidgetCon3 = self.welc.findChild(QWidget, 'page_Consultant')
        self.welc.stack.setCurrentWidget(self.welc.page_Consultant)
        self.ghghg = General(self.QWidgetCon3, self.table_widget)