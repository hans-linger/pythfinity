import math
from math import radians

from PyQt5.QtCore import QPropertyAnimation, QPointF, Qt
from PyQt5.QtGui import QColor, QPolygonF, QBrush, QPen
from PyQt5.QtWidgets import QGraphicsPolygonItem, QGraphicsOpacityEffect, QGraphicsRotation

from src.core.constants import DYING_SPEED, NORMAL_SPEED, START_SPEED
from src.core.helpers import ease_out_circ, DeadEmit


class Polly(QGraphicsPolygonItem):
	def __init__(self, r, n, color: QColor, x=0, y=0, start_angle=0, parent=None):
		super().__init__(parent)
		self.r = r
		self.n = n
		self._color = color
		self.x = x
		self.y = y
		self._a = start_angle
		self._is_appearing = True
		self.is_dying = False
		self._t = 0.0
		self.rotation_speed = START_SPEED
		self.opacity_effect = QGraphicsOpacityEffect()
		self.rotation_effect = QGraphicsRotation()
		self.setGraphicsEffect(self.opacity_effect)
		self.opacity_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
		self.opacity_animation.setDuration(500)
		self.rotation_animation = QPropertyAnimation(self.rotation_effect, b"a")
		self.rotation_animation.setDuration(500)
		self.rotation_animation.valueChanged.connect(self.angle_changed)
		self.cry = DeadEmit()
		self.setBrush(self._color)
		self.setPen(QPen(Qt.NoPen))
		self.draw()
		self.rotation_animation.setStartValue(start_angle)
		self.rotation_animation.setEndValue(start_angle + radians(45))
		self.rotation_animation.start()
		self.start_fade_in()

	@property
	def color(self):
		return self._color

	@color.setter
	def color(self, color: QColor):
		self._color = color
		self.draw()

	def angle_changed(self, value):
		self.a = value
		self.draw()

	@property
	def a(self):
		return self._a

	@a.setter
	def a(self, a):
		self._a = a
		self.draw()

	def calculate_vertices(self):
		vertices = []
		for i in range(self.n):
			angle = 2 * math.pi * i / self.n + self.a
			vx = self.x + self.r * math.cos(angle)
			vy = self.y + self.r * math.sin(angle)
			vertices.append((vx, vy))
		return vertices

	def calc_polygon(self):
		vv = self.calculate_vertices()
		return QPolygonF(QPointF(v[0], v[1]) for v in vv)

	def live(self):
		# rotation speed
		if self.is_dying:
			if self.rotation_speed < DYING_SPEED:
				self._t += 0.1
				self.rotation_speed = ease_out_circ(
					NORMAL_SPEED,
					DYING_SPEED,
					self._t,
				)
			else:
				self.cry.imdead.emit(":(")
		elif self._is_appearing and self._t < 1.0:
			self._t += 0.06
			self.rotation_speed = ease_out_circ(
				START_SPEED,
				NORMAL_SPEED,
				max(0, 1 - self._t),
			)
		else:
			self._is_appearing = False
		# self.rotate()
		self.draw()

	def die(self):
		self._is_appearing = False
		self.is_dying = True
		self._t = 0.0

	# def rotate(self):

	# print("dummy")
	# self.a += self.rotation_speed
	# self.draw()

	def start_fade_in(self):
		self.opacity_animation.setStartValue(0.0)
		self.opacity_animation.setEndValue(1.0)
		self.opacity_animation.start()

	def start_fade_out(self):
		self.opacity_animation.setStartValue(1.0)
		self.opacity_animation.setEndValue(0.0)
		self.opacity_animation.start()

	def draw(self):
		self.setBrush(QBrush(self.color))
		self.setPolygon(self.calc_polygon())
