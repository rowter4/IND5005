from PyQt5 import QtWidgets
import os
import datetime

import manipulation as mp
from PyQt5.QtCore import QRect, Qt
from PyQt5.QtWidgets import QTabWidget, QFileDialog
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QListWidget
from PyQt5.QtWidgets import QStackedWidget
from PyQt5.QtWidgets import (QWidget, QPushButton, QMainWindow,
                             QHBoxLayout, QAction)

import sqlite3
import re
import pandas as pd

try:
    conn = sqlite3.connect('stock.db')
    c = conn.cursor()
    c.execute("""CREATE TABLE stock (
                name text,
                quantity integer,
                cost integer
                ) """)
    conn.commit()
except Exception:
    print('DB exists')


class Login(QtWidgets.QDialog):
    def __init__(self, parent=None):
        print('Start App')
        super(Login, self).__init__(parent)
        print('Get Username and Password')
        self.textName = QtWidgets.QLineEdit(self)
        self.textPass = QtWidgets.QLineEdit(self)
        self.buttonLogin = QtWidgets.QPushButton('Admin Login', self)
        # self.buttonLogin.clicked.connect(self.handleLogin)
        self.buttonLogin.clicked.connect(self.login_check)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.textName)
        layout.addWidget(self.textPass)
        layout.addWidget(self.buttonLogin)

    def login_check(self):
        uname = self.textName.text()
        passw = self.textPass.text()
        connection = sqlite3.connect("user.db")
        result = connection.execute("SELECT * FROM user WHERE USERNAME = ? AND PASSWORD = ?", (uname, passw))
        if result.fetchall():
            self.accept()
        else:
            print("invalid login")
            QtWidgets.QMessageBox.warning(
                self, 'Error', 'Bad user or password')

    # def handleLogin(self):
    #     if (self.textName.text() == 'Admin' and
    #         self.textPass.text() == '1234'):
    #         self.accept()
    #     else:
    #         QtWidgets.QMessageBox.warning(
    #             self, 'Error', 'Bad user or password')

