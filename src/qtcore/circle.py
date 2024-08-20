from random import randint

from PyQt5.QtCore import QRect, QBasicTimer, Qt
from PyQt5.QtGui import QPainter, QBrush, QColor, QPen
from PyQt5.QtWidgets import QWidget

from src.core.constants import GRAPHICS_SIZE, easeOutBounce, easeOutCirc

MIN_SIZE = 20
MAX_SIZE = 250


class Circle(QWidget):
	def __init__(self):
		super(Circle, self).__init__()
		self.growing = True
		self.counter = MIN_SIZE
		self.tm = QBasicTimer()
		self.painter = QPainter(self)
		self.painter.setRenderHint(QPainter.Antialiasing)
		self.brush = QBrush(QColor(255, 2, 2))
		self.pen = QPen(Qt.NoPen)
		self.painter.setBrush(self.brush)
		self.painter.setPen(self.pen)
		self.tm.start(3, self)

	def live(self):
		if self.counter == MAX_SIZE and self.growing:
			self.growing = False

		elif self.counter == MIN_SIZE and not self.growing:
			self.growing = True

		self.counter += 1 if self.growing else -1
		val = self.f(self.counter)
		print(val)
		self.brush = QBrush(self.get_color())

	def get_coordinates(self):
		cw = round(GRAPHICS_SIZE / 2)
		ch = round(GRAPHICS_SIZE / 2)
		d = 42+self.f(self.counter)
		print("d: " + str(d))
		return [cw - d, ch - d, d * 2, d * 2]

	def draw(self):
		c = self.get_coordinates()
		painter = QPainter(self)
		painter.setRenderHint(QPainter.Antialiasing)
		painter.setBrush(self.brush)
		painter.setPen(self.pen)
		painter.drawEllipse(QRect(c[0], c[1], c[2], c[3]))

	def paintEvent(self, event):
		self.draw()

	def timerEvent(self, event):
		self.live()
		self.update()

	def f(self, x: float):
		r = round(easeOutBounce(x / 42))
		print("f(" + str(x) + ") = " + str(r))
		return r

	def get_color(self):
		val = self.f(self.counter)
		return QColor(127, 255 - val, val)
