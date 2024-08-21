from src.core.helpers import parabolic_interpolation

parabolic_interpolation(10, 50, 0)
a1 = 10
a2 = 50
z = a1
i = 0
while abs(a2 - z) > 10 and i < 10:
	z = parabolic_interpolation(z, a2, (z - a1) / (a2 - a1))
	i += 1
