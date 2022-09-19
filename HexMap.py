import hexy as hx
import pygame as pg
from HexTectonics import *
import HexCell as HexCell
import numpy as np
from random import randint
from HexPlate import TectonicPlate
import opensimplex


class HexMap(hx.HexMap):
    def __init__(self, radius):
        super().__init__()
        opensimplex.random_seed()
        self.radius = radius
        self.TectonicPlates = []

    def createCells(self, size):
        spiralCoordinates = hx.get_spiral(np.array((0, 0, 0)), 0, self.radius)
        axial_coordinates = hx.cube_to_axial(spiralCoordinates)
        for i, v in enumerate(axial_coordinates):
            coord = f"{v[0]},{v[1]}"
            self.setitem_direct(coord, HexCell.HexCell(v, size, 0, i, self))

        for v in axial_coordinates:
            coord = f"{v[0]},{v[1]}"
            self._map[coord].setNeighbors()

    def generateTectonis(self):
        colors = [
            (
                125 + randint(-125, 125),
                125 + randint(-125, 125),
                125 + randint(-125, 125),
            )
            for i in self.TectonicPlates
        ]
        assignPlates(list(self._map.values()), self.TectonicPlates, colors)
        for plate in self.TectonicPlates:
            plate.setBoundaryCells()
            plate.map = self
            plate.generateElevation()

    def createTectonicPlates(self, nPlates, ratio):
        types = ["oceanic", "continental"]
        nContinental = nPlates * ratio
        for i in range(nPlates):
            if i < nContinental:
                self.TectonicPlates.append(TectonicPlate(types[1]))
            else:
                self.TectonicPlates.append(TectonicPlate(types[0]))

    def setCellsBiomes(self):
        for cell in self.values():
            if cell.elevation < 0:
                cell.setBiomeColor((52, 70, 235))
            elif 0 <= cell.elevation < 90:
                cell.setBiomeColor((0, 125, 25))
            elif 90 <= cell.elevation:
                cell.setBiomeColor((255, 255, 255))
            else:
                cell.setBiomeColor((0, 125, 25))

    def createMap(self, size, nPlates, ratio):
        self.createCells(size)
        self.createTectonicPlates(nPlates, ratio)
        self.generateTectonis()
        self.setCellsBiomes()

    def draw(self):
        for i in self._map.values():
            i.draw()
