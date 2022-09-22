from random import randint
from HexDirections import HexDirections
import hexy as hx
import numpy as np
import opensimplex
import HexTectonics


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
        self.speed = randint(0, 100)
        self.direction = HexDirections(randint(0, 5))

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

    def propagateTectonics(self, cell, zeta):
        if zeta > 1:
            raise ValueError("Zeta must be ]0,1]")
        magnitudeToPropagate = cell.getTectonicActivity() * zeta
        for neighbor in cell.getNeighbors():
            if neighbor is None:
                pass
            elif neighbor.getTectonicPlate() != self:
                pass
            elif abs(neighbor.getTectonicActivity()) >= abs(magnitudeToPropagate):
                pass
            else:
                neighbor.setTectonicActivity(magnitudeToPropagate)
                self.propagateTectonics(neighbor, zeta)

    def generateElevation(self, zeta=0.5):

        for boundary in self.boundaries:
            self.collisions[boundary] = HexTectonics.getCollisionMagnitude(
                self, boundary
            )
            heightDifference = self.baseHeight - boundary.baseHeight
            if abs(heightDifference) < 30:
                for cell in self.boundaries[boundary]:
                    cell.setTectonicActivity(self.collisions[boundary])
                    self.propagateTectonics(cell, zeta)

            elif heightDifference >= 30:
                for cell in self.boundaries[boundary]:
                    cell.setTectonicActivity(self.collisions[boundary])
                    self.propagateTectonics(cell, zeta)
            elif heightDifference <= -30:
                for cell in self.boundaries[boundary]:
                    cell.setTectonicActivity(-self.collisions[boundary])
                    self.propagateTectonics(cell, zeta)

        for i in self.cells:
            coord = i.axial_coordinates
            i.setElevation(
                abs(opensimplex.noise2(x=coord[0][0], y=coord[0][1]))
                * i.getTectonicActivity()
                + self.baseHeight
            )
           # print(i.elevation)
