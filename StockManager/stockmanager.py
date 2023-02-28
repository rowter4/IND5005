from PyQt5 import QtWidgets
import os
import datetime
import check_input

import manipulation as mp
from PyQt5.QtCore import QRect, Qt, QDate
from PyQt5.QtWidgets import QTabWidget, QFileDialog
from PyQt5.QtWidgets import QTableWidget
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QListWidget
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QDateEdit
from PyQt5.QtWidgets import QCalendarWidget
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

    def showDate(self):
        # Update the label with the selected date
        date = self.calendar.selectedDate().toString()
        self.selected_date = date

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

        self.ok = QPushButton('Ok', self)

        cancel = QPushButton('Cancel', self)

        self.supplier_name = QLineEdit()
        layout.addRow("Supplier Name", self.supplier_name)

        self.item_name = QLineEdit()
        layout.addRow("Item Name", self.item_name)

        self.item_no = QLineEdit()
        layout.addRow("Item No.", self.item_no)

        self.serial_no = QLineEdit()
        layout.addRow("Serial No.", self.serial_no)

        self.description = QLineEdit()
        layout.addRow("Description", self.description)

        self.unit = QLineEdit()
        layout.addRow("Unit of Measurement", self.unit)

        self.reorder_lvl = QLineEdit()
        layout.addRow("Reorder Level", self.reorder_lvl)

        self.reorder_days = QLineEdit()
        layout.addRow("Days Per Reorder", self.reorder_days)

        self.reorder_qty = QLineEdit()
        layout.addRow("Reorder Quantity", self.reorder_qty)

        layout.addWidget(self.ok)
        layout.addWidget(cancel)

        # Confirmation function called when ok is clicked
        self.ok.clicked.connect(self.confirmation_add_inv)

        # Clear all fields when cancel is clicked
        self.field_dict_stack1UI = {"Supplier Name": self.supplier_name,
                                    "Item Name": self.item_name,
                                    "Item No.": self.item_no,
                                    "Serial No.": self.serial_no,
                                    "Description": self.description,
                                    "Unit of Measurement": self.unit,
                                    "Reorder Level": self.reorder_lvl,
                                    "Days Per Reorder": self.reorder_days,
                                    "Reorder Quantity": self.reorder_qty}
        # self.field_array_stack1UI = [self.supplier_name, self.item_name, self.item_no, self.serial_no, self.description, self.unit, self.reorder_lvl, self.reorder_days,
        #                       self.reorder_qty]
        for key, value in self.field_dict_stack1UI.items():
            cancel.clicked.connect(value.clear)

        self.stack1.setLayout(layout)

    def confirmation_add_inv(self):
        # Check for empty fields
        empty_fields_array = []
        incorrect_dtype_array = []
        for key, value in self.field_dict_stack1UI.items():
            if check_input.check_empty_field(value.text()) == 'blank':
                empty_fields_array.append(key)
            # if check_input.check_dtype(value.text()) == 'error':
            #     incorrect_dtype_array.append(key)

        if empty_fields_array:
            # there are empty fields
            empty_fields_message = "\n".join(empty_fields_array)
            error_message_box = QtWidgets.QMessageBox()
            error_message_box.warning(
                self, 'Error', f'Unable to add item to inventory. \nPlease ensure that the following fields have been filled.\n\n{empty_fields_message}')
            return 'Error'


        # Follow this variable names (inp: input)
        now = datetime.datetime.now()
        supplier_name_inp = self.supplier_name.text().replace(' ', '_').upper()
        item_name_inp = self.item_name.text().replace(' ', '_').upper()
        item_no_inp = self.item_no.text().upper()
        description_inp = self.description.text().upper()
        unit_inp = self.unit.text()
        reorder_lvl_inp = self.reorder_lvl.text()
        reorder_days_inp = self.reorder_days.text()
        reorder_qty_inp = self.reorder_qty.text()
        stock_add_date_time = now.strftime("%Y-%m-%d %H:%M")


        confirmation_box = QMessageBox.question(self, 'Confirmation',
                                            f"Please Confirm the Following Details:\n"
                                            f"Supplier Name: {supplier_name_inp}\n"
                                            f"Item Name: {item_name_inp}\n"
                                            f"Item No.: {item_no_inp}\n"
                                            f"Description: {description_inp}\n"
                                            f"UOM: {unit_inp}\n"
                                            f"Reorder Level: {reorder_lvl_inp}\n"
                                            f"Reorder Days: {reorder_days_inp}\n"
                                            f"Reorder Qty: {reorder_qty_inp}\n",
                                            QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if confirmation_box == QMessageBox.Yes:
            d = mp.insert_prod(supplier_name_inp, item_name_inp, item_no_inp, description_inp, unit_inp, reorder_lvl_inp,
                            reorder_days_inp, reorder_qty_inp, stock_add_date_time)
            print(d)

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
        # Function for add stock tab
        layout = QFormLayout()

        # Calendar widget
        self.expiry_add = QDateEdit(self)
        self.expiry_add.setDisplayFormat('dd-MM-yyyy')
        self.expiry_add.setCalendarPopup(True)
        self.expiry_add.setDate(QDate(7999,12,31))

        # Add item button
        self.ok_add = QPushButton('Add Item', self)
        cancel = QPushButton('Cancel', self)

        # Individual line edits
        self.item_no_add = QLineEdit()
        layout.addRow("Item No.", self.item_no_add)

        self.stock_count_add = QLineEdit()
        layout.addRow("Quantity to Add", self.stock_count_add)

        self.cost_per_item_add = QLineEdit()
        layout.addRow("Cost Per Item", self.cost_per_item_add)

        self.location_add = QLineEdit()
        layout.addRow("Location of Item", self.location_add)

        # Create the label for the date field
        layout.addRow("Expiry Date", self.expiry_add)
        # self.expiry_add.dateChanged.connect(self.on_select_date)

        layout.addWidget(self.ok_add)
        layout.addWidget(cancel)

        self.ok_add.clicked.connect(self.confirmation_add_stock)

        self.tab1.setLayout(layout)

        # Clear all fields when cancel is clicked
        self.field_dict_tab1UI = {"Item No.": self.item_no_add,
                                  "Quantity to Add": self.stock_count_add,
                                  "Cost Per Item": self.cost_per_item_add,
                                  "Location of Item": self.location_add,
                                  "Expiry Date": self.expiry_add}

        for key, value in self.field_dict_tab1UI.items():
            cancel.clicked.connect(value.clear)

    def confirmation_add_stock(self):
        empty_fields_array = []
        incorrect_dtype_array = []
        for key, value in self.field_dict_tab1UI.items():
            if check_input.check_empty_field(value.text()) == 'blank':
                empty_fields_array.append(key)
            # if check_input.check_dtype(value.text()) == 'error':
            #     incorrect_dtype_array.append(key)

        if empty_fields_array:
            # there are empty fields
            empty_fields_message = "\n".join(empty_fields_array)
            error_message_box = QtWidgets.QMessageBox()
            error_message_box.warning(
                self, 'Error', f'Unable to add quantity.\nPlease ensure that the following fields have been filled.\n\n{empty_fields_message}')
            return 'Error'

        # print(field_array_tab1UI)
        # Follow this variable names
        now = datetime.datetime.now()
        item_no_add = self.item_no_add.text()
        stock_count_add = int(self.stock_count_add.text())
        cost_per_item_add = float(self.cost_per_item_add.text())
        location_add = self.location_add.text()
        expiry_add = self.expiry_add.text()
        print(expiry_add)
        stock_add_date_time = now.strftime("%Y-%m-%d %H:%M")

        confirmation_box = QMessageBox.question(self, 'Confirmation',
                                        f"Please confirm if you wish to add the following details:\n\n"
                                        f"Item No.: {item_no_add}\n"
                                        f"Qty to Add: {stock_count_add}\n"
                                        f"Cost per Item: {cost_per_item_add}\n"
                                        f"Location: {location_add}\n"
                                        f"Expiry Date: {expiry_add}\n",
                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if confirmation_box == QMessageBox.Yes:
            self.ok_add.clicked.connect(self.call_add)

    # def on_select_date(self, date):
    #     self.expiry_date_add = date.toString(Qt.ISODate)
    #     print(date)

    def tab2UI(self):
        # Function for reduce stock tab

        ## Requires confirmation once reduce qty button is pressed

        layout = QFormLayout()
        self.ok_red = QPushButton('Reduce Stock', self)
        cancel = QPushButton('Cancel', self)

        self.item_no_red = QLineEdit()
        layout.addRow("Item No.", self.item_no_red)

        self.serial_no_red = QLineEdit()
        layout.addRow("Serial No.", self.serial_no_red)

        self.stock_count_red = QLineEdit()
        layout.addRow("Quantity to Reduce", self.stock_count_red)

        self.location_red = QLineEdit()
        layout.addRow("Location", self.location_red)

        layout.addWidget(self.ok_red)
        layout.addWidget(cancel)
        self.tab2.setLayout(layout)
        self.ok_red.clicked.connect(self.confirmation_red_stock)

        # Clear all fields when cancel is clicked
        self.field_dict_tab2UI = {"Item No.": self.item_no_red,
                                  "Serial No.": self.serial_no_red,
                                  "Quantity to Reduce": self.stock_count_red,
                                  "Location": self.location_red}

        for key, value in self.field_dict_tab2UI.items():
            cancel.clicked.connect(value.clear)

    def confirmation_red_stock(self):
        empty_fields_array = []
        incorrect_dtype_array = []
        for key, value in self.field_dict_tab2UI.items():
            if check_input.check_empty_field(value.text()) == 'blank':
                empty_fields_array.append(key)
            # if check_input.check_dtype(value.text()) == 'error':
            #     incorrect_dtype_array.append(key)

        if empty_fields_array:
            # there are empty fields
            empty_fields_message = "\n".join(empty_fields_array)
            error_message_box = QtWidgets.QMessageBox()
            error_message_box.warning(
                self, 'Error', f'Unable to reduce quantity.\nPlease ensure that the following fields have been filled.\n\n{empty_fields_message}')
            return 'Error'
        # print(field_array_tab1UI)
        # Follow this variable names
        now = datetime.datetime.now()
        item_no_red = self.item_no_red.text()
        serial_no_red = self.serial_no_red.text()
        stock_count_red = int(self.stock_count_red.text())
        location_red = self.location_red.text()
        expiry_add = self.expiry_add.text()
        print(expiry_add)
        stock_red_date_time = now.strftime("%Y-%m-%d %H:%M")

        confirmation_box = QMessageBox.question(self, 'Confirmation',
                                                f"Please confirm if you wish to delete the following item from database:\n\n"
                                                f"Item No.: {item_no_red}\n"
                                                f"Serial No.: {serial_no_red}\n"
                                                f"Qty to Reduce: {stock_count_red}\n"
                                                f"Location: {location_red}\n",
                                                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if confirmation_box == QMessageBox.Yes:
            self.ok_add.clicked.connect(self.call_red)

    def tab3UI(self):

        # Function for del stock tab
        layout = QFormLayout()
        self.ok_del = QPushButton('Delete Stock', self)
        cancel = QPushButton('Cancel', self)

        self.item_no_del = QLineEdit()
        layout.addRow("Item No.", self.item_no_del)

        layout.addWidget(self.ok_del)
        layout.addWidget(cancel)
        self.tab3.setLayout(layout)
        self.ok_del.clicked.connect(self.confirmation_del_stock)
        # self.ok_del.clicked.connect(self.call_del)  # need to write function to delete stock
        # Clear all fields when cancel is clicked
        self.field_dict_tab3UI = {"Item No.": self.item_no_del}

        for key, value in self.field_dict_tab3UI.items():
            cancel.clicked.connect(value.clear)

    def confirmation_del_stock(self):

        empty_fields_array = []
        incorrect_dtype_array = []
        for key, value in self.field_dict_tab3UI.items():
            if check_input.check_empty_field(value.text()) == 'blank':
                empty_fields_array.append(key)
            # if check_input.check_dtype(value.text()) == 'error':
            #     incorrect_dtype_array.append(key)

        if empty_fields_array:
            # there are empty fields
            empty_fields_message = "\n".join(empty_fields_array)
            error_message_box = QtWidgets.QMessageBox()
            error_message_box.warning(
                self, 'Error', f'Unable to delete item.\nPlease ensure that the following fields have been filled.\n\n{empty_fields_message}')
            return 'Error'
        # print(field_array_tab1UI)
        # Follow this variable names
        now = datetime.datetime.now()
        item_no_del = self.item_no_del.text()
        stock_del_date_time = now.strftime("%Y-%m-%d %H:%M")

        confirmation_box = QMessageBox.question(self, 'Confirmation',
                                                f"Please confirm if you wish to remove the following item:\n\n"
                                                f"Item No.: {item_no_del}\n",
                                                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if confirmation_box == QMessageBox.Yes:
            self.ok_add.clicked.connect(self.call_del)

    def call_del(self):
        now = datetime.datetime.now()
        stock_del_date_time = now.strftime("%Y-%m-%d %H:%M")
        item_name = self.item_name_del.text().replace(' ','_').upper()
        mp.remove_stock(item_name,stock_del_date_time)

    def call_add(self):
        now = datetime.datetime.now()
        stock_call_add_date_time = now.strftime("%Y-%m-%d %H:%M")
        item_name = self.item_name_add.text().replace(' ','_').upper()
        stock_val = int(self.stock_count_add.text())
        mp.update_quantity(item_name, stock_val, stock_call_add_date_time)

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
                self, 'Error', f'The following files have invalid file type\n{invalid_files_message}')

        data = data.fillna('')
        data = data.astype(str)
        self.updateTable(data)


    def extract_pdf(self):
        print('extract pdf')




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

        #Add columns here
        stack3UI_headers = ['Stock Name', 'Quantity', 'Cost(Per Unit)']
        self.View.setColumnCount(3)
        self.View.setHorizontalHeaderLabels(stack3UI_headers)
        self.View.setColumnWidth(0, 250)
        self.View.setColumnWidth(1, 250)
        self.View.setColumnWidth(2, 200)



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
