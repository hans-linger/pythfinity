import math

from PyQt5.QtCore import QObject, QPropertyAnimation, pyqtProperty


class Polly(QObject):
	def __init__(self, r, n, color, x=0, y=0, a=0, parent=None):
		super().__init__(parent)
		self.r = r
		self.n = n
		self.color = color
		self.x = x
		self.y = y
		self.a = a
		self._alpha = 1.0  # Полная непрозрачность
		self.vertices = self.calculate_vertices()
		self.rotation_speed = 10 - 2 * n
		self.animation = QPropertyAnimation(self, b"alpha")
		self.animation.setDuration(1000)
		self.animation.setStartValue(0.0)
		self.animation.setEndValue(1.0)
		self.animation.setLoopCount(1)

	def calculate_vertices(self):
		vertices = []
		for i in range(self.n):
			angle = 2 * math.pi * i / self.n + math.radians(self.a)
			vx = self.x + self.r * math.cos(angle)
			vy = self.y + self.r * math.sin(angle)
			vertices.append((vx, vy))
		return vertices

	def rotate(self, angle):
		self.a += angle
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
