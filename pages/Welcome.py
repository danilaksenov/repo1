from PyQt5.QtWidgets import (
    QDialog,
    QTableWidget,
    QWidget
)

from PyQt5.uic import loadUi
from pages.Konsultant import Consultant
from pages.Manager import Manager
from pages.Director import Director

import sqlite3

class WelcomeScreen(QDialog):
    def __init__(self):
        super().__init__()
        loadUi('dialog2.ui', self)
        self.cb1text = ''
        self.stack = self.stackedWidget
        self.comboBox1.activated.connect(self.cb1)
        self.btnAvtorization.clicked.connect(self.fAvtorization)
        self.pushButton_quit.clicked.connect(self.sign_out)
        self.pushButton_quit.hide()
        self.stackedWidget.currentChanged.connect(self.hiddenButton)

    def cb1(self, index):
        self.label_5.setText('')
        self.cb1text = self.comboBox1.itemText(index)

    def fAvtorization(self):
        password = self.lineEdit1.text()
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        if self.cb1text.strip() == '' or password.strip() == '':
            self.label_5.setText('Заполните все поля')

        else:
            cursor.execute('''SELECT id FROM users WHERE (role, password) = (?, ?)''',
                                        (self.cb1text, password))
            user_input = cursor.fetchone()
            if user_input is None:
                self.label_5.setText('Такого пользователя нет')
            elif user_input[0] == 1:
                self.table_widget = self.findChild(QTableWidget, 'tableWidget_Consultant')
                self.QWidgetCon = self.findChild(QWidget, 'page_Consultant')
                self.stack.setCurrentWidget(self.page_Consultant)
                self.fdfd = Consultant(self.QWidgetCon, self.table_widget)
            elif user_input[0] == 2:
                self.table_widget = self.findChild(QTableWidget, 'tableWidget_otchet')
                self.QWidgetCon = self.findChild(QWidget, 'page_otchetSales')
                self.stack.setCurrentWidget(self.page_otchetSales)
                self.fdfd = Manager(self.QWidgetCon, self.table_widget, self.stack, self)
            elif user_input[0] == 3:
                self.table_widget = self.findChild(QTableWidget, 'tableWidget_proizvOtchet')
                self.QWidgetCon = self.findChild(QWidget, 'page_Director')
                self.stack.setCurrentWidget(self.page_Director)
                self.fdfd = Director(self.QWidgetCon, self.table_widget, self.stack, self)
        conn.commit()
        conn.close()

    def hiddenButton(self):
        if self.stackedWidget.currentWidget() == self.pageAvtorisation:
            self.pushButton_quit.hide()
        else:
            self.pushButton_quit.show()

    def sign_out(self):
        self.stackedWidget.setCurrentWidget(self.pageAvtorisation)
