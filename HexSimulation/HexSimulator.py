from random import randint

import pygame as pg

from utils import randomColor
from . import HexNation


class HexBorder(pg.sprite.Sprite):
    def __init__(self, pos, color):
        super().__init__()
        self.image = pg.image.load("HexagonBorder.png")
        self.colorImage = pg.Surface(self.image.get_size().convert_alpha())
        self.colorImage.fill(color)
        self.position = pos
        self.rect = self.image.get_rect(center=pos)
        self.draw()

    def scale(self, size):
        self.image = pg.transform.scale(self.image, size)

    def rotate(self, angle):
        """rotate an image while keeping its center"""
        self.image = pg.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def draw(self):
        self.image.blit(self.colorImage, (0, 0), special_flags=pg.BLEND_RGBA_MULT)


class HexSimulator:
    def __init__(self, HexMap):
        self.map = HexMap
        self.nations = {}

    def createNations(self, n):
        for i in range(n):
            index = randint(0, len(self.map._map.values()) - 1)
            color = randomColor()
            self.nations[i] = HexNation.HexNation(color)

    def drawBorders(self):
        for nation in self.nations.values():
            for cell in nation.cells:
                HexBorder(cell.getPosition(), nation.color)
