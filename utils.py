import numpy as np


def axial_to_offset(axial):
    q = int(axial[0][0])
    r = int(axial[0][1])

    offset = r & 1
    col = q + (r - offset) / 2
    row = r
    offsetCoords = np.array([[col, row]])
    return offsetCoords


def offset_to_axial(offset):
    col = int(offset[0][0])
    row = int(offset[0][1])

    q = col - ((row - (row & 1)) / 2)
    r = row
    return np.array([[q, r]])


def clamp(num, min_value, max_value):
    return max(min(num, max_value), min_value)


def grayscaleLerp(value):
    x = value
    x = clamp(x, -100, 100)
    x = normalize(x, -100, 100)

    return (255 * x, 255 * x, 255 * x)


def colorLerp(value, min, max, color1, color2):
    x = value
    x = clamp(x, min, max)
    x = normalize(x, min, max)
    colorDiff = (color2[0] - color1[0], color2[1] - color1[1], color2[2] - color1[2])
    color = (
        color1[0] + colorDiff[0] * x,
        color1[1] + colorDiff[1] * x,
        color1[2] + colorDiff[2] * x,
    )
    # print(f"colorDiff: {colorDiff}. \n In:{value}, normalized: {x}, out:{color}")
    return color


def numericalLerp(value, minValue, maxValue, minRange, maxRange) -> float:
    x = value
    x = normalize(x, minValue, maxValue)
    return minRange + ((maxRange - minRange) * x)


def normalize(value, min, max):
    normalizedValue = (value - min) / (max - min)
    return normalizedValue
