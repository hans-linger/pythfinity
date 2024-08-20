import sys

from PyQt5.QtWidgets import QApplication

from src.layout import make_layout
from ctypes import windll

from src.qtcore.main_window import MainWindow

timeBeginPeriod = windll.winmm.timeBeginPeriod
timeBeginPeriod(1)

# window, pm = make_layout()
# window.mainloop()

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
