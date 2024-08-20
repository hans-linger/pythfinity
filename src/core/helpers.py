from math import cos, tan, radians, degrees, pi
from cmath import polar, rect


def circum_from_inscribe(r: float, n: int):
    # r - inscribed radius
    # n - vertices number
    return r / (cos(radians(180/n)))

def circum_to_inscribe(R: float, n: int):
    # R - circumcircle radius
    # n - vertices number
    print(n)
    return R * cos(radians(180 / n))

