import hexy as hx
from HexTectonics import assignPlates
import HexCell as HexCell
import numpy as np
from random import randint
from HexPlate import TectonicPlate
import opensimplex
import utils
import time


class HexMap(hx.HexMap):
    def __init__(self):
        super().__init__()
        opensimplex.random_seed()
        self.tectonicPlates = []
        self.mapSize = None
        self.screenSize = None

    def createCells(self, mapSize, tileSize) -> None:
        coords = []

        if len(mapSize) == 1:
            raise Exception("Map must be rectangular, not circular.")
            spiralCoordinates = hx.get_spiral(np.array((0, 0, 0)), 0, mapSize[0])
            coords = hx.cube_to_axial(spiralCoordinates)

        elif len(mapSize) == 2:
            if mapSize[0] % 2 != 0 or mapSize[1] % 2 != 0:
                raise Exception("Grid size not even")
            for i in range(int(-mapSize[0] / 2), int(mapSize[0] / 2)):
                for j in range(int(-mapSize[1] / 2), int(mapSize[1] / 2)):
                    coords.append(utils.offset_to_axial(np.array([[i, j]]))[0])

        for i, v in enumerate(coords):
            coord = f"{v[0]},{v[1]}"
            self.setitem_direct(
                coord, HexCell.HexCell(v, tileSize, 0, i, self, self.screenSize)
            )

        for v in coords:
            coord = f"{v[0]},{v[1]}"
            self._map[coord].setNeighbors()

    def generateTectonics(self, zeta) -> None:
        assignPlates(list(self._map.values()), self.tectonicPlates)
        print("     Cells assigned to plates")
        for i, plate in enumerate(self.tectonicPlates):
            plate.setBoundaryCells()
            plate.generateElevation(zeta)
            print(f"     {i}/{len(self.tectonicPlates)} plates done")

    def createTectonicPlates(self, nPlates, ratio) -> None:
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

    def setCellsBiomes(self) -> None:
        for cell in self.values():
            if abs(cell.tectonicActivity) > 290:
                print(cell.tectonicActivity)
                cell.setBiomeColor((255, 0, 0))
                cell.setElevation(cell.elevation + 100)

            elif cell.elevation < 0:
                cell.setBiomeColor(
                    utils.colorLerp(cell.elevation, -50, 0, (0, 30, 52), (0, 212, 255))
                )
            elif 0 <= cell.elevation < 80 and -20 < cell.temperature < 25:
                cell.setBiomeColor((0, 125, 25))
            elif 0 <= cell.elevation < 80 and cell.temperature >= 25:
                cell.setBiomeColor((248, 238, 100))
            elif 0 <= cell.elevation < 80 and cell.temperature <= -20:
                cell.setBiomeColor((240, 240, 240))
            elif 80 <= cell.elevation < 95:
                cell.setBiomeColor((116, 118, 125))
            elif 95 <= cell.elevation:
                cell.setBiomeColor((255, 255, 255))
            else:
                cell.setBiomeColor((0, 125, 25))

    def setElevationColor(self) -> None:
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
        print("Setting making heightmap")
        self.setElevationColor()
        print("Setting temperatures")
        self.setTemperature(35, -40)
        print("Attributing biomes")
        self.setCellsBiomes()
        stop = time.time()
        print(f"Map generated in: {stop-start}s")

    def setTemperature(self, equatorTemp, polesTemp) -> None:
        for cell in self._map.values():
            latitude = abs(cell.axial_coordinates[0][1])
            temperature = utils.numericalLerp(
                latitude, 0, self.mapSize[1] / 2, equatorTemp, polesTemp
            ) + randint(-5, 5)
            cell.setTemperature(temperature)
            hot = (
                255,
                0,
                0,
            )
            cold = (0, 30, 152)
            cell.setTemperatureColor(
                utils.colorLerp(temperature, polesTemp, equatorTemp, cold, hot)
            )

    def draw(self) -> None:
        for i in self._map.values():
            i.draw()
