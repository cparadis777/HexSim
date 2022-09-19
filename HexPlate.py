from random import randint
from HexDirections import HexDirections
import hexy as hx
import numpy as np
import opensimplex


class TectonicPlate:
    def __init__(self, type):
        self.map = None
        self.cells = []
        self.boundaryCells = []
        self.setDirection()
        self.neighboringPlates = []
        self.type = type

    def addCell(self, cell):
        self.cells.append(cell)

    def setDirection(self):
        self.speed = randint(0, 100)
        self.direction = HexDirections(randint(0, 5))

    def setBoundaryCells(self):
        for cell in self.cells:
            for neighbor in cell.neighbors:
                if neighbor is not None and neighbor.tectonicPlate is not None:
                    if neighbor.tectonicPlate != cell.tectonicPlate:
                        if cell not in self.boundaryCells:
                            self.boundaryCells.append(cell)
                        if neighbor.tectonicPlate not in self.neighboringPlates:
                            self.neighboringPlates.append(neighbor.tectonicPlate)

        for cell in self.boundaryCells:
            newColor = (
                min(255, cell.tectonicColor[0] + 40),
                min(255, cell.tectonicColor[1] + 40),
                min(255, cell.tectonicColor[2] + 40),
            )
            cell.setTectonicColor(newColor)

    def generateElevation(self):
        base = 25 if self.type == "continental" else -75
        for i in self.cells:
            coord = i.axial_coordinates
            i.setElevation(
                opensimplex.noise2(x=coord[0][0], y=coord[0][1]) * 100 + base
            )
