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


black = (0, 0, 0)
size = [100, 80]
# size = [40]
nPlates = 50
ratio = 0.5
tileSize = 4
zeta = 0.3
HexMapManager = hmm.HexMapManager()
HexMapManager.createMap(size, tileSize, nPlates, ratio, zeta)
HexMapManager.queueUpdate()
HexMapManager.setMode(1)


print("starting")
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_0:
                print("mode switch")
                HexMapManager.setMode(0)
            if event.key == pg.K_1:
                print("monde switch")
                HexMapManager.setMode(1)
            if event.key == pg.K_2:
                print("monde switch")
                HexMapManager.setMode(2)
            if event.key == pg.K_a:
                HexMapManager.drawArrows()
            if event.key == pg.K_n:
                print("Regen")
                HexMapManager.createMap(size, tileSize, nPlates, ratio, zeta)

    HexMapManager.update()

    pg.display.flip()
