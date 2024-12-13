from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QPushButton,
    QDialog,
    QTableWidgetItem,
    QComboBox,
    QLineEdit,
    QLabel,
)

import sqlite3

class Otchet(QDialog):
    def __init__(self, QwidgetOtchet, table):
        super().__init__()
        self.QwidgetOtchet = QwidgetOtchet
        self.Qcombox_seller = QwidgetOtchet.findChild(QComboBox, 'comboBox_seller')
        QWidgetbtn_daysale = self.QwidgetOtchet.findChild(QPushButton, 'pushButton_apply_4')
        self.table_widget = table

        self.Qcombox_seller_text = ''
        self.qtext = ''
        self.month = ''
        self.QCB_Text = ''

        QWidgetbtn_daysale.clicked.connect(self.btn_apply)
        self.Qcombox = QwidgetOtchet.findChild(QComboBox, 'comboBox_month')
        self.QText = QwidgetOtchet.findChild(QLineEdit, 'lineEdit_daysale')
        self.label_sales = QwidgetOtchet.findChild(QLabel, 'label_sales')
        self.Qcombox.activated.connect(self.QCB1)
        self.Qcombox_seller.activated.connect(self.QCB2)
        self.allmonths = {'Январь': '01', 'Февраль': '02', 'Март': '03', 'Апрель': '04', 'Май': '05',
                          'Июнь': '06', 'Июль': '07', 'Август': '08', 'Сентябрь': '09', 'Октябрь': '10',
                          'Ноябрь': '11', 'Декабрь': '12'}
        self.table()

    def QCB1(self, index):
        self.QCB_Text = self.Qcombox.itemText(index)
        if self.QCB_Text != '':
            self.month = self.allmonths[self.QCB_Text]
        self.Qcombox_seller.clear()
        self.Qcombox_seller_text = ''
        self.table()

    def QCB2(self, index):
        self.Qcombox_seller_text = self.Qcombox_seller.itemText(index)
        self.table()

    def btn_apply(self):
        self.Qcombox_seller.clear()
        self.Qcombox_seller_text = ''
        self.qtext = self.QText.text()
        self.table()

    def table(self):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        if self.qtext.strip() == '':
            data = cursor.execute('SELECT * FROM sales')
        else:
            data = cursor.execute('SELECT * FROM sales WHERE date=DATE(?)', (self.qtext, ))
        col_name = [i[0] for i in data.description]
        data_rows = data.fetchall()
        if self.QCB_Text != '':
            new_data = []
            for el in data_rows:
                if el[3][5:7] == self.month:
                    new_data.append(el)
            data_rows = new_data
        sellers = set([i[2] for i in data_rows])
        if len(self.Qcombox_seller) == 0:
            self.Qcombox_seller.addItem('')
            for i in sellers:
                self.Qcombox_seller.addItem(i)
        if self.Qcombox_seller_text != '':
            seller_data = []
            for el in data_rows:
                if el[2] == self.Qcombox_seller_text:
                    seller_data.append(el)
            data_rows = seller_data

        req = 'SELECT price_rub FROM tovar WHERE id=(?)'
        price = []
        for el in data_rows:
            price.append((cursor.execute(req, (el[1],)).fetchone()[0]) * el[4])
        self.label_sales.setText(f'Общая сумма продаж: {sum(price)}')
        self.label_sales.setFont(QFont('Times', 18))

        self.table_widget.setColumnCount(len(col_name))
        self.table_widget.setHorizontalHeaderLabels(col_name)
        self.table_widget.setRowCount(0)
        for i, row in enumerate(data_rows):
            self.table_widget.setRowCount(self.table_widget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.table_widget.setItem(i, j, QTableWidgetItem(str(elem)))
        self.table_widget.resizeColumnsToContents()
        conn.commit()
        conn.close()

class ProizvOtchet(QDialog):
    def __init__(self, QwidgetOtchet, table):
        super().__init__()
        self.QCB_Text = ''
        self.table = table
        self.Qcombox = QwidgetOtchet.findChild(QComboBox, 'comboBox1_3')
        self.Qcombox.activated.connect(self.QCB)

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        req1 = 'SELECT type FROM tovar'
        cursor.execute(req1)
        data_r1 = cursor.fetchall()
        data_r1 = set(data_r1)

        for el in data_r1:
            self.Qcombox.addItem(el[0])
        conn.close()
        self.otchet()

    def QCB(self, index):
        self.QCB_Text = self.Qcombox.itemText(index)
        self.otchet()

    def otchet(self):
        conn1 = sqlite3.connect('database.db')
        cur1 = conn1.cursor()
        if self.QCB_Text != '':
            data = cur1.execute('SELECT product, type, description, price_rub FROM tovar WHERE type=(?)',
                                (self.QCB_Text,))
        else:
            data = cur1.execute('SELECT product, type, description, price_rub FROM tovar')

        col_name = [i[0] for i in data.description]
        data_rows = data.fetchall()
        self.table.setColumnCount(len(col_name))

        self.table.setHorizontalHeaderLabels(col_name)
        self.table.setRowCount(0)
        for i, row in enumerate(data_rows):
            self.table.setRowCount(self.table.rowCount() + 1)
            for j, elem in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(elem)))
        self.table.resizeColumnsToContents()
        conn1.commit()
        conn1.close()