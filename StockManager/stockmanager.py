from PyQt5 import QtWidgets, QtGui
import os
import datetime
import check_input

import sys

from numpy import double
import manipulation as mp
from PyQt5.QtCore import QRect, Qt, QDate
from PyQt5.QtWidgets import QTabWidget, QFileDialog, QAbstractItemView
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
                             QHBoxLayout, QAction, QApplication, QLabel, QLineEdit, QMessageBox)

# import sqlite3
import re
import pandas as pd
import mysql.connector as mc

mydb = mc.connect(host='localhost', password='2023nusproject%', user='root', database='dr_db')
if mydb.is_connected():
    print("Connection established....")
    mycursor = mydb.cursor()


employee_id = 000

# try:
#     conn = sqlite3.connect('stock.db')
#     c = conn.cursor()
#     c.execute("""CREATE TABLE stock (
#                 name text,
#                 quantity integer,
#                 cost integer
#                 ) """)
#     conn.commit()
# except Exception:
#     print('DB exists')


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

    def login_check(self, parent=None):
        global employee_id
        uname = self.textName.text()
        passw = self.textPass.text()
        # connection = sqlite3.connect("user.db")
        # self.accept()
        sql_query = "SELECT * FROM user where user_id = '%s' AND password = '%s'" % (uname, passw)
        # result = mycursor.execute( )
        # result = connection.execute("SELECT * FROM user WHERE USERNAME = ? AND PASSWORD = ?", (uname, passw))
        mycursor.execute(sql_query)
        myresults = mycursor.fetchall()
        print(myresults, "Result from Query")
        if myresults:
            self.accept()

            employee_id = myresults[0][2]
            print("Login Credentials is Valid")
            # loginFlag = True
            # if login.exec_() == QtWidgets.QDialog.Accepted:
            #     window = Example()
            #     print("Able to log in")
            #     # sys.exit(app.exec_())
        else:
            print("invalid login")
            QtWidgets.QMessageBox.warning(self, 'Error', 'Bad user or password')
            # login = Login()
            # Login.__init__(self)

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
        self.setGeometry(200, 150, 1000, 800)
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
        # Check for existing item number
        sql_query_check_existing = f"SELECT * FROM stock_list where item_no_inp = '{self.item_no.text()}'"
        mycursor = mydb.cursor()
        mycursor.execute(sql_query_check_existing)
        results_check_existing = mycursor.fetchall()
        print('results_check_existing')
        print(results_check_existing)
        if results_check_existing:
            error_message_box = QtWidgets.QMessageBox()
            error_message_box.warning(
                self, 'Error',
                f'Item No. {self.item_no.text()} already exist in the database.')
            return 'Error'

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
                self, 'Error',
                f'Unable to add item to inventory. \nPlease ensure that the following fields have been filled.\n\n{empty_fields_message}')
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
            # d = mp.insert_prod(supplier_name_inp, item_name_inp, item_no_inp, description_inp, unit_inp, reorder_lvl_inp,
            #                 reorder_days_inp, reorder_qty_inp, stock_add_date_time)
            # print(d)

            mycursor = mydb.cursor()
            query = "INSERT INTO STOCK_LIST (supplier_name_inp,item_name_inp,item_no_inp,description_inp,unit_inp,reorder_lvl_inp,reorder_days_inp,reorder_qty_inp,stock_add_date_time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            value = (
            supplier_name_inp, item_name_inp, item_no_inp, description_inp, unit_inp, reorder_lvl_inp, reorder_days_inp,
            reorder_qty_inp, stock_add_date_time)
            mycursor.execute(query, value)
            mydb.commit()

            self.upload_data()
            self.show_trans_history()
            self.add_trans_history("INSERT", item_name_inp, item_no_inp, 0)

    def stack2UI(self):

        layout = QHBoxLayout()
        layout.setGeometry(QRect(0, 300, 1150, 500))
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
        self.expiry_add.setDate(QDate(7999, 12, 31))

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
                self, 'Error',
                f'Unable to add quantity.\nPlease ensure that the following fields have been filled.\n\n{empty_fields_message}')
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
            self.upload_data()
            self.show_trans_history()
            self.add_trans_history("UPDATE", "", item_no_add, stock_count_add)

    # def on_select_date(self, date):
    #     self.expiry_date_add = date.toString(Qt.ISODate)
    #     print(date)

    def call_add(self):
        now = datetime.datetime.now()
        stock_call_add_date_time = now.strftime("%Y-%m-%d %H:%M")
        # item_name = self.item_name_add.text().replace(' ','_').upper()
        stock_val = (self.stock_count_add.text())

        print("updated stock Value is : ", stock_val)

        query = "UPDATE stock_list SET unit_inp = '" + stock_val + "' WHERE item_no_inp = '1'"
        # need to update query to reflect the item no.
        mycursor.execute(query)
        mydb.commit()
        print(mycursor.rowcount, "record(s) affected")

        # mp.update_quantity(item_name, stock_val, stock_call_add_date_time)

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
                self, 'Error',
                f'Unable to reduce quantity.\nPlease ensure that the following fields have been filled.\n\n{empty_fields_message}')
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
            self.add_trans_history("UPDATE", "", item_no_red, -stock_count_red)

    def call_red(self):
        now = datetime.datetime.now()
        stock_red_date_time = now.strftime("%Y-%m-%d %H:%M")
        item_name = self.item_name_red.text().replace(' ', '_').lower()
        try:
            stock_val = -(int(self.stock_count_red.text()))
            print(stock_val)
            print(type(stock_val))

            item_no = self.item_no_red.text()

            print("updated stock Value is : ", stock_val)

            query = "UPDATE stock_list SET unit_inp = '" + stock_val + "' WHERE item_no_inp = '" + item_no + "'"
            mycursor.execute(query)
            mydb.commit()
            print(mycursor.rowcount, "record(s) affected")

            # mp.update_quantity(item_name, stock_val, stock_red_date_time)
        except Exception:
            print('Exception')

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
                self, 'Error',
                f'Unable to delete item.\nPlease ensure that the following fields have been filled.\n\n{empty_fields_message}')
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
            self.add_trans_history("DELETE", "", item_no_del, 0)

    def call_del(self):
        now = datetime.datetime.now()
        stock_del_date_time = now.strftime("%Y-%m-%d %H:%M")
        item_name = self.item_name_del.text().replace(' ', '_').upper()

        query = "DELETE FROM stock_list WHERE item_name='" + item_name + "' "
        mycursor.execute(query)
        mydb.commit()
        print(mycursor.rowcount, "record(s) affected")

        # mp.remove_stock(item_name,stock_del_date_time)

    def tab4UI(self):
        layout = QVBoxLayout()
        self.choose_file = QPushButton()
        self.choose_file.setText("Choose File")
        self.choose_file.clicked.connect(self.open_file_dialogue)
        self.choose_file.setMinimumWidth(50)
        self.choose_file.setMaximumWidth(100)

        widget_btm_buttons = QWidget()
        layout_btm_buttons = QHBoxLayout()

        self.clear_table_button = QPushButton()
        self.clear_table_button.setText("Clear")
        self.clear_table_button.setFixedWidth(80)

        self.confirm_submit_upload_button = QPushButton()
        self.confirm_submit_upload_button.setText("Confirm")
        self.confirm_submit_upload_button.setFixedWidth(80)

        layout_btm_buttons.addWidget(self.clear_table_button)
        layout_btm_buttons.addWidget(self.confirm_submit_upload_button)
        widget_btm_buttons.setLayout(layout_btm_buttons)
        # self.setCellWidget(2,0,widget_btm_buttons)

        headers = ['Invoice No.', 'Item No.', 'Location', 'Supplier', 'Item Name', 'Quantity', 'Inventory Value']

        self.upload_table = QTableWidget()

        font = QFont()
        font.setPointSize(10)
        self.upload_table.setFont(font)
        self.upload_table.verticalHeader().setDefaultSectionSize(15)

        self.upload_table.setColumnCount(7)
        self.upload_table.setHorizontalHeaderLabels(headers)
        self.upload_table.setColumnWidth(0, 100)
        self.upload_table.setColumnWidth(1, 100)
        self.upload_table.setColumnWidth(2, 100)
        self.upload_table.setColumnWidth(3, 100)
        self.upload_table.setColumnWidth(4, 100)
        self.upload_table.setColumnWidth(5, 100)
        self.upload_table.setColumnWidth(6, 100)

        self.df = pd.DataFrame()

        layout.addWidget(self.choose_file)
        layout.addWidget(self.upload_table)

        layout.addWidget(widget_btm_buttons)
        layout.setAlignment(widget_btm_buttons, Qt.AlignRight)

        self.clear_table_button.clicked.connect(self.clear_upload_table)
        self.confirm_submit_upload_button.clicked.connect(self.update_DB_upload)
        self.tab4.setLayout(layout)

    def updateTable(self):
        # Clear existing table content

        self.upload_table.setRowCount(self.df.shape[0])

        for row_num, row_data in self.df.iterrows():
            for col_num, cell_data in enumerate(row_data):
                self.upload_table.setItem(row_num, col_num, QTableWidgetItem(cell_data))

        self.upload_table.itemChanged.connect(self.on_item_changed)

    def open_file_dialogue(self):
        filenames, _ = QFileDialog.getOpenFileNames(
            None,
            "QFileDialog.getOpenFileNames()",
            "",
            # "All Files (*);;Python Files (*.py);;Text Files (*.txt)",
            "All Files (*);;Excel Files (*.xlsx);;Text Files (*.csv);;PDF Files (*.pdf)",
        )


        invalid_files = []
        error_opening_files = []
        pdf_files = []
        headers = ['Invoice No.', 'Item No.', 'Location', 'Supplier', 'Item Name', 'Quantity', 'Inventory Value']
        self.df = pd.DataFrame(columns=headers)

        if filenames:
            for filename in filenames:
                fileextension = re.search(".*\.([^\.]+)$", filename).group(1)
                # print(f'{fileextension}: {filename}')
                if fileextension == 'pdf':
                    pdf_files.append(filename)
                elif fileextension == 'csv':
                    try:
                        read_csv_data = pd.read_csv(filename)
                        if self.check_uploadFile_schema(read_csv_data, headers) == 1:
                            invalid_files.append(filename)
                        else:
                            self.df = pd.concat([self.df, read_csv_data])
                    except:
                        error_opening_files.append(filename)
                elif fileextension in ['xlsx', 'xls']:
                    try:
                        read_xls_data = pd.read_excel(filename)
                        if self.check_uploadFile_schema(read_xls_data, headers) == 1:
                            invalid_files.append(filename)
                        else:
                            self.df = pd.concat([self.df, read_xls_data])
                    except:
                        error_opening_files.append(filename)
                else:
                    invalid_files.append(filename)

        invalid_files_message = "\n".join(invalid_files)
        error_opening_files_message = "\n".join(error_opening_files)
        font = QFont('Calibri', 10)

        if invalid_files_message:
            error_message_box = QtWidgets.QMessageBox()
            error_message_box.setFont(font)
            error_message_box.warning(
                self, 'Error',
                f'The following files have invalid file type or invalid format \n {invalid_files_message}')

        if error_opening_files_message:
            error_message_box = QtWidgets.QMessageBox()
            error_message_box.setFont(font)
            error_message_box.warning(
                self, 'Error',
                f'Unable to read the following files. Please check if there are any restrictions on the file. \n {error_opening_files_message}')

        self.df = self.df.fillna('')
        self.df = self.df.astype(str)
        self.updateTable()


    def on_item_changed(self, item):
        row = item.row()
        col = item.column()
        value = item.text()
        self.df.iloc[row, col] = value
        # print(f"Row:{row}, Col:{col}, value:{value}")

    def extract_pdf(self):
        print('extract pdf')


    def clear_upload_table(self):
        # self.upload_table.clearContents()
        while self.upload_table.rowCount() > 0 :
            self.upload_table.removeRow(0)
        self.df = pd.DataFrame()

    def update_DB_upload(self):
        # upload to stock DB

        # update transaction history
        for index, df_row in self.df.iterrows():
            self.add_trans_history("BULK", df_row['Item Name'], df_row['Item No.'], df_row['Quantity'])

        # clear table widget
        while self.upload_table.rowCount() > 0:
            self.upload_table.removeRow(0)

        if self.df.shape[0] > 0:
            success_message_box = QtWidgets.QMessageBox()
            success_message_box.warning(self, 'Message', f'Successfully updated database')
        self.df = pd.DataFrame()


    def check_uploadFile_schema(self, df, headers):
        if list(df.columns) == headers:
            return 0
        else:
            return 1

    def stack3UI(self):

        # table = mp.show_stock()
        print('show')
        # print(table)
        layout = QVBoxLayout()
        self.srb = QPushButton()
        self.srb.setText("Get Search Result.")
        self.View = QTableWidget()

        font = QFont()
        font.setPointSize(10)
        self.View.setFont(font)
        self.View.verticalHeader().setDefaultSectionSize(15)

        self.lbl3 = QLabel()
        self.lbl_conf_text = QLabel()
        self.lbl_conf_text.setText("Enter the search keyword:")
        self.conf_text = QLineEdit()

        self.View.setColumnCount(14)
        self.View.setRowCount(0)

        stack3UI_headers = ['Supplier Name', 'Item Name', 'Item No.', 'Description', 'Unit of Measurement',
                            'Reorder Level', 'Days Per Reorder', ' Reorder Quantity',
                            'Date Added', 'Serial No', 'Location', 'Quantity', 'Cost Per Item', 'Inventory Value']
        self.View.setHorizontalHeaderLabels(stack3UI_headers)
        self.View.setColumnWidth(0, 150)
        self.View.setColumnWidth(1, 150)
        self.View.setColumnWidth(2, 100)
        self.View.setColumnWidth(3, 150)
        self.View.setColumnWidth(4, 75)
        self.View.setColumnWidth(5, 75)
        self.View.setColumnWidth(6, 75)
        self.View.setColumnWidth(7, 75)
        self.View.setColumnWidth(8, 150)
        self.View.setColumnWidth(9, 100)
        self.View.setColumnWidth(10, 75)
        self.View.setColumnWidth(11, 75)
        self.View.setColumnWidth(12, 75)
        self.View.setColumnWidth(13, 75)

        # cur = self.SQLiteDB.cursor()
        # cur.execute("SELECT * FROM SQLTable")admi
        # allSQLRows= cursor.fetchall()

        layout.addWidget(self.View)

        layout.addWidget(self.lbl_conf_text)
        layout.addWidget(self.conf_text)
        layout.addWidget(self.srb)
        layout.addWidget(self.lbl3)
        self.stack3.setLayout(layout)
        self.srb.clicked.connect(self.upload_data)

    def clear_view_table(self):

        # self.upload_table.clearContents()

        while self.View.rowCount() > 0:
            self.View.removeRow(0)

    def upload_data(self):
        sql_query1 = "SELECT * FROM stock_list"
        mycursor.execute(sql_query1)
        results = mycursor.fetchall()
        print(results, "Results that are called from the stock")
        self.clear_view_table()
        for row_number, row_data in enumerate(results):
            self.View.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.View.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))

    def show_search(
            self):  # this code is for filtering the data that we would like to show. However, this is not being used for now

        sql_query1 = "SELECT * FROM stock_list"
        mycursor.execute(sql_query1)
        results = mycursor.fetchall()
        print(results, "Results that are called from the stock")

        if self.View.rowCount() > 1:
            for i in range(1, self.View.rowCount()):
                self.View.removeRow(1)

        # x_act = mp.show_stock()
        # print(x_act, "Result for Stock Count from SQL Lite")

        # the table is already integrated with MySQL using the 'results' variable
        x = []

        if self.conf_text.text() != '':
            print("DEBUG: there is a text")
            for i in range(0, len(results)):
                a = list(results[i])
                if self.conf_text.text().lower() in a[0].lower():
                    x.append(a)
        else:
            print("DEBUG : fetching the data again")
            print(results, "DEBUG : check if result variable is populated")
            x = results

        if len(x) != 0:
            for i in range(1, len(x) + 1):
                self.View.insertRow(i)
                a = list(x[i - 1])
                print(str(a[0]), "DEBUG : get value for a[0]")
                self.View.setItem(i, 0, QTableWidgetItem(str(a[0].replace('_', ' ').upper())))
                self.View.setItem(i, 1, QTableWidgetItem(str(a[1])))
                self.View.setItem(i, 2, QTableWidgetItem(str(a[2])))
                # self.View.setRowHeight(i, 10)
            self.lbl3.setText('Viewing Stock Database.')
        else:
            self.lbl3.setText('No valid information in database.')

    def stack4UI(self):
        layout = QVBoxLayout()
        self.srt = QPushButton()
        self.srt.setText("Get Transaction History.")
        self.Trans = QTableWidget()

        font = QFont()
        font.setPointSize(10)
        self.Trans.setFont(font)
        self.Trans.verticalHeader().setDefaultSectionSize(15)

        self.lbl4 = QLabel()
        self.lbl_trans_text = QLabel()
        self.lbl_trans_text.setText("Enter the search keyword:")
        self.trans_text = QLineEdit()

        self.Trans.setColumnCount(7)
        self.Trans.setHorizontalHeaderLabels(
            ['Transaction ID', 'Employee ID', 'Item Name', 'Item No.', 'Quantity', 'Transaction Type', 'Date'])
        self.Trans.setColumnWidth(0, 150)
        self.Trans.setColumnWidth(1, 150)
        self.Trans.setColumnWidth(2, 150)
        self.Trans.setColumnWidth(3, 100)
        self.Trans.setColumnWidth(4, 100)
        self.Trans.setColumnWidth(5, 150)
        self.Trans.setColumnWidth(6, 150)

        layout.addWidget(self.Trans)
        layout.addWidget(self.lbl_trans_text)
        layout.addWidget(self.trans_text)
        layout.addWidget(self.srt)
        layout.addWidget(self.lbl4)
        self.srt.clicked.connect(self.show_trans_history)
        self.stack4.setLayout(layout)


    def add_trans_history(self, transaction_type, stock_name, item_no, qty):
        print('this is employee number ' + str(employee_id))
        sql_tid = "SELECT max(trn_id) FROM trn_hist"
        mycursor.execute(sql_tid)
        try:
            results_tid = mycursor.fetchall()[0][0] + 1
        except:
            results_tid = 1900001

        if stock_name == "":

            sql_query_item_name = f"SELECT item_name_inp FROM STOCK_LIST where item_no_inp = '{item_no}'"
            mycursor.execute(sql_query_item_name)
            stock_name = mycursor.fetchall()[0][0]
            print(stock_name)


        date_now = datetime.datetime.now()
        query_trns_hist = "INSERT INTO trn_hist (trn_id,user_id,stock_name,item_no,qty,trns_mode,date) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        value_trns_hist = (
            results_tid, employee_id, stock_name, item_no, qty, transaction_type, date_now)
        print(value_trns_hist)
        mycursor.execute(query_trns_hist, value_trns_hist)
        mydb.commit()


    def clear_trans_table(self):

        # self.upload_table.clearContents()
        while self.Trans.rowCount() > 0:
            self.Trans.removeRow(0)


    def show_trans_history(self):

        sql_query_trans_hist = "SELECT * FROM trn_hist"
        mycursor.execute(sql_query_trans_hist)
        results_trans_hist = mycursor.fetchall()
        print(results_trans_hist)
        self.clear_trans_table()
        for row_number, row_data in enumerate(results_trans_hist):
            self.Trans.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.Trans.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))


    def display(self, i):
        self.Stack.setCurrentIndex(i)


if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)
    print("Getting the login first")
    loginFlag = False
    login = Login()
    login.show()

    if login.exec_() == QtWidgets.QDialog.Accepted:
        # if loginFlag == True: 
        window = Example()
        print("Able to log in")
    # sys.exit(app.exec_())

    sys.exit(app.exec_())
