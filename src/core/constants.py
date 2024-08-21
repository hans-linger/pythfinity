from tkinter.constants import NORMAL

from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QWidget

GRAPHICS_SIZE = 500
START_COLOR = QColor(0, 0, 0)
END_COLOR = QColor(255, 255, 255)
START_SPEED = 1
NORMAL_SPEED = 15
DYING_SPEED = 1000


class Color(QWidget):

	def __init__(self, color):
		super(Color, self).__init__()
		self.setAutoFillBackground(True)
		palette = self.palette()
		palette.setColor(QPalette.Window, QColor(color))
		self.setPalette(palette)


def easeOutBounce(x: float):
	n1 = 7.5625
	d1 = 2.75

	if x < 1 / d1:
		return n1 * x * x
	elif x < 2 / d1:
		return n1 * (x - 1.5 / d1) * x + 0.75
	elif (x < 2.5 / d1):
		return n1 * (x - 2.25 / d1) * x + 0.9375
	else:
		return n1 * (x - 2.625 / d1) * x + 0.984375


def easeOutCirc(t):
	import math
	t -= 1
	return math.sqrt(1 - t * t)
