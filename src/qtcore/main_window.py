from PyQt5.QtWidgets import QMainWindow

from src.core.constants import GRAPHICS_SIZE
from src.qtcore.mirror import Mirror


class MainWindow(QMainWindow):
	def __init__(self):
		super(MainWindow, self).__init__()
		self.setWindowTitle("Pythfinity 0.1a")
		self.setGeometry(GRAPHICS_SIZE, GRAPHICS_SIZE, GRAPHICS_SIZE, GRAPHICS_SIZE)
		m = Mirror()
		self.setCentralWidget(m)
