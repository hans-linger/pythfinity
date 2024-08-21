from math import cos, radians, pi, sin, sqrt

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
		return [QColor(c1.red() - c2.red(), c1.green() - c2.green(), c1.blue() - c2.blue())]
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


def parabolic_interpolation(a1, a2, t: float):
	return (1 - t) ** 2 * a1 + 2 * (1 - t) * t * ((a1 + a2) / 2) + t ** 2 * a2


def ease_in_back(a1, a2, t: float):
	c1 = 1.70158
	c3 = c1 + 1
	return (a2 - a1) * (c3 * t * t * t - c1 * t * t)


def ease_out_elastic(a1, a2, x: float):
	c4 = (2 * pi) / 3
	return (a2 - a1) * (0 if x == 0 else 1 if x == 1 else pow(2, -10 * x) * sin((x * 10 - 0.75) * c4) + 1)


def easeOutBounce(x: float):
	n1 = 7.5625
	d1 = 2.75

	if x < 1 / d1:
		return n1 * x * x
	elif x < 2 / d1:
		return n1 * (x - 1.5 / d1) * x + 0.75
	elif x < 2.5 / d1:
		return n1 * (x - 2.25 / d1) * x + 0.9375
	else:
		return n1 * (x - 2.625 / d1) * x + 0.984375


def ease_out_circ(a1, a2, t: float):
	t -= 1
	return (a2 - a1) * sqrt(1 - t * t)
