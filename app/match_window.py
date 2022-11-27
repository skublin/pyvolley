import sys
from PySide6.QtCore import Qt, QRect, QPoint
from PySide6.QtGui import QImage, QPixmap
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
        self.court_label = QLabel(alignment=Qt.AlignCenter)
        layout.addWidget(self.court_label)
        self.setLayout(layout)

        self.court_image = QImage()
        self.court_image.load("C:\\Users\\szymo\\OneDrive\\Pulpit\\python\\volleyball\\app\\img\\court.jpg")
        print(f"court img size : {self.court_image.size()}")
        self.court_pixmap = QPixmap()
        self.court_pixmap.convertFromImage(self.court_image)
        self.court_label.setPixmap(self.court_pixmap)

        self.court = self.court_label.rect()
        new_top_left = QPoint(self.WIDTH / 2 - 212, self.HEIGHT / 2 - 258)
        self.court.setTopLeft(new_top_left)
        new_bottom_right = QPoint(self.WIDTH / 2 + 212, self.HEIGHT / 2 + 258)
        self.court.setBottomRight(new_bottom_right)
        print(self.court.getCoords())

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            # handle the left-button press in here
            print("mousePressEvent LEFT")

        elif e.button() == Qt.MiddleButton:
            # handle the middle-button press in here.
            print("mousePressEvent MIDDLE")

        elif e.button() == Qt.RightButton:
            # handle the right-button press in here.
            print("mousePressEvent RIGHT")

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton:
            print("mouseReleaseEvent LEFT")

        elif e.button() == Qt.MiddleButton:
            print("mouseReleaseEvent MIDDLE")

        elif e.button() == Qt.RightButton:
            print("mouseReleaseEvent RIGHT")

    def mouseDoubleClickEvent(self, e):
        if e.button() == Qt.LeftButton:
            print(f"(!) mouseDoubleClickEvent LEFT, position: {e.pos()} or {e.globalPos()}")
            if self.court.contains(e.pos()):
                print(f"INSIDE, topLeft: {self.court.topLeft()}")

        elif e.button() == Qt.MiddleButton:
            print("mouseDoubleClickEvent MIDDLE")

        elif e.button() == Qt.RightButton:
            print("mouseDoubleClickEvent RIGHT")