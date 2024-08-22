import math

from PyQt5.QtCore import QPropertyAnimation, QPointF
from PyQt5.QtGui import QColor, QPolygonF, QBrush
from PyQt5.QtWidgets import QGraphicsPolygonItem, QGraphicsOpacityEffect

from src.core.constants import DYING_SPEED, NORMAL_SPEED, START_SPEED
from src.core.helpers import ease_out_circ, DeadEmit


class Polly(QGraphicsPolygonItem):
	def __init__(self, r, n, color: QColor, x=0, y=0, a=0, parent=None):
		super().__init__(parent)
		self.r = r
		self.n = n
		self._color = color
		self.x = x
		self.y = y
		self.a = a
		self._is_appearing = True
		self.is_dying = False
		self._t = 0.0
		self.vertices = self.calculate_vertices()
		self.rotation_speed = START_SPEED
		self.setOpacity(1)
		self.opacity_effect = QGraphicsOpacityEffect()
		self.setGraphicsEffect(self.opacity_effect)
		self.draw()
		self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
		self.animation.setDuration(400)
		self.cry = DeadEmit()

	@property
	def color(self):
		return self._color

	@color.setter
	def color(self, color: QColor):
		self._color = color
		self.draw()

	def calculate_vertices(self):
		vertices = []
		for i in range(self.n):
			angle = 2 * math.pi * i / self.n + math.radians(self.a)
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
		self.rotate()
		self.draw()

	def die(self):
		self._is_appearing = False
		self.is_dying = True
		self._t = 0.0

	def rotate(self):
		self.a += self.rotation_speed
		self.vertices = self.calculate_vertices()
		self.draw()

	def start_fade_in(self):
		self.animation.setStartValue(0.0)
		self.animation.setEndValue(1.0)
		self.animation.start()

	def start_fade_out(self):
		self.animation.setStartValue(1.0)
		self.animation.setEndValue(0.0)
		self.animation.start()

	def draw(self):
		self.setBrush(QBrush(self.color))
		self.setPolygon(self.calc_polygon())
