import sys
from random import seed

import opensimplex
import pygame as pg

import HexMapManager as hmm

chosenSeed = 1234
seed(chosenSeed)
opensimplex.seed(chosenSeed)
black = (0, 0, 0)
size = [200, 180]
# size = [40]
nPlates = 50
ratio = 0.3
tileSize = 2
zeta = 0.6
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
            if event.key == pg.K_2:
                print("mode switch: tectonics")
                HexMapManager.setMode(0)
            if event.key == pg.K_1:
                print("monde switch: biomes")
                HexMapManager.setMode(1)
            if event.key == pg.K_3:
                print("monde switch: heightmap")
                HexMapManager.setMode(2)
            if event.key == pg.K_4:
                print("monde switch: temperature")
                HexMapManager.setMode(3)
            if event.key == pg.K_n:
                print("Regen")
                HexMapManager.createMap(size, tileSize, nPlates, ratio, zeta)

    HexMapManager.update()

    pg.display.flip()
