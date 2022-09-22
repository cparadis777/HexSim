import pygame as pg
from HexMap import HexMap
import time


class arrow(pg.sprite.Sprite):
    def __init__(self, image, pos):
        super().__init__()
        self.image = image
        self.position = pos
        self.rect = self.image.get_rect(center=pos)

    def scale(self, size):
        self.image = pg.transform.scale(self.image, size)

    def rotate(self, angle):
        """rotate an image while keeping its center"""
        self.image = pg.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)


class HexMapManager:
    def __init__(self):

        self.update_enabled = False
        self.pgInit()
        self.arrowImage = pg.image.load("arrow.png").convert_alpha()
        self.spritesList = []
        self.mode = 0

    def pgInit(self):
        self.height, self.width = 1000, 1000
        self.screenCenter = (self.height / 2, self.width / 2)
        self.screen = pg.display.set_mode((self.height, self.width))
        self.main_surf = None
        self.font = None
        self.clock = None
        self.main_surf = pg.display.set_mode((self.height, self.width))

    def setMode(self, mode):
        # start = time.time()
        if mode == self.mode:
            return
        self.mode = mode
        self.queueUpdate()

    def queueUpdate(self):
        self.update_enabled = True

    def update(self):
        if self.update_enabled:
            self.screen.fill((0, 0, 0))
            self.draw()
            self.update_enabled = False

    def draw(self):
        start = time.time()
        for cell in list(self.currentMap.values()):
            cell.draw(self.mode)
            self.main_surf.blit(
                cell.image, (cell.getPosition()[0], cell.getPosition()[1])
            )
        for i in self.spritesList:
            self.main_surf.blit(i.image, (i.position[0] + 500, i.position[1] + 500))

        stop = time.time()
        print(f"Draw call took {stop-start}s")

    def createMap(self, mapSize, tileSize, nPlates, ratio, zeta):
        self.currentMap = HexMap()
        self.currentMap.createMap(
            mapSize, tileSize, nPlates, ratio, (self.width, self.height), zeta
        )
        self.queueUpdate()

    def drawArrows(self):
        for plate in self.currentMap.tectonicPlates:
            for cell in plate.cells:
                currentSprite = arrow(
                    self.arrowImage,
                    (cell.position[0] + 12, cell.position[1] + 15),
                )
                currentSprite.scale((10, 10))
                angle = plate.direction.value * 60
                currentSprite.rotate(angle)
                self.spritesList.append(currentSprite)
