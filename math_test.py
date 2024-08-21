from PyQt5.QtGui import QColor

from src.core.helpers import calc_colors

cc = calc_colors(QColor(0, 0, 0), QColor(255, 255, 255), 3)
ccc = [10, 30, 50]
print(' '.join(map(lambda x: str(x.red()), cc)))
