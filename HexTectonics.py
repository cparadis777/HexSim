from random import randint
from HexCell import HexCell
import hexy as hx


def assignPlates(cells, plates, colors):

    freeIndices = [i for i in range(len(cells))]
    plateRoots = []
    for i in range(len(plates)):
        index = randint(0, len(cells) - 1)
        freeIndices.remove(index)
        plates[i].addCell(cells[index])
        cells[index].setTectonicColor(colors[i])
        plateRoots.append(plates[i].cells[0].cube_coordinates)
        cells[index].setTectonicPlate(i)

    for cell in cells:
        if cell.tile_id in freeIndices:
            closestDistance = 1000000000
            closestRoot = None
            for i, root in enumerate(plateRoots):
                dist = hx.get_cube_distance(cell.cube_coordinates, root)
                if dist < closestDistance:
                    closestDistance = dist
                    closestRoot = i
            cell.setTectonicPlate(closestRoot)
            plates[closestRoot].addCell(cell)
            cell.setTectonicColor(colors[closestRoot])
