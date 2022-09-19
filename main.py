import numpy as np
import hexy as hx
from HexCell import HexCell
from random import randint
from HexTectonics import *
from HexDirections import HexDirections
import pygame as pg
import sys
import HexMapManager as hmm

black = (0, 0, 0)
radius = 48
nPlates = 10
ratio = 0.5
tileSize = 6
HexMapManager = hmm.HexMapManager()
HexMapManager.createMap(radius, tileSize, nPlates, ratio)
# HexMapManager.drawArrows()
HexMapManager.queueUpdate()
HexMapManager.setMode(1)

print("starting")


while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_0:
                HexMapManager.setMode(0)
            if event.key == pg.K_1:
                HexMapManager.setMode(1)
            if event.key == pg.K_n:
                HexMapManager.createMap(radius, tileSize, nPlates, ratio)
                HexMapManager.setMode(1)

    HexMapManager.update()

    pg.display.flip()
