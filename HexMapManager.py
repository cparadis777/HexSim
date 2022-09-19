import pygame as pg
from HexMap import HexMap


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
        self.arrowImage = pg.image.load("arrow.jpg").convert_alpha()
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
        self.mode = mode
        for i in list(self.currentMap.values()):
            if self.mode == 1:
                i.setColor(i.biomeColor)
            elif self.mode == 0:
                i.setColor(i.tectonicColor)
        self.queueUpdate()

    def queueUpdate(self):
        self.update_enabled = True

    def update(self):
        if self.update_enabled:
            self.screen.fill((0, 0, 0))
            self.draw()
            self.update_enabled = False

    def draw(self):
        for cell in list(self.currentMap.values()):
            cell.draw()
            self.main_surf.blit(
                cell.image, (cell.get_position()[0] + 500, cell.get_position()[1] + 500)
            )
        for i in self.spritesList:
            self.main_surf.blit(i.image, (i.position[0] + 500, i.position[1] + 500))

    def createMap(self, radius, size, nPlates, ratio):
        self.currentMap = HexMap(radius)
        self.currentMap.createMap(size, nPlates, ratio)
        self.queueUpdate()

    def drawArrows(self):
        for plate in self.currentMap.TectonicPlates:
            for cell in plate.cells:
                currentSprite = arrow(
                    self.arrowImage,
                    (cell.get_position()[0] + 12, cell.get_position()[1] + 15),
                )
                currentSprite.scale((10, 10))
                angle = plate.direction.value * 60
                currentSprite.rotate(angle)
                self.spritesList.append(currentSprite)
