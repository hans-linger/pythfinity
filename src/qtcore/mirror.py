import math

from PyQt5.QtCore import QTimer, QPointF
from PyQt5.QtGui import QPainter, QPolygonF, QColor
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel

from src.core.helpers import calc_colors
from src.qtcore.polly import Polly


class Mirror(QWidget):
    def __init__(self):
        super().__init__()
        self.color_start = QColor()
        self.color_start.setNamedColor("#ff00a0")
        self.color_end = QColor()
        self.color_end.setNamedColor("#b0ff00")

        self.polygons = []
        self.colors = []
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_animation)
        self.timer.start(50)

        self.initUI()
        self.add_polygon()  # Создаем первый треугольник

    def initUI(self):
        layout = QVBoxLayout()

        self.addButton = QPushButton("Add Polly", self)
        self.addButton.clicked.connect(self.add_polygon)
        layout.addWidget(self.addButton)

        self.removeButton = QPushButton("Remove Polly", self)
        self.removeButton.clicked.connect(self.remove_polygon)
        layout.addWidget(self.removeButton)

        self.infoLabel = QLabel(self)
        layout.addWidget(self.infoLabel)

        self.setLayout(layout)
        self.update_info()

    def add_polygon(self):
        num_polygons = len(self.polygons)
        if num_polygons == 0:
            r = 50
            n = 3
        else:
            last_polygon = self.polygons[0]
            n = last_polygon.n + 2
            r = last_polygon.r / math.cos(math.pi / n)

        new_polygon = Polly(r=r, n=n, color=self.color_start, x=0, y=0)
        new_polygon.start_fade_in()
        self.polygons.insert(0, new_polygon)
        self.update_colors()
        self.update_info()

    def update_colors(self):
        self.colors = calc_colors(self.color_start, self.color_end, len(self.polygons))
        for i in range(len(self.polygons)):
            self.polygons[i].color = self.colors[i]

    def remove_polygon(self):
        if self.polygons:
            polygon = self.polygons.pop(0)
            polygon.start_fade_out()
            self.update_info()

    def update_info(self):
        self.infoLabel.setText(f"Number of Polygons: {len(self.polygons)}")

    def update_animation(self):
        for i, polygon in enumerate(self.polygons):
            polygon.live()
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        for polygon in self.polygons:
            qpolygon = QPolygonF()
            for vx, vy in polygon.vertices:
                qpolygon.append(QPointF(self.width() / 2 + vx, self.height() / 2 + vy))
            polygon.color.setAlphaF(polygon.alpha)
            painter.setPen(polygon.color)
            painter.setBrush(polygon.color)
            painter.drawPolygon(qpolygon)
        painter.end()
