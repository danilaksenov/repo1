from PyQt5.QtWidgets import (
    QDialog,
    QPushButton,
    QTableWidget,
    QWidget,
    QComboBox,
    QLineEdit,
    QMessageBox
)

from datetime import datetime
from otchet import Otchet, ProizvOtchet
from pages.General import General
import sqlite3

class Director(QDialog):
    def __init__(self, QwidgetO, widget, stack, welc):
        super().__init__()
        self.text = ''
        self.QwidgetO = QwidgetO
        self.widget = widget
        self.stack = stack
        self.welc = welc

        widget1 = self.QwidgetO.findChild(QPushButton, 'pushButton_otchetsales_2')
        widget2 = self.QwidgetO.findChild(QPushButton, 'pushButton_tovar_2')
        widget3 = self.QwidgetO.findChild(QPushButton, 'pushButton_sales_del')
        widget4 = self.QwidgetO.findChild(QPushButton, 'pushButton_proizvOtchet')
        widget5 = self.QwidgetO.findChild(QPushButton, 'pushButton_apply_3')
        self.widgetcombobox = self.QwidgetO.findChild(QComboBox, 'comboBox_change')
        self.lineedit = self.QwidgetO.findChild(QLineEdit, 'lineEdit_change')
        widget1.clicked.connect(self.btn_otchetsales)
        widget2.clicked.connect(self.pushButton_tovar)
        widget3.clicked.connect(self.pushButton_sales_del)
        widget4.clicked.connect(self.proizvOtchet)
        widget5.clicked.connect(self.pushButton_apply_3)
        self.widgetcombobox.activated.connect(self.QCB)

    def btn_otchetsales(self):
        self.table_widget = self.welc.findChild(QTableWidget, 'tableWidget_otchet')
        self.QWidgetCon2 = self.welc.findChild(QWidget, 'page_Otchet')
        self.welc.stack.setCurrentWidget(self.welc.page_Otchet)
        self.ghgh = Otchet(self.QWidgetCon2, self.table_widget)

    def pushButton_tovar(self):
        self.table_widget = self.welc.findChild(QTableWidget, 'tableWidget_Consultant')
        self.QWidgetCon3 = self.welc.findChild(QWidget, 'page_Consultant')
        self.welc.stack.setCurrentWidget(self.welc.page_Consultant)
        self.ghghg = General(self.QWidgetCon3, self.table_widget)

    def pushButton_sales_del(self):
        con = sqlite3.connect('database.db')
        cursor = con.cursor()
        currentyear = datetime.now().year
        pastyear = str(currentyear - 1)
        cursor.execute('SELECT * FROM sales')
        f = cursor.fetchall()
        for el in f:
            if el[3][:4] == pastyear:
                cursor.execute('DELETE FROM sales WHERE date=(?)', (el[3],))
        con.commit()
        con.close()

    def proizvOtchet(self):
        self.QWidgetCon3 = self.welc.findChild(QWidget, 'page_Proizvotchet')
        self.welc.stack.setCurrentWidget(self.welc.page_Proizvotchet)
        self.ghghg = ProizvOtchet(self.QWidgetCon3, self.widget)

    def QCB(self, index):
        self.text = self.widgetcombobox.itemText(index)

    def pushButton_apply_3(self):
        try:
            linetext = int(self.lineedit.text())
        except ValueError:
            linetext = 0
            QMessageBox.critical(self, 'Ошибка', 'Введите число', QMessageBox.Ok)
        if self.text != '':
            con = sqlite3.connect('database.db')
            cursor = con.cursor()
            if self.text == 'Уменьшить цену':
                cursor.execute('UPDATE tovar SET price_rub = price_rub - (?)', (linetext,))
                cursor.execute('UPDATE tovar SET ye = ye - (?)', (linetext,))
            elif self.text == 'Увеличить цену':
                cursor.execute('UPDATE tovar SET price_rub = price_rub + (?)', (linetext,))
                cursor.execute('UPDATE tovar SET ye = ye + (?)', (linetext,))
            con.commit()
            con.close()