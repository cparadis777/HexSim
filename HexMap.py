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
import utils as utils


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
            spiralCoordinates = hx.get_spiral(np.array((0, 0, 0)), 0, mapSize[0])
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

    def generateTectonics(self, zeta):
        assignPlates(list(self._map.values()), self.tectonicPlates)
        print("     Cells assigned to plates")
        for i, plate in enumerate(self.tectonicPlates):
            plate.setBoundaryCells()
            plate.generateElevation(zeta)
            print(f"     {i}/{len(self.tectonicPlates)} plates done")

    def createTectonicPlates(self, nPlates, ratio):
        baseHeights = [-50, 50]
        nContinental = nPlates * ratio
        for i in range(nPlates):
            color = (randint(0, 255), randint(0, 255), randint(0, 255))
            if i < nContinental:
                self.tectonicPlates.append(
                    TectonicPlate(self, baseHeights[1] + randint(-20, 20), color)
                )
            else:
                self.tectonicPlates.append(
                    TectonicPlate(self, baseHeights[0] + randint(-20, 20), color)
                )

    def setCellsBiomes(self):
        for cell in self.values():
            if cell.elevation < 0:
                cell.setBiomeColor(
                    utils.colorLerp(cell.elevation, -50, 0, (0, 30, 52), (0, 212, 255))
                )
            elif 0 <= cell.elevation < 80:
                cell.setBiomeColor((0, 125, 25))
            elif 80 <= cell.elevation < 95:
                cell.setBiomeColor((116, 118, 125))
            elif 95 <= cell.elevation:
                cell.setBiomeColor((255, 255, 255))
            else:
                cell.setBiomeColor((0, 125, 25))

    def setElevationColor(self):
        for cell in self.values():
            cell.setHeightColor(utils.grayscaleLerp(cell.elevation))

    def createMap(self, mapSize, tileSize, nPlates, ratio, screenSize, zeta):
        start = time.time()
        self.screenSize = screenSize
        self.mapSize = mapSize
        print("Creating cells")
        self.createCells(mapSize, tileSize)
        print("Creating tectonic plates")
        self.createTectonicPlates(nPlates, ratio)
        print("Simulating Tectonics")
        self.generateTectonics(zeta)
        for i in self.tectonicPlates:
            i.shuffleEdges(0)
            i.setBoundaryCells()
        
        print("Attributing biomes")
        self.setCellsBiomes()
        print("Setting making heightmap")
        self.setElevationColor()
        stop = time.time()
        print(f"Map generated in: {stop-start}s")

    def draw(self):
        for i in self._map.values():
            i.draw()
