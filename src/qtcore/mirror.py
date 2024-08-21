import math

from PyQt5.QtCore import QTimer, QPointF
from PyQt5.QtGui import QPainter, QPolygonF, QColor
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from src.qtcore.polly import Polly


class Mirror(QWidget):
	def __init__(self):
		super().__init__()
		self.polygons = []
		self.rotation_speeds = []
		self.timer = QTimer(self)
		self.timer.timeout.connect(self.update_animation)
		self.timer.start(50)

		self.color_start = QColor(255, 0, 0)  # Красный
		self.color_end = QColor(0, 0, 255)  # Синий

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

	def calculate_color(self, index, total):
		ratio = index / max(1, total - 1)
		red = self.color_start.red() * (1 - ratio) + self.color_end.red() * ratio
		green = self.color_start.green() * (1 - ratio) + self.color_end.green() * ratio
		blue = self.color_start.blue() * (1 - ratio) + self.color_end.blue() * ratio
		return QColor(int(red), int(green), int(blue))

	def add_polygon(self):
		num_polygons = len(self.polygons)
		if num_polygons == 0:
			r = 50
			n = 3
		else:
			last_polygon = self.polygons[-1]
			n = last_polygon.n + 2
			r = last_polygon.r / math.cos(math.pi / n)  # Увеличиваем радиус для нового полигона

		color = self.calculate_color(num_polygons, num_polygons + 1)
		new_polygon = Polly(r=r, n=n, color=color, x=0, y=0)
		new_polygon.start_fade_in()
		self.polygons.append(new_polygon)
		self.rotation_speeds.append(0.5)  # Начальная медленная скорость
		self.update_info()

	def remove_polygon(self):
		if self.polygons:
			polygon = self.polygons.pop()
			polygon.start_fade_out()
			self.rotation_speeds.pop()
			self.update_info()

	def update_info(self):
		self.infoLabel.setText(f"Number of Polygons: {len(self.polygons)}")

	def update_animation(self):
		for i, polygon in enumerate(self.polygons):
			if self.rotation_speeds[i] < 100:  # Максимальная скорость
				self.rotation_speeds[i] += 0.1  # Увеличиваем скорость до максимума
			polygon.rotate(self.rotation_speeds[i])
		self.update()

	def paintEvent(self, event):
		painter = QPainter(self)
		painter.setRenderHint(QPainter.Antialiasing)
		for polygon in self.polygons:
			qpolygon = QPolygonF()
			for vx, vy in polygon.vertices:
				qpolygon.append(QPointF(self.width() / 2 + vx, self.height() / 2 + vy))
			color = QColor(polygon.color.red(), polygon.color.green(), polygon.color.blue(), int(polygon.alpha * 255))
			painter.setPen(color)
			painter.setBrush(color)
			painter.drawPolygon(qpolygon)
