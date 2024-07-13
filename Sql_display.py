# -------------------------------------------------------------------------------
# Name:             Sql_display.py
# Purpose:          Generic Sqlite starup. Open and connect to a dBase
#
# Author:           Jeffreaux
#
# Created:          07July24
#
# Required Packages:    PyQt5, PyQt5-Tools
# -------------------------------------------------------------------------------

from PyQt5.QtWidgets import (
    QMainWindow,
    QApplication,
    QPushButton,
    QAction,
    QLineEdit,
    QLabel,
    QPlainTextEdit,
    QStackedWidget,
)
from PyQt5 import uic

# from fileModule import *
import sys
import sqlite3
import random

# Create dBase and create cursor
conn = sqlite3.connect("test.db")
c = conn.cursor()

command_create_table = """
                    CREATE TABLE IF NOT EXISTS people(
                    id INTEGER PRIMARY KEY,
                    firstname TEXT,
                    lastname TEXT,
                    email TEXT,
                    town TEXT,
                    age INTEGER
                    )"""

c.execute(command_create_table)
# c.execute("INSERT INTO people(firstname, lastname, email, town, age) VALUES ('Brennen', 'Deslatte', 'Bernon@Deslatte.com', 'Lafayette', '26')")

# c.execute("CREATE TABLE IF NOT EXISTS people (firstname, lastname, age)")
# c.execute("INSERT INTO people VALUES ('John', 'Richard', 23)")

conn.commit()
conn.close()


class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        # Load the UI file
        uic.loadUi("Sql_display_GUI.ui", self)

        # define Widgets
        self.btnExit = self.findChild(QPushButton, "btnExit")
        self.btnBack2Search = self.findChild(QPushButton, "btnBack2Search")
        self.btnGo = self.findChild(QPushButton, "btnGo")

        self.txtFirstName = self.findChild(QLineEdit, "txtFirstName")
        self.txtLastName = self.findChild(QLineEdit, "txtLastName")
        self.txtGetIndex = self.findChild(QLineEdit, "txtGetIndex")
        self.txtAge = self.findChild(QLineEdit, "txtAge")

        self.lblResults_Name = self.findChild(QLabel, "lblResults_Name")
        self.lblResults_Age = self.findChild(QLabel, "lblResults_Age")
        self.lblResults_Email = self.findChild(QLabel, "lblResults_Email")
        self.lblResults_Town = self.findChild(QLabel, "lblResults_Town")

        self.pteSearchResults = self.findChild(QPlainTextEdit, "pteSearchResults")

        self.actExit = self.findChild(QAction, "actExit")

        self.stackedWidget = self.findChild(QStackedWidget, "stackedWidget")

        # Define the actions
        self.btnExit.clicked.connect(self.closeEvent)
        self.btnGo.clicked.connect(self.get_index)
        self.btnBack2Search.clicked.connect(self.go2Search)

        self.txtFirstName.returnPressed.connect(self.search_firstname)
        self.txtLastName.returnPressed.connect(self.search_lastname)
        self.txtGetIndex.returnPressed.connect(self.get_index)

        self.actExit.triggered.connect(self.closeEvent)

        #self.stackedWidget.setCurrentWidget(self.Search)
        self.stackedWidget.setCurrentWidget(self.Results)

        # Show the app
        self.show()

        self.get_random_index()

    def search_firstname(self):
        print("Searching through FIRST names")
        self.pteSearchResults.clear()
        conn = sqlite3.connect("test.db")  # Opening dB for reading
        c = conn.cursor()
        first_name_search = self.txtFirstName.text()
        c.execute(
            "SELECT * FROM people WHERE firstname LIKE (?) ", (first_name_search + "%",)
        )
        items = c.fetchall()
        for item in items:
            print(str(item))
            self.pteSearchResults.appendPlainText((f"{item[0]} - {item[1]} {item[2]}"))
        self.txtFirstName.clear()

        conn.commit()
        conn.close()

    def search_lastname(self):
        print("Searching through LAST names")
        self.pteSearchResults.clear()
        conn = sqlite3.connect("test.db")  # Opening dB for reading
        c = conn.cursor()
        last_name_search = self.txtLastName.text()
        
        c.execute(
            "SELECT * FROM people WHERE lastname LIKE (?) ", (last_name_search + "%",)
        )

        items = c.fetchall()
        for item in items:
            print(item)
            # Send results to output window
            self.pteSearchResults.appendPlainText((f"{item[0]} - {item[1]} {item[2]}"))
        self.txtLastName.clear()

        conn.commit()
        conn.close()

        self.txtLastName.clear()

    def get_index(self):
        print("Fetching Index")
        print(f"{self.txtGetIndex.text()} was selected!")
        selection = self.txtGetIndex.text()
        conn = sqlite3.connect("test.db")  # Opening dB for reading
        c = conn.cursor()
        # Retrieving selected record.  Record Identified by selection variable
        c.execute(f"SELECT * FROM people WHERE id ='{selection}'")  
        rlist = c.fetchone()
        print(rlist)
        print(f"{rlist[0]}, {rlist[1]}, {rlist[2]}, {rlist[3]}, {rlist[4]}")
        self.lblResults_Name.setText(f"{rlist[1]} {rlist[2]}")
        self.lblResults_Age.setText(str(rlist[5]))
        self.lblResults_Email.setText(rlist[3])
        self.lblResults_Town.setText(rlist[4])

        # Go to Results Page/Widget
        self.stackedWidget.setCurrentWidget(self.Results)

    def get_random_index(self):
        min_value = 1
        max_value = 7
        random_index = random.randint(min_value, max_value)
        print(random_index)
        conn = sqlite3.connect("test.db")  # Opening dB for reading
        c = conn.cursor()
        # Retrieving selected record.  Record Identified by selection variable
        c.execute(f"SELECT * FROM people WHERE id ='{random_index}'")  
        rlist = c.fetchone()
        print(rlist)
        print(f"{rlist[0]}, {rlist[1]}, {rlist[2]}, {rlist[3]}, {rlist[4]}")
        self.lblResults_Name.setText(f"{rlist[1]} {rlist[2]}")
        self.lblResults_Age.setText(str(rlist[5]))
        self.lblResults_Email.setText(rlist[3])
        self.lblResults_Town.setText(rlist[4])

        


    def go2Search(self):
        self.pteSearchResults.clear()
        self.txtGetIndex.setText(" ")
        self.stackedWidget.setCurrentWidget(self.Search)
    
    def closeEvent(self, *args, **kwargs):
        # print("Program closed Successfully!")
        self.close()


# Initialize the App
app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()
