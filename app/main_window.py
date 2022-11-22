import sys
from PySide6 import QtWidgets
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QComboBox, QTableWidget, QTableWidgetItem

from engine import Engine
from match_window import MatchWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # ENGINE OBJECT
        self.engine = Engine()

        # SETTINGS SECTION
        self.WIDTH, self.HEIGHT = 800, 600

        self.setFixedWidth(self.WIDTH)
        self.setFixedHeight(self.HEIGHT)
        self.setWindowTitle("PyVolley")

        # MATCH WINDOW SECTION
        self.match_window = None

        # MENU BAR SECTION
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("&File")
        self.view_menu = self.menu.addMenu("&View")
        self.help = self.menu.addMenu("&Help")

        # TEAMS SECTION
        self.team_a = None
        self.teams_a_removed = set()
        self.team_b = None
        self.teams_b_removed = set()

        # BUTTONS SECTION
        self.team_a_box_prepare()
        self.team_b_box_prepare()
        self.start_match_button_prepare()

    def team_a_box_prepare(self):
        # TODO : more customization and options for table view of teams, (maybe TableModel?) (feature)
        self.team_a_box = QComboBox(self)
        self.team_a_box.setGeometry(48, 64, 336, 32)
        self.team_a_box.addItems(['TEAM A'] + list(self.engine.cache['data'].Teams.keys()))
        self.team_a_box.activated.connect(self.team_a_box_activation)

    def team_a_box_activation(self):
        selection = self.team_a_box.currentText()

        if selection != 'TEAM A':
            self.team_a = selection
            if len(self.teams_b_removed) > 0:
                self.team_b_box.addItems(self.teams_b_removed)
                self.teams_b_removed.clear()
            self.team_b_box.removeItem(self.team_b_box.findText(selection))
            self.teams_b_removed.add(selection)
        
        if self.team_a_box.itemText(0) == 'TEAM A':
            self.team_a_box.removeItem(0)

        self.show_team_a()
        self.start_match_button_try_enable()

    def show_team_a(self):
        self.data_a = self.engine.get_data_for_table(self.team_a)
        self.table_a = QTableWidget(self.data_a['size'], 4, self)
        self.table_a.setHorizontalHeaderLabels(["Name", "Position", "Age", "Height"])

        self.table_a.setVerticalHeaderLabels(self.data_a['numbers'])

        # column width settings
        header = self.table_a.horizontalHeader()
        header.setDefaultSectionSize(80)
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)

        i = 0
        for player in self.data_a['players']:
            self.table_a.setItem(i, 0, QTableWidgetItem(player.name))
            self.table_a.setItem(i, 1, QTableWidgetItem(player.position))
            self.table_a.setItem(i, 2, QTableWidgetItem(str(player.age)))
            self.table_a.setItem(i, 3, QTableWidgetItem(str(player.height)))
            i += 1

        self.table_a.setGeometry(48, 100, 336, 368)
        self.table_a.show()

    def team_b_box_prepare(self):
        self.team_b_box = QComboBox(self)
        self.team_b_box.setGeometry(416, 64, 336, 32)
        self.team_b_box.addItems(['TEAM B'] + list(self.engine.cache['data'].Teams.keys()))
        self.team_b_box.activated.connect(self.team_b_box_activation)

    def team_b_box_activation(self):
        selection = self.team_b_box.currentText()

        if selection != 'TEAM B':
            self.team_b = selection
            if len(self.teams_a_removed) > 0:
                self.team_a_box.addItems(self.teams_a_removed)
                self.teams_a_removed.clear()
            self.team_a_box.removeItem(self.team_a_box.findText(selection))
            self.teams_a_removed.add(selection)
        
        if self.team_b_box.itemText(0) == 'TEAM B':
            self.team_b_box.removeItem(0)

        self.show_team_b()
        self.start_match_button_try_enable()

    def show_team_b(self):
        self.data_b = self.engine.get_data_for_table(self.team_b)
        self.table_b = QTableWidget(self.data_b['size'], 4, self)
        self.table_b.setHorizontalHeaderLabels(["Name", "Position", "Age", "Height"])

        self.table_b.setVerticalHeaderLabels(self.data_b['numbers'])

        # column width settings
        header = self.table_b.horizontalHeader()
        header.setDefaultSectionSize(80)
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)

        i = 0
        for player in self.data_b['players']:
            self.table_b.setItem(i, 0, QTableWidgetItem(player.name))
            self.table_b.setItem(i, 1, QTableWidgetItem(player.position))
            self.table_b.setItem(i, 2, QTableWidgetItem(str(player.age)))
            self.table_b.setItem(i, 3, QTableWidgetItem(str(player.height)))
            i += 1

        self.table_b.setGeometry(416, 100, 336, 368)
        self.table_b.show()

    def start_match_button_prepare(self):
        self.start_match_button = QPushButton("Start Match", self)
        self.start_match_button.setGeometry(640, 504, 128, 64)    # x, y, width, height
        self.start_match_button.clicked.connect(self.start_match_button_clicked)
        self.start_match_button.setEnabled(False)    # let user use this button only after teams selection (!)

    def start_match_button_clicked(self, checked):
        if self.match_window is None:
            self.match_window = MatchWindow(self.team_a, self.team_b)
            self.match_window.show()
        else:
            self.match_window.close()
            self.match_window = None

    def start_match_button_try_enable(self):
        if self.team_a is not None and self.team_b is not None:
            self.start_match_button.setEnabled(True)


if __name__ == "__main__":
    app = QApplication()

    main = MainWindow()
    main.show()

    sys.exit(app.exec())
