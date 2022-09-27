import time
from random import randint

import hexy as hx
import numpy as np
import opensimplex

import HexCell as HexCell
import HexGenerator.HexRiver
import utils
from HexGenerator import HexBiomes
from HexGenerator.HexHydrology import propagateMoisture
from HexGenerator.HexTectonics import assignPlates
from HexPlate import TectonicPlate


class HexMap(hx.HexMap):
    def __init__(self):
        super().__init__()
        opensimplex.random_seed()
        self.tectonicPlates = []
        self.mapSize = None
        self.screenSize = None
        self.rivers = []

    def createCells(self, mapSize, tileSize) -> None:
        coords = []

        if len(mapSize) == 1:
            raise Exception("Map must be rectangular, not circular.")
            # spiralCoordinates = hx.get_spiral(np.array((0, 0, 0)), 0, mapSize[0])
            # coords = hx.cube_to_axial(spiralCoordinates)

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
        print("     Assigning cells to plates")
        assignPlates(list(self._map.values()), self.tectonicPlates)
        print("     Calculating Boundaries & Propagating elevation")
        for i, plate in enumerate(self.tectonicPlates):
            plate.setBoundaryCells()
            plate.generateElevation(zeta)
            print(f"\r    {i}/{len(self.tectonicPlates)} plates done", end="")
        print(
            f"\r     {len(self.tectonicPlates)}/{len(self.tectonicPlates)} plates done"
        )

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
            if cell.elevation < 0:
                HexBiomes.oceanBiomes(cell)
            elif cell.elevation > 100:
                HexBiomes.mountainBiomes(cell)
            elif 0 < cell.temperature < 20:
                HexBiomes.temperateBiomes(cell)
            elif -20 < cell.temperature <= 0:
                HexBiomes.borealBiomes(cell)
            elif cell.temperature <= -20:
                HexBiomes.polarBiomes(cell)
            elif cell.temperature >= 20:
                HexBiomes.tropicalBiomes(cell)
            else:
                cell.setBiomeColor((255, 255, 255))

    def setElevationColor(self) -> None:
        for cell in self.values():
            cell.setHeightColor(utils.grayscaleLerp(cell.elevation, -400, 400))

    def propagateMoisture(self, nIterations):
        frontier = []
        moisture = 100
        for cell in self._map.values():
            if cell.elevation < 0:
                cell.moisture = moisture
                frontier.append(cell)
        i = 0
        while len(frontier) > 0 and i <= nIterations:
            frontier = propagateMoisture(frontier)
            i += 1
            print(f"\r    {i}/{nIterations} iterations done", end="")
        print(f"\r    {nIterations}/{nIterations} iterations done")

        for cell in self._map.values():
            color = utils.colorLerp(cell.moisture, 0, 100, (0, 0, 0), (0, 27, 142))
            cell.setMoistureColor(color)

    def createMap(
            self,
            mapSize,
            tileSize,
            nPlates,
            ratio,
            screenSize,
            zetaTectonics,
            axialTilt,
            nIterations,
    ):
        start = time.time()
        self.screenSize = screenSize
        self.mapSize = mapSize
        print("Creating cells")
        self.createCells(mapSize, tileSize)
        print("Creating tectonic plates")
        self.createTectonicPlates(nPlates, ratio)
        print("Simulating Tectonics")
        self.generateTectonics(zetaTectonics)
        for i in self.tectonicPlates:
            i.shuffleEdges(0)
            i.setBoundaryCells()
        print("Setting making heightmap")
        self.setElevationColor()
        print("Setting temperatures")
        self.setTemperature(axialTilt, 35, -40)
        print("Generation winds")
        self.generateWinds()
        print("Propagating moisture")
        self.propagateMoisture(nIterations)
        print("Generating Rivers")
        self.generateRivers()
        print("Attributing biomes")
        self.setCellsBiomes()
        stop = time.time()
        print(f"Map generated in: {stop - start}s")

    def setTemperature(self, axialTilt, equatorTemp, polesTemp) -> None:
        for cell in self._map.values():
            coord = cell.axial_coordinates[0][1]
            temperature = 0
            latitude = coord + axialTilt
            if latitude < 0:
                temperature = utils.numericalLerp(
                    latitude, -self.mapSize[1] / 2, 0, polesTemp, equatorTemp
                ) + 5 * opensimplex.noise2(
                    cell.axial_coordinates[0][0], cell.axial_coordinates[0][1]
                )
            elif latitude >= 0:
                temperature = utils.numericalLerp(
                    latitude, 0, self.mapSize[1] / 2, equatorTemp, polesTemp
                ) + 5 * opensimplex.noise2(
                    cell.axial_coordinates[0][0], cell.axial_coordinates[0][1]
                )
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

    def generateWinds(self):
        for cell in self._map.values():
            cell.calculateWind()

    def generateRivers(self):
        id = 0
        shortRivers = []
        for cell in self._map.values():
            if (
                    cell.elevation > 40
                    and cell.moisture > 90
                    and not cell.hasRiver()
                    and cell.temperature > 0
            ):
                self.rivers.append(HexGenerator.HexRiver.HexRiver(id, cell))
                id = id + 1
        for river in self.rivers:
            if len(river.cells) <= 2:
                shortRivers.append(river)
        for river in shortRivers:
            self.rivers.remove(river)
        print(f"    Generated {len(self.rivers)} rivers")

    def draw(self, rivers=False) -> None:
        for cell in self._map.values():
            cell.draw(rivers)
