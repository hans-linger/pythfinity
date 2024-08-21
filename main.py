import sys

from PyQt5.QtWidgets import QApplication

from src.layout import make_layout

from src.qtcore.main_window import MainWindow

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
