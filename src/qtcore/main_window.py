from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget

from src.core.constants import GRAPHICS_SIZE
from src.qtcore.circle import Circle
from src.qtcore.layout import Layout
from src.qtcore.mirror import Mirror


class MainWindow(QMainWindow):
	def __init__(self):
		super(MainWindow, self).__init__()
		self.setWindowTitle("Qt Test 1")
		self.setGeometry(GRAPHICS_SIZE, GRAPHICS_SIZE, GRAPHICS_SIZE, GRAPHICS_SIZE)
		m = Circle()
		self.setCentralWidget(m)
