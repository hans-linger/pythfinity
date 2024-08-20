from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPalette
from PyQt5.QtWidgets import QWidget

from src.core.constants import GRAPHICS_SIZE
from src.qtcore.circle import Circle


class Mirror(QWidget):
	def __init__(self):
		super(Mirror, self).__init__()
		self.setGeometry(GRAPHICS_SIZE, GRAPHICS_SIZE, GRAPHICS_SIZE, GRAPHICS_SIZE)

