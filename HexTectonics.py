from random import randint
import hexy as hx
import utils
import math
import HexDirections


def assignPlates(cells, plates):
    frontiers = {plate: [] for plate in plates}
    for plate in plates:
        cell = cells[randint(0, len(cells))]
        while cell.getTectonicPlate() != None:
            cell = cells[randint(0, len(cells) - 1)]
        plate.addCell(cell)
        frontiers[plate].append(cell)
    i = 0

    while any(n.getTectonicPlate() is None for n in cells):
        currentPlate = plates[i % len(plates)]
        if len(frontiers[currentPlate]) == 0:
            pass
        else:
            chosenCell = frontiers[currentPlate][
                randint(0, len(frontiers[currentPlate]) - 1)
            ]
            for neighbor in chosenCell.getNeighbors():
                if neighbor is None:
                    pass
                elif neighbor.getTectonicPlate() is None:

                    currentPlate.addCell(neighbor)
                    frontiers[currentPlate].append(neighbor)
                elif neighbor.getTectonicPlate() is not None:
                    if neighbor.getTectonicPlate() in currentPlate.boundaries.keys():
                        currentPlate.boundaries[neighbor.getTectonicPlate()].append(chosenCell)
                    else:
                        currentPlate.boundaries[neighbor.getTectonicPlate()] = [chosenCell]
            frontiers[currentPlate].remove(chosenCell)
        i += 1
    print("Done assigning cells")


def assignPlatesByCell(cells, plates):

    plateRoots = {}
    for plate in plates:
        cell = cells[randint(0, len(cells) - 1)]
        plateRoots[cell] = plate
        plate.addCell(cell)
        cells.remove(cell)

    for cell in cells:
        closestRoot = None
        closestDistance = 1000000000
        for root in plateRoots:
            dist = hx.get_cube_distance(root.cube_coordinates, cell.cube_coordinates)
            if dist < closestDistance:
                closestDistance = dist
                closestRoot = root
        plateRoots[closestRoot].addCell(cell)


def getCollisionMagnitude(plate1, plate2):
    relativeDirection = None
    collisionType = None
    speed1, direction1 = plate1.speed, plate1.direction
    speed2, direction2 = plate2.speed, plate2.direction

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
    magnitude = utils.clamp(magnitude, -75, 75)
    return magnitude
