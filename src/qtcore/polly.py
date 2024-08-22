import math

from PyQt5.QtCore import QObject, QPropertyAnimation, pyqtProperty
from PyQt5.QtGui import QColor

from src.core.constants import DYING_SPEED, NORMAL_SPEED, START_SPEED
from src.core.helpers import ease_out_circ, DeadEmit


class Polly(QObject):
	def __init__(self, r, n, color: QColor, x=0, y=0, a=0, parent=None):
		super().__init__(parent)
		self.r = r
		self.n = n
		self.color = color
		self.x = x
		self.y = y
		self.a = a
		self._alpha = 0.0
		self._is_appearing = True
		self.is_dying = False
		self._t = 0.0
		self.vertices = self.calculate_vertices()
		self.rotation_speed = START_SPEED
		self.animation = QPropertyAnimation(self, b"alpha")
		self.animation.setDuration(2000)
		self.animation.setStartValue(0.0)
		self.animation.setEndValue(1.0)
		self.animation.setLoopCount(1)
		self.cry = DeadEmit()

	def calculate_vertices(self):
		vertices = []
		for i in range(self.n):
			angle = 2 * math.pi * i / self.n + math.radians(self.a)
			vx = self.x + self.r * math.cos(angle)
			vy = self.y + self.r * math.sin(angle)
			vertices.append((vx, vy))
		return vertices

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

	def die(self):
		self._is_appearing = False
		self.is_dying = True
		self._t = 0.0

	def rotate(self):
		self.a += self.rotation_speed
		self.vertices = self.calculate_vertices()

	@pyqtProperty(float)
	def alpha(self):
		return self._alpha

	@alpha.setter
	def alpha(self, value):
		self._alpha = value

	def start_fade_in(self):
		self.alpha = 0.0
		self.animation.start()

	def start_fade_out(self):
		self.alpha = 1.0
		self.animation.setDirection(QPropertyAnimation.Backward)
		self.animation.start()
