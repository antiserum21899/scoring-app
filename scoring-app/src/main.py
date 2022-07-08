from asyncio import events
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem
from MainUI import Ui_MainWindow

import sqlite3
import sys

connection = sqlite3.connect("participants.db")
c = connection.cursor()

c.execute("""CREATE TABLE if not exists type_table(
    type_name TEXT
)""")

c.execute("""CREATE TABLE if not exists events_table(
    event_name TEXT,
    event_type TEXT,
    FOREIGN KEY(event_type) REFERENCES type_table(type_name)
)""")

c.execute("""CREATE TABLE if not exists singles_table(
    individual_name TEXT,
    event_1 TEXT,
    event_2 TEXT,
    event_3 TEXT,
    event_4 TEXT,
    event_5 TEXT,
    FOREIGN KEY(event_1) REFERENCES events_table(event_name),
    FOREIGN KEY(event_2) REFERENCES events_table(event_name),
    FOREIGN KEY(event_3) REFERENCES events_table(event_name),
    FOREIGN KEY(event_4) REFERENCES events_table(event_name),
    FOREIGN KEY(event_5) REFERENCES events_table(event_name)
)""")

c.execute("""CREATE TABLE if not exists teams_table(
    team_name TEXT,
    event_1 TEXT,
    event_2 TEXT,
    event_3 TEXT,
    event_4 TEXT,
    event_5 TEXT,
    FOREIGN KEY(event_1) REFERENCES events_table(event_name),
    FOREIGN KEY(event_2) REFERENCES events_table(event_name),
    FOREIGN KEY(event_3) REFERENCES events_table(event_name),
    FOREIGN KEY(event_4) REFERENCES events_table(event_name),
    FOREIGN KEY(event_5) REFERENCES events_table(event_name)
)""")

c.execute("""CREATE TABLE if not exists team_members_table(
    member_1 TEXT,
    member_2 TEXT,
    member_3 TEXT,
    member_4 TEXT,
    member_5 TEXT,
    team_name TEXT,
    FOREIGN KEY(team_name) REFERENCES teams_table(team_name)
)""")

c.execute("""CREATE TABLE if not exists singles_scores_table(
    individual TEXT,
    event_name TEXT,
    position INTEGER,
    score INTEGER,
    FOREIGN KEY(individual) REFERENCES singles_table(individual_name),
    FOREIGN KEY(event_name) REFERENCES events_table(event_name)
)""")

c.execute("""CREATE TABLE if not exists team_scores_table(
    team TEXT,
    event_name TEXT,
    position INTEGER,
    score INTEGER,
    FOREIGN KEY(team) REFERENCES teams_table(team_name),
    FOREIGN KEY(event_name) REFERENCES events_table(event_name)
)""")

connection.commit()
connection.close()

class MainWindow():

    def __init__(self):
        self.main_win = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.main_win)

        # finds the home page and sets it to current page.
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)

        # connects buttons to functions to switch between pages
        self.ui.add_events_form_btn.clicked.connect(self.show_add_events_form)
        self.ui.add_participants_form_btn.clicked.connect(self.show_add_participants_form)
        self.ui.add_events_scores_btn.clicked.connect(self.show_event_scores)
        self.ui.leaderboard_btn.clicked.connect(self.show_leaderboard)

        self.ui.leaderboards_teams_btn.clicked.connect(self.show_team_leaderboard)
        self.ui.leaderboards_individuals_btn.clicked.connect(self.show_individual_leaderboard)

        # connects buttons on events page
        self.ui.add_events_btn.clicked.connect(self.add_events)
        self.ui.save_events_btn.clicked.connect(self.save_events)

        self.team_members = [
            self.ui.member_1,
            self.ui.member_2,
            self.ui.member_3,
            self.ui.member_4,
            self.ui.member_5
        ]

    def show(self):
        self.main_win.show()

    def show_add_events_form(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_add_events_form)

    def show_add_participants_form(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_entry_form)

    def show_event_scores(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_events)

    def show_leaderboard(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_leaderboards)

    def show_team_leaderboard(self):
        self.ui.stacked_widget_leaderboards.setCurrentWidget(self.ui.leaderboard_teams)
    
    def show_individual_leaderboard(self):
        self.ui.stacked_widget_leaderboards.setCurrentWidget(self.ui.leaderboard_individuals)

    def add_events(self):
        row = self.ui.events_tableWidget.rowCount() # gets total amount of rows
        self.ui.events_tableWidget.setRowCount(row + 1) # increments row count by 1

        event_name = self.ui.add_events_lineEdit.text()
        event_type = self.ui.event_type_cb.currentText()

        self.ui.events_tableWidget.setItem(row, 0, QTableWidgetItem(event_name))
        self.ui.events_tableWidget.setItem(row, 1, QTableWidgetItem(event_type))

        self.ui.add_events_lineEdit.setText("")

    # function to save data to database
    def save_events(self):
        rowCount = self.ui.events_tableWidget.rowCount()
        columnCount = self.ui.events_tableWidget.columnCount()
        event_data = []
        events = []

        for row in range(rowCount):
            for column in range(columnCount):
                table_item = self.ui.events_tableWidget.item(row, column)
                event_data.append(table_item.text())

        for i in range(0, len(event_data), 2):
            events.append(tuple(event_data[i:i + 2]))

        connection = sqlite3.connect("participants.db")
        c = connection.cursor()
        c.executemany("INSERT INTO events_table VALUES (?, ?)", events)  
        connection.commit()
        connection.close()

        self.show_saved_message("events")

    def clear_data(self):
        pass

    # creates popup message when save button is clicked
    def show_saved_message(self, text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Information Box")
        msg.setText("Your " + text + " have been saved.")
        init_msg = msg.exec_()

# runs the main application            
def main():
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