class Example(QMainWindow):


    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.st = stackedExample()
        exitAct = QAction(QIcon('exit_icon.png'), 'Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(self.close)

        self.statusBar()

        toolbar = self.addToolBar('Exit')
        toolbar.addAction(exitAct)

        self.setCentralWidget(self.st)

        self.show()

class stackedExample(QWidget):
    def __init__(self):

        super(stackedExample, self).__init__()
        self.leftlist = QListWidget()
        self.leftlist.setFixedWidth(250)
        self.leftlist.insertItem(0, 'Add Stock')
        self.leftlist.insertItem(1, 'Manage Stock')
        self.leftlist.insertItem(2, 'View Stock')
        self.leftlist.insertItem(3, 'View Transaction History')

        self.stack1 = QWidget()
        self.stack2 = QWidget()
        self.stack3 = QWidget()
        self.stack4 = QWidget()

        self.stack1UI()
        self.stack2UI()
        self.stack3UI()
        self.stack4UI()

        self.Stack = QStackedWidget(self)
        self.Stack.addWidget(self.stack1)
        self.Stack.addWidget(self.stack2)
        self.Stack.addWidget(self.stack3)
        self.Stack.addWidget(self.stack4)

        hbox = QHBoxLayout(self)
        hbox.addWidget(self.leftlist)
        hbox.addWidget(self.Stack)

        self.setLayout(hbox)
        self.leftlist.currentRowChanged.connect(self.display)
        self.setGeometry(500,350, 200, 200)
        self.setWindowTitle('Stock Management')
        self.show()


    def stack1UI(self):
        layout = QFormLayout()

        self.ok = QPushButton('Add Stock', self)
        cancel = QPushButton('Cancel', self)

        self.supplier_name = QLineEdit()
        layout.addRow("Supplier Name", self.supplier_name)

        self.item_name = QLineEdit()
        layout.addRow("Item Name", self.item_name)

        self.item_no = QLineEdit()
        layout.addRow("Item No.", self.item_no)

        self.serial_no = QLineEdit()
        layout.addRow("Serial Number", self.serial_no)

        self.description = QLineEdit()
        layout.addRow("Description", self.description)

        self.unit = QLineEdit()
        layout.addRow("Unit", self.unit)

        self.reorder_lvl = QLineEdit()
        layout.addRow("Reorder Level", self.reorder_lvl)

        self.reorder_days = QLineEdit()
        layout.addRow("Days Per Reorder", self.reorder_days)

        self.reorder_qty = QLineEdit()
        layout.addRow("Reorder Quantity", self.reorder_qty)

        layout.addWidget(self.ok)
        layout.addWidget(cancel)

        self.ok.clicked.connect(self.on_click)

        field_array_stack1UI = [self.supplier_name, self.item_name, self.item_no, self.serial_no, self.description, self.unit, self.reorder_lvl, self.reorder_days,
                              self.reorder_qty]
        for x in field_array_stack1UI:
            cancel.clicked.connect(x.clear)

        self.stack1.setLayout(layout)

    def on_click(self):
        now = datetime.datetime.now()
        item_name_inp = self.item_name.text().replace(' ','_').lower()
        description_inp = self.description.text().lower()
        stock_count_inp = int(self.reorder_days.text())
        stock_cost_inp = int(self.reorder_qty.text())
        #print(item_name_inp,stock_count_inp,stock_cost_inp)
        stock_add_date_time = now.strftime("%Y-%m-%d %H:%M")
        d = mp.insert_prod(item_name_inp,description_inp, stock_count_inp,stock_cost_inp,stock_add_date_time)
        print(d)
        #Need to add the above details to table

    def stack2UI(self):

        layout = QHBoxLayout()
        layout.setGeometry(QRect(0,300,1150,500))
        tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tab4 = QWidget()

        tabs.addTab(self.tab1, 'Add Quantity')
        tabs.addTab(self.tab2, 'Reduce Quantity')
        tabs.addTab(self.tab3, 'Delete Stock')
        tabs.addTab(self.tab4, 'Bulk Upload')

        self.tab1UI()
        self.tab2UI()
        self.tab3UI()
        self.tab4UI()

        layout.addWidget(tabs)
        self.stack2.setLayout(layout)

    def tab1UI(self):
        layout = QFormLayout()
        # Buttons to press once fields have been entered
        ## Requires confirmation once add stock button is pressed

        self.ok_add = QPushButton('Add Item', self)
        cancel = QPushButton('Cancel', self)

        ## To change to choose from added stock inventory list

        self.item_no_add = QLineEdit()
        layout.addRow("Item No.", self.item_no_add)

        self.stock_count_add = QLineEdit()
        layout.addRow("Quantity to Add", self.stock_count_add)

        self.cost_per_item = QLineEdit()
        layout.addRow("Cost Per Item", self.cost_per_item)

        self.location = QLineEdit()
        layout.addRow("Location of Item", self.location)

        ## To change to select date from calendar
        self.expiry_date = QLineEdit()
        layout.addRow("Expiry Date", self.expiry_date)

        layout.addWidget(self.ok_add)
        layout.addWidget(cancel)
        self.tab1.setLayout(layout)

        self.ok_add.clicked.connect(self.call_add)       #need to write function to add quantity
        field_array_tab1UI = [self.item_no_add, self.stock_count_add, self.cost_per_item, self.location, self.expiry_date]
        for x in field_array_tab1UI:
            cancel.clicked.connect(x.clear)

    def tab2UI(self):
        layout = QFormLayout()
        self.ok_red = QPushButton('Reduce Stock', self)
        cancel = QPushButton('Cancel', self)

        self.item_no_red = QLineEdit()
        layout.addRow("Item No.", self.item_no_red)

        self.location_red = QLineEdit()
        layout.addRow("Location", self.location_red)

        self.stock_count_red = QLineEdit()
        layout.addRow("Quantity to Reduce", self.stock_count_red)


        layout.addWidget(self.ok_red)
        layout.addWidget(cancel)
        self.tab2.setLayout(layout)

        self.ok_red.clicked.connect(self.call_red)  # need to write function to reduce quantity
        field_array_tab2UI = [self.item_no_red, self.location_red, self.stock_count_red]
        for x in field_array_tab2UI:
            cancel.clicked.connect(x.clear)

    def tab3UI(self):
        layout = QFormLayout()
        self.ok_del = QPushButton('Delete Stock', self)
        cancel = QPushButton('Cancel', self)

        self.item_name_del = QLineEdit()
        layout.addRow("Stock Name", self.item_name_del)
        layout.addWidget(self.ok_del)
        layout.addWidget(cancel)
        self.tab3.setLayout(layout)

        self.ok_del.clicked.connect(self.call_del)  # need to write function to delete stock
        cancel.clicked.connect(self.item_name_del.clear)


    def call_del(self):
        now = datetime.datetime.now()
        stock_del_date_time = now.strftime("%Y-%m-%d %H:%M")
        item_name = self.item_name_del.text().replace(' ','_').lower()
        mp.remove_stock(item_name,stock_del_date_time)

    def call_red(self):
        now = datetime.datetime.now()
        stock_red_date_time = now.strftime("%Y-%m-%d %H:%M")
        item_name = self.item_name_red.text().replace(' ','_').lower()
        try:
            stock_val = -(int(self.stock_count_red.text()))
            print(stock_val)
            print(type(stock_val))
            mp.update_quantity(item_name, stock_val, stock_red_date_time)
        except Exception:
            print('Exception')

    def tab4UI(self):
        layout = QVBoxLayout()
        self.choose_file = QPushButton()
        self.choose_file.setText("Choose File")
        self.choose_file.setMinimumWidth(50)
        self.choose_file.setMaximumWidth(100)

        self.confirm_submit = QPushButton()
        self.confirm_submit.setText("Confirm")
        self.confirm_submit.setMinimumWidth(50)
        self.confirm_submit.setMaximumWidth(100)

        headers = ['Invoice No.', 'Item No.', 'Location', 'Supplier', 'Item Name', 'Quantity', 'Inventory Value']

        self.upload_table = QTableWidget()
        self.upload_table.setColumnCount(7)
        self.upload_table.setHorizontalHeaderLabels(headers)
        self.upload_table.setColumnWidth(0, 100)
        self.upload_table.setColumnWidth(1, 100)
        self.upload_table.setColumnWidth(2, 100)
        self.upload_table.setColumnWidth(3, 100)
        self.upload_table.setColumnWidth(4, 100)
        self.upload_table.setColumnWidth(5, 100)
        self.upload_table.setColumnWidth(6, 100)
        # self.upload_table.insertRow(0)
        # self.upload_table.setItem(0, 0, QTableWidgetItem('Transaction ID'))
        # self.upload_table.setItem(0, 1, QTableWidgetItem('Stock Name'))
        # self.upload_table.setItem(0, 2, QTableWidgetItem('Transaction Type'))
        # self.upload_table.setItem(0, 3, QTableWidgetItem('Date'))
        # self.upload_table.setItem(0, 4, QTableWidgetItem('Time'))
        # self.upload_table.setItem(0, 5, QTableWidgetItem('Transaction Specific'))
        self.upload_table.setRowHeight(0, 20)

        layout.addWidget(self.choose_file)
        layout.addWidget(self.upload_table)
        self.choose_file.clicked.connect(self.open_file_dialogue)
        layout.addWidget(self.confirm_submit)
        layout.setAlignment(self.confirm_submit, Qt.AlignRight)
        self.tab4.setLayout(layout)

    def updateTable(self, data):
        # Clear existing table content

        self.upload_table.setRowCount(data.shape[0])

        for row_num, row_data in data.iterrows():
            for col_num, cell_data in enumerate(row_data):
                self.upload_table.setItem(row_num, col_num, QTableWidgetItem(cell_data))

    def open_file_dialogue(self):
        filenames, _ = QFileDialog.getOpenFileNames(
            None,
            "QFileDialog.getOpenFileNames()",
            "",
            # "All Files (*);;Python Files (*.py);;Text Files (*.txt)",
            "All Files (*);;Excel Files (*.xlsx);;Text Files (*.csv);;PDF Files (*.pdf)",
        )


        df = pd.DataFrame()
        invalid_files = []
        pdf_files = []
        headers = ['Invoice No.', 'Item No.', 'Location', 'Supplier', 'Item Name', 'Quantity', 'Inventory Value']
        data = pd.DataFrame(columns=headers)

        if filenames:
            for filename in filenames:
                fileextension = re.search(".*\.([^\.]+)$", filename).group(1)
                print(f'{fileextension}: {filename}')
                if fileextension == 'pdf':

                    pdf_files.append(filename)
                elif fileextension == 'csv':
                    read_csv_data = pd.read_csv(filename)
                    data = pd.concat([data, read_csv_data])
                elif fileextension in ['xlsx', 'xls']:
                    read_xls_data = pd.read_excel(filename)
                    data = pd.concat([data, read_xls_data])
                else:
                    invalid_files.append(filename)

            invalid_files_message = "\n".join(invalid_files)
            font = QFont()
            font.setFamily("Calibri")
            font.setPointSize(10)

        if invalid_files_message:
            error_message_box = QtWidgets.QMessageBox()
            error_message_box.setFont(font)
            error_message_box.warning(
                self, 'Error', f'The following files have invalid file type \n {invalid_files_message}')

        data = data.fillna('')
        data = data.astype(str)
        self.updateTable(data)


    def extract_pdf(self):
        print('extract pdf')

    def call_add(self):
        now = datetime.datetime.now()
        stock_call_add_date_time = now.strftime("%Y-%m-%d %H:%M")
        item_name = self.item_name_add.text().replace(' ','_').lower()
        stock_val = int(self.stock_count_add.text())
        mp.update_quantity(item_name, stock_val, stock_call_add_date_time)


    def stack3UI(self):

        table = mp.show_stock()
        print('show')
        print(table)
        layout = QVBoxLayout()
        self.srb = QPushButton()
        self.srb.setText("Get Search Result.")
        self.View = QTableWidget()
        self.lbl3 = QLabel()
        self.lbl_conf_text = QLabel()
        self.lbl_conf_text.setText("Enter the search keyword:")
        self.conf_text = QLineEdit()

        self.View.setColumnCount(3)
        self.View.setColumnWidth(0, 250)
        self.View.setColumnWidth(1, 250)
        self.View.setColumnWidth(2, 200)
        self.View.insertRow(0)
        self.View.setItem(0, 0, QTableWidgetItem('Stock Name'))
        self.View.setItem(0, 1, QTableWidgetItem('Quantity'))
        self.View.setItem(0, 2, QTableWidgetItem('Cost(Per Unit)'))



        layout.addWidget(self.View)
        layout.addWidget(self.lbl_conf_text)
        layout.addWidget(self.conf_text)
        layout.addWidget(self.srb)
        layout.addWidget(self.lbl3)
        self.srb.clicked.connect(self.show_search)
        self.stack3.setLayout(layout)

    def show_search(self):
        if self.View.rowCount()>1:
            for i in range(1,self.View.rowCount()):
                self.View.removeRow(1)


        x_act = mp.show_stock()
        x = []
        if self.conf_text.text() != '':
            for i in range(0,len(x_act)):
                a = list(x_act[i])
                if self.conf_text.text().lower() in a[0].lower():
                    x.append(a)
        else:
            x = mp.show_stock()

        if len(x)!=0:
            for i in range(1,len(x)+1):
                self.View.insertRow(i)
                a = list(x[i-1])
                self.View.setItem(i, 0, QTableWidgetItem(a[0].replace('_',' ').upper()))
                self.View.setItem(i, 1, QTableWidgetItem(str(a[1])))
                self.View.setItem(i, 2, QTableWidgetItem(str(a[2])))
                self.View.setRowHeight(i, 50)
            self.lbl3.setText('Viewing Stock Database.')
        else:
            self.lbl3.setText('No valid information in database.')

    def stack4UI(self):
        layout = QVBoxLayout()
        self.srt = QPushButton()
        self.srt.setText("Get Transaction History.")
        self.Trans = QTableWidget()
        self.lbl4 = QLabel()
        self.lbl_trans_text = QLabel()
        self.lbl_trans_text.setText("Enter the search keyword:")
        self.trans_text = QLineEdit()

        self.Trans.setColumnCount(6)
        self.Trans.setHorizontalHeaderLabels(
            ['Transaction ID', 'Stock Name', 'Transaction Type', 'Date', 'Time', 'Transaction Specific'])
        self.Trans.setColumnWidth(0, 150)
        self.Trans.setColumnWidth(1, 150)
        self.Trans.setColumnWidth(2, 150)
        self.Trans.setColumnWidth(3, 100)
        self.Trans.setColumnWidth(4, 100)
        self.Trans.setColumnWidth(5, 500)
        # self.Trans.insertRow(0)
        # self.Trans.setItem(0, 0, QTableWidgetItem('Transaction ID'))
        # self.Trans.setItem(0, 1, QTableWidgetItem('Stock Name'))
        # self.Trans.setItem(0, 2, QTableWidgetItem('Transaction Type'))
        # self.Trans.setItem(0, 3, QTableWidgetItem('Date'))
        # self.Trans.setItem(0, 4, QTableWidgetItem('Time'))
        # self.Trans.setItem(0, 5, QTableWidgetItem('Transaction Specific'))
        self.Trans.setRowHeight(0, 20)

        layout.addWidget(self.Trans)
        layout.addWidget(self.lbl_trans_text)
        layout.addWidget(self.trans_text)
        layout.addWidget(self.srt)
        layout.addWidget(self.lbl4)
        self.srt.clicked.connect(self.show_trans_history)
        self.stack4.setLayout(layout)

    def show_trans_history(self):
        if self.Trans.rowCount()>1:
            for i in range(1,self.Trans.rowCount()):
                self.Trans.removeRow(1)

        path = os.path.join(os.path.dirname(os.path.realpath(__file__)),'transaction.txt')
        if os.path.exists(path):
            tsearch = open(path, 'r')
            x_c = tsearch.readlines()
            tsearch.close()
            x = []
            if self.trans_text.text() != '':
                key = self.trans_text.text()
                for i in range(0,len(x_c)):
                    a = x_c[i].split(" ")
                    name = a[0]
                    action = a[-2]
                    if (key.lower() in name.lower()) or (key.lower() in action.lower()) :
                        x.append(a)
            else:
                x = x_c.copy()

            for i in range(0,len(x)):
                x.sort(key=lambda a: a[4])
            #print(x)
            tid = 1900001
            for i in range(1,len(x)+1):
                self.Trans.insertRow(i)

                a = x[i-1].split(" ")
                if a[-2] == 'UPDATE':
                    p = 'Quantity of Stock Changed from '+a[1]+' to '+a[2]
                elif a[-2] == 'INSERT':
                    p = 'Stock added with Quantity : '+a[1]+' and Cost(Per Unit in Rs.) : '+a[2]
                elif a[-2] == 'REMOVE':
                    p = 'Stock information deleted.'
                else:
                    p = 'None'


                self.Trans.setItem(i, 0, QTableWidgetItem(str(tid)))
                self.Trans.setItem(i, 1, QTableWidgetItem(a[0].replace('_',' ')))
                self.Trans.setItem(i, 2, QTableWidgetItem(a[-2]))
                self.Trans.setItem(i, 3, QTableWidgetItem(a[3]))
                self.Trans.setItem(i, 4, QTableWidgetItem(a[4]))
                self.Trans.setItem(i, 5, QTableWidgetItem(p))
                self.Trans.setRowHeight(i, 50)
                tid += 1

            self.lbl4.setText('Transaction History.')
        else:
            self.lbl4.setText('No valid information found.')



    def display(self, i):
        self.Stack.setCurrentIndex(i)




if __name__ == '__main__':

    import sys
    app = QtWidgets.QApplication(sys.argv)
    login = Login()

    if login.exec_() == QtWidgets.QDialog.Accepted:
        window = Example()
        sys.exit(app.exec_())
