from random import randint
from HexCell import HexCell
import hexy as hx
import utils
import math
import HexDirections


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
            previousClosest = None
            for i, root in enumerate(plateRoots):
                dist = hx.get_cube_distance(cell.cube_coordinates, root)
                if dist < closestDistance:
                    closestDistance = dist
                    previousClosest = closestRoot
                    closestRoot = i
            cell.setTectonicPlate(closestRoot)
            plates[closestRoot].addCell(cell)
            cell.setTectonicColor(colors[closestRoot])


def getCollisionType(plate1, plate2):
    relativeDirection = None
    collisionType = None
    type1, speed1, direction1 = plate1.type, plate1.speed, plate1.direction
    type2, speed2, direction2 = plate2.type, plate2.speed, plate2.direction

    angle1 = math.radians(60 * direction1.value)
    angle2 = math.radians(60 * direction2.value)

    hSpeed1 = speed1 * math.cos(angle1)
    hSpeed2 = speed2 * math.cos(angle2)
    vSpeed1 = speed1 * math.sin(angle1)
    vSpeed2 = speed2 * math.sin(angle2)

    relativeSpeedx, relativeSpeedy = (hSpeed2 - hSpeed1), (vSpeed2 - vSpeed1)

    relativeSpeedx = 1 if relativeSpeedx == 0 else relativeSpeedx
    relativeAngle = math.degrees(math.tan(relativeSpeedy / relativeSpeedx))

    if relativeAngle > 360:
        relativeAngle = relativeAngle % 360
    if relativeAngle < -360:
        relativeAngle = -1 * (-relativeAngle % 360)

    roundedAngle = relativeAngle // 60
    if roundedAngle < 0:
        roundedAngle += 6

    relativeDirection = HexDirections.HexDirections(roundedAngle)

    magnitude = math.sqrt(relativeSpeedx**2 + relativeSpeedy**2) * (
        relativeDirection.value - direction1.value
    )
    if magnitude < -100:
        collisionType = "Divergent"
    if -100 <= magnitude < 100:
        collisionType = "Transform"
    if 100 <= magnitude:
        collisionType = "Convergent"
    return collisionType
