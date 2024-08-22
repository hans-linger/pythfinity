import sys

from PyQt5.QtWidgets import QApplication

from src.core.constants import GRAPHICS_SIZE
from src.qtcore.main_window import MainWindow

app = QApplication(sys.argv)
window = MainWindow()
window.setFixedSize(GRAPHICS_SIZE, GRAPHICS_SIZE + 100)
window.setContentsMargins(0, 0, 0, 0)
window.setStyleSheet("QGraphicsView { border: 0; }")
window.show()
sys.exit(app.exec_())
