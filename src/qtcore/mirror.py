import math

from PyQt5.QtCore import QTimer, QPointF
from PyQt5.QtGui import QPainter, QPolygonF, QColor
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QGraphicsView, QGraphicsScene

from src.core.helpers import calc_colors
from src.qtcore.polly import Polly


class Mirror(QWidget):
	def __init__(self):
		super().__init__()
		self.view = QGraphicsView()
		self.view.setRenderHint(QPainter.Antialiasing)
		self.scene = QGraphicsScene()


		self.view.setScene(self.scene)
		self.color_start = QColor()
		self.color_start.setNamedColor("#ff00a0")
		self.color_end = QColor()
		self.color_end.setNamedColor("#b0ff00")

		self.polygons = []
		self.colors = []
		self.timer = QTimer(self)
		self.timer.timeout.connect(self.update_animation)
		self.timer.start(25)

		self.init_ui()
		self.add_polygon()

	# self.add_polygon()
	# self.add_polygon()

	def init_ui(self):
		layout = QVBoxLayout()

		self.addButton = QPushButton("Add Polly", self)
		self.addButton.clicked.connect(self.add_polygon)
		layout.addWidget(self.addButton)

		self.removeButton = QPushButton("Remove Polly", self)
		self.removeButton.clicked.connect(self.remove_polygon)
		layout.addWidget(self.removeButton)

		self.infoLabel = QLabel(self)
		layout.addWidget(self.infoLabel)

		layout.addWidget(self.view)
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
		new_polygon.cry.imdead.connect(lambda: self.polygon_died(new_polygon))
		self.polygons.insert(0, new_polygon)
		self.scene.addItem(new_polygon)
		self.polygons.append(new_polygon)
		self.update_colors()
		new_polygon.start_fade_in()
		self.update_info()


	def update_colors(self):
		self.colors = calc_colors(self.color_start, self.color_end, len(self.polygons))
		for i in range(len(self.polygons)):
			self.polygons[i].color = self.colors[i]

	def remove_polygon(self):
		if self.polygons:
			lively_pollies = [x for x in self.polygons if not x.is_dying]
			if len(lively_pollies) > 1:
				polygon = lively_pollies[0]
				if polygon:
					print("Mark to die: " + str(polygon.n))
					self.update_colors()
					polygon.start_fade_out()
					polygon.die()
					self.update_info()


	def polygon_died(self, dead_polly):
		print("DIED " + str(dead_polly.n))
		if dead_polly in self.polygons:
			self.polygons.pop(self.polygons.index(dead_polly))
			self.update_info()

	def update_info(self):
		self.infoLabel.setText(f"Number of Polygons: {len(self.polygons)}")

	def update_animation(self):
		for i, polygon in enumerate(self.polygons):
			polygon.live()
		self.update()

	def paintEventq(self, event):
		painter = QPainter(self)
		painter.setRenderHint(QPainter.Antialiasing)
		for polygon in self.polygons:
			qpolygon = QPolygonF()
			for vx, vy in polygon.vertices:
				qpolygon.append(QPointF(self.width() / 2 + vx, self.height() / 2 + vy))
			polygon.color.setAlphaF(polygon.opacity())
			painter.setPen(polygon.color)
			painter.setBrush(polygon.color)
			painter.drawPolygon(qpolygon)
			circle_color = polygon.color
			circle_color.setAlphaF(0.2)
			painter.setBrush(circle_color)
			painter.drawEllipse(QPointF(self.width() / 2, self.width() / 2), polygon.r, polygon.r)
		painter.end()
