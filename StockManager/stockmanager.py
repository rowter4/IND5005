from PyQt5 import QtWidgets, QtGui
import os
import datetime

import sys

from numpy import double
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
                             QHBoxLayout, QAction, QApplication, QLabel, QLineEdit,QMessageBox)

# import sqlite3
import re
import pandas as pd
import mysql.connector as mc

mydb = mc.connect(host='localhost', password='2023nusproject%', user='root', database='dr_db')
if mydb.is_connected():
    print("Connection established....")
    mycursor = mydb.cursor()

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
        self.accept()
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

        self.stock_name = QLineEdit()
        layout.addRow("Stock Name", self.stock_name)

        self.stock_count = QLineEdit()
        layout.addRow("Quantity", self.stock_count)

        self.stock_cost = QLineEdit()
        layout.addRow("Cost of Stock (per item)", self.stock_cost)

        self.stock_serialNo = QLineEdit()
        layout.addRow("Serial Number (Numbers)", self.stock_serialNo)


        layout.addWidget(self.ok)
        layout.addWidget(cancel)

        self.ok.clicked.connect(self.on_click)

        cancel.clicked.connect(self.stock_name.clear)
        cancel.clicked.connect(self.stock_cost.clear)
        cancel.clicked.connect(self.stock_count.clear)
        cancel.clicked.connect(self.stock_serialNo.clear)
        self.stack1.setLayout(layout)

    def on_click(self):
        now = datetime.datetime.now()
        stock_name_inp = self.stock_name.text().replace(' ','_').lower()
        stock_count_inp = int(self.stock_count.text())
        stock_cost_inp = double(self.stock_cost.text())
        stock_serialNo_inp = int(self.stock_serialNo.text())

        print(stock_name_inp,stock_count_inp,stock_cost_inp, stock_serialNo_inp, "Details from Add Stock" )

        stock_add_date_time = now.strftime("%Y-%m-%d %H:%M")

        # Below is the old database
            # d = mp.insert_prod(stock_name_inp,stock_count_inp,stock_cost_inp,stock_add_date_time)
            # print(d)
        #Need to add the above details to table

        mycursor = mydb.cursor()
        query = "INSERT INTO STOCK_1 (name,sn,quantity,cost) VALUES (%s,%s,%s,%s)"
        value = (stock_name_inp, stock_serialNo_inp, stock_count_inp, stock_cost_inp)
        mycursor.execute(query,value)
        mydb.commit()
        # self.labelResult.setText("Data Inserted")



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
        self.ok_add = QPushButton('Add Stock', self)
        cancel = QPushButton('Cancel', self)

        self.stock_name_add = QLineEdit()
        layout.addRow("Stock Name", self.stock_name_add)

        self.stock_count_add = QLineEdit()
        layout.addRow("Quantity to add", self.stock_count_add)

        layout.addWidget(self.ok_add)
        layout.addWidget(cancel)
        self.tab1.setLayout(layout)

        self.ok_add.clicked.connect(self.call_add)       #need to write function to add quantity
        cancel.clicked.connect(self.stock_name_add.clear)
        cancel.clicked.connect(self.stock_count_add.clear)

    def tab2UI(self):
        layout = QFormLayout()
        self.ok_red = QPushButton('Reduce Stock', self)
        cancel = QPushButton('Cancel', self)

        self.stock_name_red = QLineEdit()
        layout.addRow("Stock Name", self.stock_name_red)

        self.stock_count_red = QLineEdit()
        layout.addRow("Quantity to reduce", self.stock_count_red)


        layout.addWidget(self.ok_red)
        layout.addWidget(cancel)
        self.tab2.setLayout(layout)

        self.ok_red.clicked.connect(self.call_red)  # need to write function to reduce quantity
        cancel.clicked.connect(self.stock_name_red.clear)
        cancel.clicked.connect(self.stock_count_red.clear)

    def tab3UI(self):
        layout = QFormLayout()
        self.ok_del = QPushButton('Delete Stock', self)
        cancel = QPushButton('Cancel', self)

        self.stock_name_del = QLineEdit()
        layout.addRow("Stock Name", self.stock_name_del)
        layout.addWidget(self.ok_del)
        layout.addWidget(cancel)
        self.tab3.setLayout(layout)

        self.ok_del.clicked.connect(self.call_del)  # need to write function to delete stock
        cancel.clicked.connect(self.stock_name_del.clear)


    def call_del(self):
        now = datetime.datetime.now()
        stock_del_date_time = now.strftime("%Y-%m-%d %H:%M")
        stock_name = self.stock_name_del.text().replace(' ','_').lower()
        mp.remove_stock(stock_name,stock_del_date_time)

    def call_red(self):
        now = datetime.datetime.now()
        stock_red_date_time = now.strftime("%Y-%m-%d %H:%M")
        stock_name = self.stock_name_red.text().replace(' ','_').lower()
        try:
            stock_val = -(int(self.stock_count_red.text()))
            print(stock_val)
            print(type(stock_val))
            mp.update_quantity(stock_name, stock_val, stock_red_date_time)
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
        stock_name = self.stock_name_add.text().replace(' ','_').lower()
        stock_val = int(self.stock_count_add.text())
        mp.update_quantity(stock_name, stock_val, stock_call_add_date_time)


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

        self.View.setColumnCount(4)
        self.View.setColumnWidth(0, 250)
        self.View.setColumnWidth(1, 250)
        self.View.setColumnWidth(2, 200)
        self.View.setColumnWidth(3, 200)

        self.View.insertRow(0)
        self.View.setItem(0, 0, QTableWidgetItem('Stock Name'))
        self.View.setItem(0, 1, QTableWidgetItem('Quantity'))
        self.View.setItem(0, 2, QTableWidgetItem('Cost(Per Unit)'))
        self.View.setItem(0, 3, QTableWidgetItem('Test2 Header'))

        
        
        # self.tableWidget.setRowCount(0)
        # for row_number, row_data in enumerate(results):
        #     self.tableWidget.insertRow(row_number)

        #     for column_number, data in enumerate(row_data):
        #         self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)) )


       
        
        # print(results, "Results that are called from the stock")

       

        # cur = self.SQLiteDB.cursor()
        # cur.execute("SELECT * FROM SQLTable")admi
        # allSQLRows= cursor.fetchall()

        # self.myTableWidget.setRowCount(len(stockResults)) ##set number of rows
        # self.myTableWidget.setColumnCount(8) ##this is fixed for myTableWidget, ensure that both of your tables, sql and qtablewidged have the same number of columns

        # row = 0
        # while True:
        #     sqlRow = mycursor.fetchone()
        #     if sqlRow == None:
        #         break ##stops while loop if there is no more lines in sql table
        #     for col in range(0, 8): ##otherwise add row into tableWidget
                # self.myTableWidget.setItem(row, col, QtGui.QTableWidgetItem(sqlRow[col]))
            # row += 1


        layout.addWidget(self.View)
        layout.addWidget(self.lbl_conf_text)
        layout.addWidget(self.conf_text)
        layout.addWidget(self.srb)
        layout.addWidget(self.lbl3)
        self.srb.clicked.connect(self.show_search)
        self.stack3.setLayout(layout)

    def show_search(self):

        sql_query1 = "SELECT * FROM stock_1" 
        mycursor.execute(sql_query1)
        results = mycursor.fetchall()
        print(results, "Results that are called from the stock")

        if self.View.rowCount()>1:
            for i in range(1,self.View.rowCount()):
                self.View.removeRow(1)


        x_act = mp.show_stock()
        print(x_act, "Result for Stock Count from SQL Lite")
        x = []

        if self.conf_text.text() != '':
            for i in range(0,len(results)):
                a = list(results[i])
                if self.conf_text.text().lower() in a[0].lower():
                    x.append(a)
        else:
            x = results

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
