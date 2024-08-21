from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QWidget

GRAPHICS_SIZE = 500
START_COLOR = QColor(0, 0, 0)
END_COLOR = QColor(255, 255, 255)
START_SPEED = 15
NORMAL_SPEED = 0
DYING_SPEED = 100


class Color(QWidget):

	def __init__(self, color):
		super(Color, self).__init__()
		self.setAutoFillBackground(True)
		palette = self.palette()
		palette.setColor(QPalette.Window, QColor(color))
		self.setPalette(palette)
