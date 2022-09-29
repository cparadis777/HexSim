import time

import pygame as pg

from HexMap import HexMap
from HexSimulation.HexSimulator import HexSimulator


class HexMapManager:
    def __init__(self) -> None:

        self.update_enabled = False
        self.pgInit()
        self.spritesList = []
        self.mode = 0
        self.riverMode = False
        self.tileSize = None
        self.center = (0, 0)
        self.currentMap = None
        self.simulator = HexSimulator(self.currentMap)

    def pgInit(self) -> None:
        self.width, self.height = 1200, 1000
        self.screenCenter = (self.width / 2, self.height / 2)
        self.screen = pg.display.set_mode((self.width, self.height))
        self.main_surf = None
        self.font = None
        self.clock = None
        self.main_surf = pg.display.set_mode((self.width, self.height))

    def setMode(self, mode) -> None:
        # start = time.time()
        if mode == self.mode:
            return
        self.mode = mode
        self.queueUpdate()

    def setRiverMode(self, mode: bool) -> None:
        if self.riverMode != mode:
            self.riverMode = mode
            self.queueUpdate()

    def queueUpdate(self) -> None:
        print("queued update")
        self.update_enabled = True

    def update(self) -> None:
        if self.update_enabled:
            self.screen.fill((0, 0, 0))
            self.draw()
            self.update_enabled = False
            print("updated")

    def draw(self) -> None:
        start = time.time()
        for cell in list(self.currentMap.values()):
            cell.draw(self.mode, self.riverMode, radius=self.tileSize)
            self.main_surf.blit(
                cell.image, (cell.getPosition()[0] + self.center[0], cell.getPosition()[1] + self.center[1])
            )
        stop = time.time()
        print(f"Draw call took {stop - start}s")

    def zoom(self, newtileSize: int) -> None:
        self.tileSize = newtileSize
        self.queueUpdate()

    def pan(self, newCenter: tuple[int, int]) -> None:
        if newCenter == self.center:
            pass
        else:
            self.center = newCenter
        self.queueUpdate()

    def setView(self, newTileSize: int, newCenter: tuple[int, int]) -> None:
        self.pan(newCenter)
        self.zoom(newTileSize)

    def createMap(
            self, mapSize: list[int, int], tileSize: int, nPlates: int, ratio: float, zetaTectonics: float,
            axialTilt: int, nIterationsMoisture: int
    ) -> None:
        self.currentMap = HexMap()
        self.tileSize = tileSize
        self.currentMap.createMap(
            mapSize,
            tileSize,
            nPlates,
            ratio,
            (self.width, self.height),
            zetaTectonics,
            axialTilt,
            nIterationsMoisture
        )
        self.queueUpdate()
