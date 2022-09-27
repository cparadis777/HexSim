from random import randint

# import hexy as hx
# import numpy as np
import opensimplex

from HexGenerator import HexTectonics
from HexGenerator.HexDirection import HexDirection


class TectonicPlate:
    def __init__(self, map, baseHeight, color):
        self.map = map
        self.cells = []
        self.boundaryCells = []
        self.setDirection()
        self.boundaries = {}
        self.collisions = {}
        self.collisionTypes = []
        self.baseHeight = baseHeight
        self.color = color

    def addCell(self, cell):
        self.cells.append(cell)
        cell.setTectonicPlate(self)
        cell.setTectonicColor(self.color)

    def setDirection(self):
        self.speed = randint(0, 10)
        self.direction = HexDirection(randint(0, 5))

    def setBoundaryCells(self):
        for neighbor in self.boundaries:
            newColor = (
                min(255, self.color[0] + randint(10, 50)),
                min(255, self.color[1] + randint(10, 50)),
                min(255, self.color[2] + randint(10, 50)),
            )
            for cell in self.boundaries[neighbor]:
                cell.setTectonicColor(newColor)

    def shuffleEdges(self, shuffleFactor=10):
        cellsToRemove = []
        for boundary, cells in self.boundaries.items():
            for cell in cells:
                if randint(0, 100) < shuffleFactor:
                    boundary.addCell(cell)
                    cellsToRemove.append(cell.tile_id)
            for cell in self.boundaries[boundary]:
                if cell.tile_id in cellsToRemove:
                    self.boundaries[boundary].remove(cell)
        for cell in self.cells:
            if cell.tile_id in cellsToRemove:
                self.cells.remove(cell)
        self.setBoundaryCells()

    def generateElevation(self, zeta=0.5):

        for boundary in self.boundaries:
            magnitude = HexTectonics.getCollisionMagnitude(self, boundary)
            self.collisions[boundary] = magnitude
            heightDifference = self.baseHeight - boundary.baseHeight
            if -30 < heightDifference < 30:
                for cell in self.boundaries[boundary]:
                    cell.setTectonicActivity(magnitude)

            elif heightDifference >= 30:
                for cell in self.boundaries[boundary]:
                    cell.setTectonicActivity(magnitude)

            elif heightDifference <= -30:
                magnitude = -magnitude
                for cell in self.boundaries[boundary]:
                    cell.setTectonicActivity(-magnitude)

            frontier = self.boundaries[boundary]

            while len(frontier) != 0 and (magnitude > 1 or magnitude < -1):
                magnitude = magnitude * zeta
                frontier = HexTectonics.propagateTectonics(self, frontier, magnitude)

        for i in self.cells:
            coord = i.axial_coordinates
            # print(i.getTectonicActivity())
            i.setElevation(
                abs(opensimplex.noise2(x=coord[0][0] / (self.map.mapSize[0] / 2),
                                       y=coord[0][1] / (self.map.mapSize[1] / 2))) * 30 +
                i.getTectonicActivity() / 100 * self.baseHeight
                + self.baseHeight
            )
        # print(i.elevation)
