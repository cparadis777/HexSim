import numpy as np
import hexy as hx
from HexCell import HexCell
from random import randint
from HexTectonics import *
from HexDirections import HexDirections
import pygame as pg
import sys
import HexMapManager as hmm
import HexTectonics


#sys.setrecursionlimit(300)
black = (0, 0, 0)
size = [60, 40]
nPlates = 15
ratio = 0.3
tileSize = 12
HexMapManager = hmm.HexMapManager()
HexMapManager.createMap(size, tileSize, nPlates, ratio)
# HexMapManager.drawArrows()
HexMapManager.queueUpdate()
HexMapManager.setMode(1)

HexTectonics.getCollisionType(
    HexMapManager.currentMap.tectonicPlates[0],
    HexMapManager.currentMap.tectonicPlates[
        HexMapManager.currentMap.tectonicPlates[0].neighboringPlates[0]
    ],
)
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
                HexMapManager.createMap(size, tileSize, nPlates, ratio)

    HexMapManager.update()

    pg.display.flip()
