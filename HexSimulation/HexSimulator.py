from random import randint

import pygame as pg

from utils import randomColor
from . import HexNation


class HexBorder(pg.sprite.Sprite):
    def __init__(self, pos, color):
        super().__init__()
        self.image = pg.image.load(r".\HexSimulation\HexagonBorder.png")
        self.colorImage = pg.Surface(self.image.get_size()).convert_alpha()
        self.colorImage.fill(color)
        self.scale((10, 10))
        self.position = (pos[0], pos[1])
        self.rect = self.image.get_rect(center=pos)

    def scale(self, size):
        self.image = pg.transform.scale(self.image, size)

    def rotate(self, angle):
        """rotate an image while keeping its center"""
        self.image = pg.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def draw(self, ):
        self.image.blit(self.colorImage, (0, 0), special_flags=pg.BLEND_RGBA_MULT)


class HexSimulator:
    def __init__(self, HexMap):
        self.map = HexMap
        self.nations = {}
        self.started = False
        self.borders = pg.sprite.Group()

    def start(self):
        if not self.started:
            self.started = True
            self.createNations(10)
            print("nations created")

    def createNations(self, n):
        for i in range(n):
            index = randint(0, len(self.map._map.values()) - 1)
            color = randomColor()
            if list(self.map._map.values())[index].elevation > 1:
                self.nations[i] = HexNation.HexNation(color, list(self.map._map.values())[index])
                list(self.map._map.values())[index].nation = self.nations[i]

    def step(self):
        for nation in self.nations.values():
            nation.step()
