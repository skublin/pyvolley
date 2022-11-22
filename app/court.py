import sys
from PySide6.QtWidgets import QWidget, QVBoxLayout, QApplication, QLabel
from PySide6.QtGui import QPixmap, QPolygon
from PySide6.QtCore import QPoint
from PySide6.QtCore import Qt as Qt


class TextEditDemo(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # TODO : court MUST be unified and planned for future to have the same measures (click position) for different matches (feature) (!)
        self.setWindowTitle("Court Test")
        
        # create the image
        self.bike_img = QPixmap("app/img/court.jpg")
        self.pixmap_label = QLabel()
        self.pixmap_label.setPixmap(self.bike_img)

        # connect the mouse press event on the image to the img_click function
        self.pixmap_label.mousePressEvent = self.img_click

        # create the polygons
        first_polygon = QPolygon() << QPoint(0, 0) << QPoint(100, 0) << QPoint(100, 100) << QPoint(0, 100)
        second_polygon = QPolygon() << QPoint(200, 200) << QPoint(300, 200) << QPoint(300, 300) << QPoint(200, 300)

        # create a dictionary containing the name of the area, the polygon and the function to be called when
        # the polygon is clicked
        self.clickable_areas = {
            "first": {
                "polygon": first_polygon,
                "func": self.func1
            },
            "second": {
                "polygon": second_polygon,
                "func": self.func2
            }
        }

        layout = QVBoxLayout()
        layout.addWidget(self.pixmap_label)
        self.setLayout(layout)


    def img_click(self, event):
        # get the position of the click
        pos = event.pos()
        print(pos)
        # iterate over all polygons
        for area in self.clickable_areas:
            # if the point is inside one of the polygons, call the function associated with that polygon
            if self.clickable_areas[area]["polygon"].containsPoint(pos, Qt.FillRule.OddEvenFill):
                self.clickable_areas[area]["func"]()
                return
            self.func3()


    # the functions to be called when specific polygons are clicked
    def func1(self):
        print("first polygon clicked!")

    def func2(self):
        print("second polygon clicked!")

    def func3(self):
        print("no polygon was clicked")


if __name__ == "__main__":
    # just testing code
    app = QApplication(sys.argv)
    win = TextEditDemo()
    win.show()

    sys.exit(app.exec())
