import math

from PyQt5.QtCore import QObject, QPropertyAnimation, pyqtProperty
from PyQt5.QtGui import QColor

from src.core.constants import DYING_SPEED, NORMAL_SPEED, START_SPEED
from src.core.helpers import parabolic_interpolation


class Polly(QObject):
    def __init__(self, r, n, color: QColor, x=0, y=0, a=0, parent=None):
        super().__init__(parent)
        self.r = r
        self.n = n
        self.color = color
        self.x = x
        self.y = y
        self.a = a
        self._alpha = 0.0
        self._is_dying = False
        self.vertices = self.calculate_vertices()
        self.rotation_speed = START_SPEED
        self.animation = QPropertyAnimation(self, b"alpha")
        self.animation.setDuration(200)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.setLoopCount(1)

    def calculate_vertices(self):
        vertices = []
        for i in range(self.n):
            angle = 2 * math.pi * i / self.n + math.radians(self.a)
            vx = self.x + self.r * math.cos(angle)
            vy = self.y + self.r * math.sin(angle)
            vertices.append((vx, vy))
        return vertices

    def live(self):
        # rotation speed
        if self._is_dying:
            if self.rotation_speed < DYING_SPEED:
                self.rotation_speed *= 2
        elif abs(self.rotation_speed - NORMAL_SPEED) < 1000:
            self.rotation_speed = parabolic_interpolation(
                START_SPEED,
                NORMAL_SPEED,
                (self.rotation_speed) / (NORMAL_SPEED - START_SPEED),
            )

        self.rotate()

    def rotate(self):
        self.a += self.rotation_speed
        self.vertices = self.calculate_vertices()

    @pyqtProperty(float)
    def alpha(self):
        return self._alpha

    @alpha.setter
    def alpha(self, value):
        self._alpha = value

    def start_fade_in(self):
        self.alpha = 0.0
        self.animation.start()

    def start_fade_out(self):
        self.alpha = 1.0
        self.animation.setDirection(QPropertyAnimation.Backward)
        self.animation.start()
