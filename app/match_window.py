import sys
from PySide6.QtWidgets import QApplication, QVBoxLayout, QLabel, QWidget


class MatchWindow(QWidget):
    def __init__(self, team_a, team_b):
        super().__init__()

        self.team_a, self.team_b = team_a, team_b

        self.WIDTH, self.HEIGHT = 1200, 800

        self.setFixedWidth(self.WIDTH)
        self.setFixedHeight(self.HEIGHT)
        self.setWindowTitle(f"PyVolley - {self.team_a} vs {self.team_b}")

        layout = QVBoxLayout()
        self.label = QLabel("LAYOUT LABEL")
        layout.addWidget(self.label)
        self.setLayout(layout)
