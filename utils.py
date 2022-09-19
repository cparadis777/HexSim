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
