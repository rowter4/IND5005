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
                             QHBoxLayout, QAction, QApplication, QLabel, QLineEdit,QMessageBox, QDialog, QApplication)

# import sqlite3
import re
import pandas as pd
import mysql.connector as mc

mydb = mc.connect(host='localhost', password='2023nusproject%', user='root', database='dr_db')
if mydb.is_connected():
    print("Connection established....")
    mycursor = mydb.cursor()


 # mycursor.close() #might need to close the connection to the database 


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
        uname = self.textName.text()
        passw = self.textPass.text()
        # connection = sqlite3.connect("user.db")
        # self.accept()
        sql_query = "SELECT * FROM user where user_id = '%s' AND password = '%s'" % (uname,passw) 
        # result = mycursor.execute( )
        # result = connection.execute("SELECT * FROM user WHERE USERNAME = ? AND PASSWORD = ?", (uname, passw))
        mycursor.execute(sql_query)
        myresults = mycursor.fetchall()
        print(myresults, "Result from Query")
        if myresults:
            self.accept()
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

        # self.stock_serialNo = QLineEdit()
        # layout.addRow("Serial Number (Numbers)", self.stock_serialNo)


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
        serial_no_inp = self.serial_no.text()


        confirmation_box = QMessageBox.question(self, 'Confirmation',
                                            f"Please Confirm the Following Details:\n"
                                            f"Supplier Name: {supplier_name_inp}\n"
                                            f"Item Name: {item_name_inp}\n"
                                            f"Item No.: {item_no_inp}\n"
                                            f"Serial No.: {serial_no_inp}\n"
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
            query = "INSERT INTO STOCK_LIST (supplier_name_inp,item_name_inp,item_no_inp,description_inp,unit_inp,reorder_lvl_inp,reorder_days_inp,reorder_qty_inp,stock_add_date_time, serial_no) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            value = (supplier_name_inp, item_name_inp, item_no_inp, description_inp, unit_inp, reorder_lvl_inp, reorder_days_inp, reorder_qty_inp, stock_add_date_time, serial_no_inp)
            mycursor.execute(query,value)
            mydb.commit()


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
        self.expiry_add.setDate(QDate(2099,12,31))

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

    def call_add(self):
        print("Tried to add the stock into the database")
        now = datetime.datetime.now()
        stock_call_add_date_time = now.strftime("%Y-%m-%d %H:%M")
        # item_name = self.item_name_add.text().replace(' ','_').upper()
        item_no = self.item_no_add.text()
        item_cost = self.cost_per_item_add.text()
        location = self.location_add.text()
        # expy_date = self.expiry_add.text()

        qty_val = (int(self.stock_count_add.text()))
        query = "SELECT stock_qty FROM stock_list WHERE item_no_inp = '"+item_no+"'"
        mycursor.execute(query)
        result_1 = mycursor.fetchall()
        for x in result_1:
            initial_stock = x[0]

        final_stock_cal = initial_stock + qty_val
        final_stock = str(final_stock_cal)

        query = "UPDATE stock_list SET stock_qty = '"+final_stock+"', cost_per_item = '"+item_cost+"', item_location = '"+location+"'  WHERE item_no_inp = '"+item_no+"'"
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
            self.ok_red.clicked.connect(self.call_red)

    def call_red(self):
        now = datetime.datetime.now()
        stock_red_date_time = now.strftime("%Y-%m-%d %H:%M")
        item_no = self.item_no_red.text()
        qty_val = -(int(self.stock_count_red.text()))

        query = "SELECT stock_qty FROM stock_list WHERE item_no_inp = '"+item_no+"'"
        mycursor.execute(query)
        result_2 = mycursor.fetchall()
        for x in result_2:
            initial_stock = x[0]
        final_stock_cal = initial_stock + qty_val
        final_stock = str(final_stock_cal)

        query = "UPDATE stock_list SET stock_qty = '"+final_stock+"' WHERE item_no_inp = '"+item_no+"'"
        mycursor.execute(query)
        mydb.commit()
        print(mycursor.rowcount, "record(s) affected")

        # mp.update_quantity(item_name, stock_val, stock_red_date_time)
        # except Exception:
        #     print('Exception')

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
        
        
        query = "DELETE FROM stock_list WHERE item_name='"+item_name+"' " 
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

        self.upload_table.setRowHeight(0, 20)

        layout.addWidget(self.choose_file)
        layout.addWidget(self.upload_table)

        layout.addWidget(widget_btm_buttons)
        layout.setAlignment(widget_btm_buttons, Qt.AlignRight)

        # self.clear_table_button.clicked.connect(self.clear_upload_table)
        # self.confirm_submit_upload_button.clicked.connect(self.update_DB_upload)
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
                self, 'Error', f'The following files have invalid file type\n{invalid_files_message}')

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


    def stack3UI(self):

        # table = mp.show_stock()
        print('show')
        # print(table)
        layout = QVBoxLayout()
        self.srb = QPushButton()
        self.srb.setText("Get Search Result.")
        self.View = QTableWidget()
        self.lbl3 = QLabel()
        self.lbl_conf_text = QLabel()
        self.lbl_conf_text.setText("Enter the search keyword:")
        self.conf_text = QLineEdit()

     
        self.View.setColumnCount(14)
        self.View.setRowCount(0)
        stack3UI_headers = ['Company Name', 'Item Name', 'Item No.', 'Description', 'Unit of Measurement', 'Reorder Level', 'Days Per Reorder', ' Reorder Quantity',
                            'Date Added', 'Serial No', 'Location', 'Cost Per Item', 'Quantity', 'Inventory Value']
        self.View.setHorizontalHeaderLabels(stack3UI_headers)
        self.View.setColumnWidth(0, 250)
        self.View.setColumnWidth(1, 250)
        self.View.setColumnWidth(2, 200)
        self.View.setColumnWidth(3, 200)
        self.View.setColumnWidth(4, 200)
        self.View.setColumnWidth(5, 200)
        self.View.setColumnWidth(6, 200)
        self.View.setColumnWidth(7, 200)
        self.View.setColumnWidth(8, 250)
        self.View.setColumnWidth(9, 200)
        self.View.setColumnWidth(10, 200)
        self.View.setColumnWidth(11, 200)
        self.View.setColumnWidth(12, 200)
        self.View.setColumnWidth(13, 200)

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
    
    def upload_data(self):
        sql_query1 = "SELECT * FROM stock_list" 
        mycursor.execute(sql_query1)
        results = mycursor.fetchall()
        print(results, "Results that are called from the stock")

        for row_number, row_data in enumerate(results):
            self.View.insertRow(row_number)
            for column_number,data in enumerate(row_data):
                self.View.setItem(row_number, column_number, QtWidgets.QTableWidgetItem(str(data)))



    def show_search(self): #this code is for filtering the data that we would like to show. However, this is not being used for now

        sql_query1 = "SELECT * FROM stock_list" 
        mycursor.execute(sql_query1)
        results = mycursor.fetchall()
        print(results, "Results that are called from the stock")

        if self.View.rowCount()>1:
            for i in range(1,self.View.rowCount()):
                self.View.removeRow(1)

        # x_act = mp.show_stock()
        # print(x_act, "Result for Stock Count from SQL Lite")

        #the table is already integrated with MySQL using the 'results' variable
        x = []

        if self.conf_text.text() != '':
            print("DEBUG: there is a text")
            for i in range(0,len(results)):
                a = list(results[i])
                if self.conf_text.text().lower() in a[0].lower():
                    x.append(a)
        else:
            print("DEBUG : fetching the data again")
            print(results, "DEBUG : check if result variable is populated")
            x = results


        if len(x)!=0:
            for i in range(1,len(x)+1):
                self.View.insertRow(i)
                a = list(x[i-1])
                print(str(a[0]), "DEBUG : get value for a[0]")
                self.View.setItem(i, 0, QTableWidgetItem(str(a[0].replace('_',' ').upper())))
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
