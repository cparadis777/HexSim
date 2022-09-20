import hexy as hx
import pygame as pg
from HexTectonics import *
import HexCell as HexCell
import numpy as np
from random import randint
from HexPlate import TectonicPlate
import opensimplex
from utils import *
import time


class HexMap(hx.HexMap):
    def __init__(self):
        super().__init__()
        opensimplex.random_seed()
        self.tectonicPlates = []
        self.mapSize = None
        self.screenSize = None

    def createCells(self, mapSize, tileSize):
        coords = []

        if len(mapSize) == 1:
            spiralCoordinates = hx.get_spiral(np.array((0, 0, 0)), 0, mapSize)
            coords = hx.cube_to_axial(spiralCoordinates)

        elif len(mapSize) == 2:
            if mapSize[0] % 2 != 0 or mapSize[1] % 2 != 0:
                raise Exception("Grid size not even")
            for i in range(int(-mapSize[0] / 2), int(mapSize[0] / 2)):
                for j in range(int(-mapSize[1] / 2), int(mapSize[1] / 2)):
                    coords.append(offset_to_axial(np.array([[i, j]]))[0])

        for i, v in enumerate(coords):
            coord = f"{v[0]},{v[1]}"
            self.setitem_direct(
                coord, HexCell.HexCell(v, tileSize, 0, i, self, self.screenSize)
            )

        for v in coords:
            coord = f"{v[0]},{v[1]}"
            self._map[coord].setNeighbors()

    def generateTectonis(self):
        colors = [
            (
                125 + randint(-125, 125),
                125 + randint(-125, 125),
                125 + randint(-125, 125),
            )
            for i in self.tectonicPlates
        ]
        assignPlates(list(self._map.values()), self.tectonicPlates, colors)
        for plate in self.tectonicPlates:
            plate.setBoundaryCells()
            plate.map = self
            plate.generateElevation()

    def createTectonicPlates(self, nPlates, ratio):
        types = ["oceanic", "continental"]
        nContinental = nPlates * ratio
        for i in range(nPlates):
            if i < nContinental:
                self.tectonicPlates.append(TectonicPlate(types[1]))
            else:
                self.tectonicPlates.append(TectonicPlate(types[0]))

    def setCellsBiomes(self):
        for cell in self.values():
            if cell.elevation < 0:
                cell.setBiomeColor((52, 70, 235))
            elif 0 <= cell.elevation < 50:
                cell.setBiomeColor((0, 125, 25))
            elif 50 <= cell.elevation < 90:
                cell.setBiomeColor((116, 118, 125))
            elif 90 <= cell.elevation:
                cell.setBiomeColor((255, 255, 255))
            else:
                cell.setBiomeColor((0, 125, 25))

    def createMap(self, mapSize, tileSize, nPlates, ratio, screenSize):
        start = time.time()
        self.screenSize = screenSize
        self.mapSize = mapSize
        self.createCells(mapSize, tileSize)
        self.createTectonicPlates(nPlates, ratio)
        self.generateTectonis()
        self.setCellsBiomes()
        stop = time.time()
        print(f"Map generated in: {stop-start}s")

    def draw(self):
        for i in self._map.values():
            i.draw()
