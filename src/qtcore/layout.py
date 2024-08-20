from PyQt5.QtCore import QRect
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QHBoxLayout, QWidget, QSizePolicy

from src.qtcore.mirror import Mirror


class Color(QWidget):

	def __init__(self, color):
		super(Color, self).__init__()
		self.setAutoFillBackground(True)

		palette = self.palette()
		palette.setColor(QPalette.Window, QColor(color))
		self.setPalette(palette)


class Layout(QHBoxLayout):
	def __init__(self):
		super(QHBoxLayout, self).__init__()
		w = Color('blue')
		w.sizeHint()
		w.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
		mirror = Mirror()
		mirror.resize(500, 500)
		mirror.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.addWidget(mirror, stretch=3)
		self.addWidget(w, stretch=1)
