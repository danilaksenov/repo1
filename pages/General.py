from PyQt5.QtWidgets import (
    QPushButton,
    QDialog,
    QTableWidgetItem,
    QComboBox,
    QLineEdit,
    QCheckBox,
    QLabel,
    QMessageBox
)

import pandas as pd
import sqlite3

class General(QDialog):
    def __init__(self, QwidgetMain, widget):
        super().__init__()
        self.QwidgetCon = QwidgetMain
        self.Qcombox = self.QwidgetCon.findChild(QComboBox, 'SortBox')
        self.Qcombox2 = self.QwidgetCon.findChild(QComboBox, 'MarkBox')
        self.Qcombox3 = self.QwidgetCon.findChild(QComboBox, 'typeBox')
        self.labelerror = self.QwidgetCon.findChild(QLabel, 'label_error')
        self.Qcombox.activated.connect(self.QCB)
        self.Qcombox2.activated.connect(self.QCB2)
        self.Qcombox3.activated.connect(self.QCB3)
        self.Qwidget1 = self.QwidgetCon.findChild(QLineEdit, 'lineEdit_price')
        self.Qwidget2 = self.QwidgetCon.findChild(QCheckBox, 'checkBox_amount')
        self.Qwidget3 = self.QwidgetCon.findChild(QPushButton, 'pushButton_apply')
        self.Qwidget3.clicked.connect(self.btnApply)

        self.check = False
        self.price = 0
        self.QCB_Text, self.QCB2_Text, self.QCB3_Text = '', '', ''
        self.table_widget = widget
        self.mainTable()

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        req1 = 'SELECT brand FROM tovar'
        cursor.execute(req1)
        data_r1 = cursor.fetchall()
        data_r1 = set(data_r1)
        self.Qwidget2.stateChanged.connect(self.checkd)

        for el in data_r1:
            self.Qcombox2.addItem(el[0])
        req2 = 'SELECT type FROM tovar'
        cursor.execute(req2)
        data_r2 = cursor.fetchall()
        data_r2 = set(data_r2)
        for el in data_r2:
            self.Qcombox3.addItem(el[0])
        conn.close()

    def QCB(self, index):
        self.QCB_Text = self.Qcombox.itemText(index)
        self.mainTable()

    def QCB2(self, index):
        self.QCB2_Text = self.Qcombox2.itemText(index)
        self.mainTable()

    def QCB3(self, index):
        self.QCB3_Text = self.Qcombox3.itemText(index)
        self.mainTable()

    def btnApply(self):
        try:
            self.price = int(self.Qwidget1.text())
        except ValueError:
            QMessageBox.critical(self, 'Ошибка', 'Введите число', QMessageBox.Ok)
        self.mainTable()

    def checkd(self):
        if self.Qwidget2.isChecked():
            self.check = True
        else:
            self.check = False
        self.mainTable()

    def mainTable(self):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        if self.QCB_Text == 'Тип/Количество':
            if self.QCB2_Text == '' and self.QCB3_Text == '':
                data = cursor.execute('SELECT * FROM tovar ORDER BY type, in_stock')
            else:
                if self.QCB3_Text == '':
                    data = cursor.execute('SELECT * FROM tovar WHERE brand=(?) ORDER BY type, in_stock',
                                          (self.QCB2_Text,))
                elif self.QCB2_Text == '':
                    data = cursor.execute('SELECT * FROM tovar WHERE type=(?) ORDER BY type, in_stock',
                                          (self.QCB3_Text,))
                else:
                    data = cursor.execute(
                        'SELECT * FROM tovar WHERE brand=(?) AND type=(?) ORDER BY type, in_stock',
                        (self.QCB2_Text, self.QCB3_Text))
        elif self.QCB_Text == 'Тип/Цена':
            if self.QCB2_Text == '' and self.QCB3_Text == '':
                data = cursor.execute('SELECT * FROM tovar ORDER BY type, price_rub')
            else:
                if self.QCB3_Text == '':
                    data = cursor.execute('SELECT * FROM tovar WHERE brand=(?) ORDER BY type, price_rub',
                                          (self.QCB2_Text,))
                elif self.QCB2_Text == '':
                    data = cursor.execute('SELECT * FROM tovar WHERE type=(?) ORDER BY type, price_rub',
                                          (self.QCB3_Text,))
                else:
                    data = cursor.execute('SELECT * FROM tovar WHERE brand=(?) AND type=(?) ORDER BY type,'
                                          ' price_rub', (self.QCB2_Text, self.QCB3_Text))
        else:
            if self.QCB2_Text == '' and self.QCB3_Text == '':
                data = cursor.execute('SELECT * FROM tovar')
            else:
                if self.QCB3_Text == '':
                    data = cursor.execute('SELECT * FROM tovar WHERE brand=(?)', (self.QCB2_Text,))
                elif self.QCB2_Text == '':
                    data = cursor.execute('SELECT * FROM tovar WHERE type=(?)', (self.QCB3_Text,))
                else:
                    data = cursor.execute('SELECT * FROM tovar WHERE brand=(?) AND type=(?)',
                                          (self.QCB2_Text, self.QCB3_Text))

        column = [i[0] for i in data.description]
        data_rows = data.fetchall()
        if self.price > 0 or self.check == True:
            if self.check == True and self.price < 1:
                req = cursor.execute('SELECT * FROM tovar WHERE in_stock < (?)', (5,))
            elif self.price > 0 and self.check == False:
                req = cursor.execute('SELECT * FROM tovar WHERE price_rub < (?)', (self.price,))
            else:
                req = cursor.execute('SELECT * FROM tovar WHERE price_rub < (?) AND in_stock < (?)',
                                     (self.price,5))
            updata = req.fetchall()
            try:
                data_rows = pd.merge(pd.DataFrame(data_rows), pd.DataFrame(updata), left_on=0,
                                     right_on=0, how='inner').values.tolist()
            except KeyError:
                data_rows = []

        self.table_widget.setColumnCount(len(column))
        self.table_widget.setHorizontalHeaderLabels(column)
        self.table_widget.setRowCount(0)
        for i, row in enumerate(data_rows):
            self.table_widget.setRowCount(self.table_widget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.table_widget.setItem(i, j, QTableWidgetItem(str(elem)))
        self.table_widget.resizeColumnsToContents()
        conn.commit()
        conn.close()