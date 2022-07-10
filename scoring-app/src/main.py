from select import select
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem
from MainUI import Ui_MainWindow

import sqlite3
import sys

connection = sqlite3.connect("participants.db")
c = connection.cursor()

c.execute("""CREATE TABLE if not exists events_table(
    event_name TEXT,
    event_type TEXT
)""")

c.execute("""CREATE TABLE if not exists singles_table(
    individual_name TEXT,
    event_1 TEXT,
    event_2 TEXT,
    event_3 TEXT,
    event_4 TEXT,
    event_5 TEXT
)""")

c.execute("""CREATE TABLE if not exists teams_table(
    team_name TEXT,
    event_1 TEXT,
    event_2 TEXT,
    event_3 TEXT,
    event_4 TEXT,
    event_5 TEXT
)""")

c.execute("""CREATE TABLE if not exists team_members_table(
    member_1 TEXT,
    member_2 TEXT,
    member_3 TEXT,
    member_4 TEXT,
    member_5 TEXT,
    team_name TEXT
)""")

c.execute("""CREATE TABLE if not exists singles_scores_table(
    individual TEXT,
    event_name TEXT,
    position INTEGER,
    score INTEGER
)""")

c.execute("""CREATE TABLE if not exists team_scores_table(
    team TEXT,
    event_name TEXT,
    position INTEGER,
    score INTEGER
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

        # connects save button to function to save participant data to db
        self.ui.participant_entry_form_save_btn.clicked.connect(self.save_participant)

        # connects function to combobox to change event types
        self.ui.team_or_individual.currentIndexChanged.connect(self.swap_events)

        self.team_members = [
            self.ui.member_1,
            self.ui.member_2,
            self.ui.member_3,
            self.ui.member_4,
            self.ui.member_5,
        ]

        self.event_cbs = [
            self.ui.event_1_cb,
            self.ui.event_2_cb,
            self.ui.event_3_cb,
            self.ui.event_4_cb,
            self.ui.event_5_cb,
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

    # function to save event data to database
    def save_events(self):
        row_count = self.ui.events_tableWidget.rowCount()
        column_count = self.ui.events_tableWidget.columnCount()
        # holds data from table
        event_data = []
        events = []
        # iterates over the rows and columns and appends each item from each cell into array
        for row in range(row_count): 
            for column in range(column_count):
                table_item = self.ui.events_tableWidget.item(row, column)
                event_data.append(table_item.text())
        # iterates over events_data array and appends every event name and event type pair as a tuple in events array
        for i in range(0, len(event_data), 2):
            events.append(tuple(event_data[i:i + 2]))
        print(events)
        connection = sqlite3.connect("participants.db")
        c = connection.cursor()
        c.executemany("INSERT INTO events_table VALUES (?, ?)", events)  
        connection.commit()
        connection.close()

        self.show_saved_message("events")

    # function to save participant data to database
    def save_participant(self):
        connection = sqlite3.connect("participants.db")
        c = connection.cursor()
        selected_events = []
        if self.ui.team_or_individual.currentText() == "Team":
            team_name = self.ui.name.text()
            team_members = []
            #converted_members = []
            selected_events.append(team_name)
            # loops over array of event comboboxs and appends text of each to events array
            for cbs in self.event_cbs:
                selected_events.append(cbs.currentText())

            converted_events = [self.convert_array_to_tuple(selected_events)]
            # loops over array of member line edits and appends text of each to team_members array
            for member in self.team_members:
                team_members.append(member.text())

            team_members.append(team_name)
            print(team_members)
            converted_members = [self.convert_array_to_tuple(team_members)]
            print(converted_members)

            c.executemany("INSERT INTO teams_table VALUES (?, ?, ?, ?, ?, ?)", converted_events)
            c.executemany("INSERT INTO team_members_table VALUES (?, ?, ?, ?, ?, ?)", converted_members)
            connection.commit()
            connection.close()
            self.show_saved_message("team")
        
        elif self.ui.team_or_individual.currentText() == "Individual":
            individual_name = self.ui.name.text()
            selected_events.append(individual_name)
            # loops over array of event comboboxs and appends text of each to events array
            for cbs in self.event_cbs:
                selected_events.append(cbs.currentText())

            print(selected_events)
            converted_events = [self.convert_array_to_tuple(selected_events)]
            print(converted_events)

            c.executemany("INSERT INTO singles_table VALUES (?, ?, ?, ?, ?, ?)", converted_events)
            connection.commit()
            connection.close()
            self.show_saved_message("participant")

    # function to swap between team or individual events
    def swap_events(self):
        events = []
        connection = sqlite3.connect("participants.db")
        c = connection.cursor()
        # loops over event comboboxes and clears all data
        for cb in self.event_cbs:
            cb.clear()

        if self.ui.team_or_individual.currentText() == "Team":
            c.execute("SELECT event_name FROM events_table WHERE event_type='Team'")
            event_names = c.fetchall() 
            # loops over event_names and appends the event to events array
            for event in event_names:
                events.append(event[0])
            # loops over comboboxes and adds the events to all comboboxes
            for cbs in self.event_cbs:
                cbs.addItems(events)

            connection.commit()
            connection.close()

        elif self.ui.team_or_individual.currentText() == "Individual":
            c.execute("SELECT event_name FROM events_table WHERE event_type='Individual'")
            event_names = c.fetchall()
            # loops over event_names and appends the event to events array
            for event in event_names:
                events.append(event[0])
            # loops over comboboxes and adds the events to all comboboxes  
            for cbs in self.event_cbs:
                cbs.addItems(events)

            connection.commit()
            connection.close()

    def clear_data(self):
        pass

    def convert_array_to_tuple(self, array):
        return tuple(i for i in array)

    # creates popup message when save button is clicked
    def show_saved_message(self, text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Information Box")
        msg.setText("Your " + text + " have been sucessfully saved to the database.")
        init_msg = msg.exec_()

    def show_error_message(self, text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Warning!")
        msg.setText(text)
        init_msg = msg.exec_()

# runs the main application            
def main():
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

