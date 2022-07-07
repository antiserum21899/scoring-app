from asyncio import events
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from UI_Main import Ui_MainWindow
import sys

class MainWindow():
    database = {
        'participants': {}
    }

    def __init__(self):
        self.main_win = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.main_win)

        # finds the home page and sets it to current page.
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_home)

        # connects buttons to functions to switch between pages
        self.ui.entry_form_btn.clicked.connect(self.show_entry_form)
        self.ui.events_btn.clicked.connect(self.show_events_page)
        self.ui.leaderboard_btn.clicked.connect(self.get_participants)

        self.ui.team_events_btn.clicked.connect(self.show_team_events)
        self.ui.individual_events_btn.clicked.connect(self.show_individual_events)

        self.ui.leaderboards_teams_btn.clicked.connect(self.show_team_leaderboard)
        self.ui.leaderboards_individuals_btn.clicked.connect(self.show_individual_leaderboard)

        # connects button to save function to save input data
        self.ui.entry_form_save_btn.clicked.connect(self.save_entry_form)

        # connects selected option in combobox to its respective page
        self.ui.team_events_cb.activated.connect(self.show_team_forms)
        self.ui.individual_events_cb.activated.connect(self.show_individual_forms)

        self.checkboxes_individuals = [
            self.ui.event_math,
            self.ui.event_chess,
            self.ui.event_100m_sprint,
            self.ui.event_badminton,
            self.ui.event_javelin,
            self.ui.event_long_jump,
            self.ui.event_shot_put,
            self.ui.event_tennis,
        ]

        self.checkboxes_teams = [
            self.ui.event_relay_sprint,
            self.ui.event_football,
            self.ui.event_rounders,
            self.ui.event_basketball,
            self.ui.event_indoor_hockey,
            self.ui.event_escape_room,
            self.ui.event_indoor_cricket,
            self.ui.event_bridge_building,
        ]

        self.team_members = [
            self.ui.member_1,
            self.ui.member_2,
            self.ui.member_3,
            self.ui.member_4,
            self.ui.member_5
        ]

        self.ranks_singles = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
        self.ranks_teams = [1, 2, 3, 4]

        self.spin_boxes_relay_sprint = [
            self.ui.relay_sprint_spin_1,
            self.ui.relay_sprint_spin_2,
            self.ui.relay_sprint_spin_3,
            self.ui.relay_sprint_spin_4,
            self.ui.football_spin_1,
            self.ui.football_spin_2,
            self.ui.football_spin_3,
            self.ui.football_spin_4,
            self.ui.rounders_spin_1,
            self.ui.rounders_spin_2,
            self.ui.rounders_spin_3,
            self.ui.rounders_spin_4,
            self.ui.basketball_spin_1,
            self.ui.basketball_spin_2,
            self.ui.basketball_spin_3,
            self.ui.basketball_spin_4,
        ]

    def show(self):
        self.main_win.show()

    def show_entry_form(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_entry_form)

    def show_events_page(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_events)
    def show_leaderboard(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_leaderboards)

    def show_team_events(self):
        self.ui.stacked_widget_event_forms.setCurrentWidget(self.ui.team_forms)

    def show_individual_events(self):
        self.ui.stacked_widget_event_forms.setCurrentWidget(self.ui.Individual_forms)

    def show_team_leaderboard(self):
        self.ui.stacked_widget_leaderboards.setCurrentWidget(self.ui.leaderboard_teams)
    
    def show_individual_leaderboard(self):
        self.ui.stacked_widget_leaderboards.setCurrentWidget(self.ui.leaderboard_individuals)

    # function to select which form appears based on current text in combo box
    def show_team_forms(self):
        if self.ui.team_events_cb.currentText() == "Relay Sprint":
            self.ui.stacked_widget_team_forms.setCurrentWidget(self.ui.form_relay_sprint)
        elif self.ui.team_events_cb.currentText() == "Football":
            self.ui.stacked_widget_team_forms.setCurrentWidget(self.ui.form_football)
        elif self.ui.team_events_cb.currentText() == "Rounders":
            self.ui.stacked_widget_team_forms.setCurrentWidget(self.ui.form_rounders)
        elif self.ui.team_events_cb.currentText() == "Basketball":
            self.ui.stacked_widget_team_forms.setCurrentWidget(self.ui.form_basketball)
        elif self.ui.team_events_cb.currentText() == "Indoor Cricket":
            self.ui.stacked_widget_team_forms.setCurrentWidget(self.ui.form_indoor_cricket)
        elif self.ui.team_events_cb.currentText() == "Indoor Hockey":
            self.ui.stacked_widget_team_forms.setCurrentWidget(self.ui.form_indoor_hockey)
        elif self.ui.team_events_cb.currentText() == "Escape Room":
            self.ui.stacked_widget_team_forms.setCurrentWidget(self.ui.form_escape_room)
        elif self.ui.team_events_cb.currentText() == "Bridge Building":
            self.ui.stacked_widget_team_forms.setCurrentWidget(self.ui.form_bridge_building)

    # function to select which form appears based on current text in combo box
    def show_individual_forms(self):
        if self.ui.individual_events_cb.currentText() == "Math":
            self.ui.stacked_widget_individual_forms.setCurrentWidget(self.ui.form_math)
        elif self.ui.individual_events_cb.currentText() == "Chess":
            self.ui.stacked_widget_individual_forms.setCurrentWidget(self.ui.form_chess)
        elif self.ui.individual_events_cb.currentText() == "100m Sprint":
            self.ui.stacked_widget_individual_forms.setCurrentWidget(self.ui.form_100m_sprint)
        elif self.ui.individual_events_cb.currentText() == "Javelin":
            self.ui.stacked_widget_individual_forms.setCurrentWidget(self.ui.form_javelin)
        elif self.ui.individual_events_cb.currentText() == "Tennis":
            self.ui.stacked_widget_individual_forms.setCurrentWidget(self.ui.form_tennis)
        elif self.ui.individual_events_cb.currentText() == "Badminton":
            self.ui.stacked_widget_individual_forms.setCurrentWidget(self.ui.form_badminton)
        elif self.ui.individual_events_cb.currentText() == "Shot Put":
            self.ui.stacked_widget_individual_forms.setCurrentWidget(self.ui.form_shot_put)
        elif self.ui.individual_events_cb.currentText() == "Long Jump":
            self.ui.stacked_widget_individual_forms.setCurrentWidget(self.ui.form_long_jump)

    # function to save data to database dictionary
    def save_entry_form(self):
        keys = self.database['participants'].keys()
        self.database['participants'][len(keys) + 1] = {
            'name': self.ui.name.text(),
            'type': self.ui.team_or_individual.currentText(),
            'events': self.check_events(),
            'members': self.check_members(),
        }
 
        print(self.database)

        # creates popup message box when save button is clicked
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Information Box")
        msg.setText("You entry has been saved.")
        init_msg = msg.exec_()

    def clear_data(self):
        pass

    # function to iterate over events and append them to an array
    def check_events(self):
        events = []
        if self.ui.team_or_individual.currentText() == "Individual":
            # iterates over array of checkbox objects
            for i in self.checkboxes_individuals:
                # checks state of checkbox for checked state
                if i.checkState() == 2:  
                    events.append([i.text()])
            return events
        elif self.ui.team_or_individual.currentText() == "Team":
            for i in self.checkboxes_teams:
                if i.checkState() == 2:
                    events.append([i.text()])
            return events

    # function to iterate over members and append input data into array
    def check_members(self):
        members = []
        if self.ui.team_or_individual.currentText() == "Team":
            for i in self.team_members:
                members.append([i.text()])
            return members
        else:
            return None

    def get_participants(self):
        teams = []
        for key in self.database['participants'].keys():
            if self.database['participants'][key]['type'] == "Team":
                teams.append(self.database['participants'][key]['name'])
        return teams



# runs the main application            
def main():
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

