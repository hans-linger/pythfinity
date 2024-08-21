from math import cos, tan, radians, degrees, pi
from cmath import polar, rect

from PyQt5.QtGui import QColor


def circum_from_inscribe(r: float, n: int):
	# r - inscribed radius
	# n - vertices number
	return r / (cos(radians(180 / n)))


def circum_to_inscribe(R: float, n: int):
	# R - circumcircle radius
	# n - vertices number
	print(n)
	return R * cos(radians(180 / n))


def calc_colors(c1: QColor, c2: QColor, n: int):
	if n == 1:
		return [c1]
	r1 = c1.red()
	g1 = c1.green()
	b1 = c1.blue()
	r2 = c2.red()
	g2 = c2.green()
	b2 = c2.blue()
	res = []
	rstep = (r2 - r1) / (n - 1)
	gstep = (g2 - g1) / (n - 1)
	bstep = (b2 - b1) / (n - 1)
	for i in range(n):
		c = QColor()
		c.setRedF((r1 + rstep * i) / 255)
		c.setGreenF((g1 + gstep * i) / 255)
		c.setBlueF((b1 + bstep * i) / 255)
		res.append(c)
	return res


def parabolic_interpolation(a1, a2, t):
	return (1 - t) ** 2 * a1 + 2 * (1 - t) * t * ((a1 + a2) / 2) + t ** 2 * a2
