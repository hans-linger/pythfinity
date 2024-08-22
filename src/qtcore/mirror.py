import math

from PyQt5.QtCore import QTimer, QPointF
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QGraphicsView, QGraphicsScene, QHBoxLayout

from src.core.constants import GRAPHICS_SIZE
from src.core.helpers import calc_colors
from src.qtcore.polly import Polly


class Mirror(QWidget):
	def __init__(self):
		super().__init__()
		self.view = QGraphicsView()
		self.view.setRenderHint(QPainter.Antialiasing)
		self.view.centerOn(QPointF(GRAPHICS_SIZE / 2, GRAPHICS_SIZE / 2))
		self.scene = QGraphicsScene()
		self.scene.setSceneRect(0, 0, GRAPHICS_SIZE, GRAPHICS_SIZE)

		self.view.setScene(self.scene)
		self.color_start = QColor()
		self.color_start.setNamedColor("#f0a040")
		self.color_end = QColor()
		self.color_end.setNamedColor("#445663")

		self.polygons = []
		self.colors = []
		self.timer = QTimer(self)
		self.timer.timeout.connect(self.update_animation)
		self.timer.start(25)

		self.init_ui()
		self.add_polygon()
		self.add_polygon()
		self.add_polygon()

	def init_ui(self):
		layout = QVBoxLayout()
		layout.setContentsMargins(0, 0, 0, 0)
		buttons_layout = QHBoxLayout()
		buttons_layout.setContentsMargins(10, 10, 10, 10)

		self.addButton = QPushButton("Create Polly", self)
		self.addButton.clicked.connect(self.add_polygon)
		buttons_layout.addWidget(self.addButton)

		self.removeButton = QPushButton("Kill Polly", self)
		self.removeButton.clicked.connect(self.kill_polly)
		buttons_layout.addWidget(self.removeButton)

		layout.addLayout(buttons_layout)

		self.infoLabel = QLabel(self)
		layout.addWidget(self.infoLabel)

		layout.addWidget(self.view)
		self.setLayout(layout)
		self.update_info()

	def add_polygon(self):
		num_polygons = len(self.polygons)
		last_polygon = None
		if num_polygons == 0:
			r = 50
			n = 3
			a = 0
		else:
			last_polygon = self.polygons[0]
			n = last_polygon.n + 2
			r = last_polygon.r / math.cos(math.pi / n)
			a = last_polygon.a + math.pi / 2

		new_polygon = Polly(r=r, n=n, color=self.color_start, a=a, x=GRAPHICS_SIZE / 2, y=GRAPHICS_SIZE / 2)
		new_polygon.cry.imdead.connect(lambda: self.polly_died(new_polygon))
		self.polygons.insert(0, new_polygon)
		self.update_colors()
		self.scene.addItem(new_polygon)
		if last_polygon:
			new_polygon.stackBefore(last_polygon)
		new_polygon.start_fade_in()
		self.update_info()

	def update_colors(self):
		self.colors = calc_colors(self.color_start, self.color_end, len(self.polygons))
		for i in range(len(self.polygons)):
			self.polygons[i].color = self.colors[i]

	def kill_polly(self):
		if self.polygons:
			lively_pollies = [x for x in self.polygons if not x.is_dying]
			if len(lively_pollies) > 1:
				polygon = lively_pollies[0]
				if polygon:
					self.update_colors()
					polygon.start_fade_out()
					polygon.die()
					self.update_info()

	def polly_died(self, dead_polly):
		if dead_polly in self.polygons:
			self.polygons.pop(self.polygons.index(dead_polly))
			self.update_info()

	def update_info(self):
		self.infoLabel.setText(f"Pollies: {len(self.polygons)}")

	def update_animation(self):
		for polygon in self.polygons:
			polygon.live()
