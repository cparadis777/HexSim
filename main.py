import sys
from random import seed

import opensimplex
import pygame as pg

import HexMapManager as hmm

###### SETTINGS ######
chosenSeed = 7856876
size = [100, 90]
nPlates = 20
ratio = 0.4
tileSize = 6
zeta = 0.1
nIterationsMoisture = 600
############

###### RUNTIME VARIABLES #########
screenFocus = (0, 0)
originalTileSize = tileSize
black = (0, 0, 0)
seed(chosenSeed)
opensimplex.seed(chosenSeed)
HexMapManager = hmm.HexMapManager()
# HexMapManager.screen.iconify()
HexMapManager.createMap(size, tileSize, nPlates, ratio, zeta, nIterationsMoisture)
HexMapManager.queueUpdate()
HexMapManager.setMode(1)
HexMapManager.setRiverMode(True)
#######

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
                print("mode switch: biomes")
                HexMapManager.setMode(1)
            if event.key == pg.K_3:
                print("mode switch: heightmap")
                HexMapManager.setMode(2)
            if event.key == pg.K_4:
                print("mode switch: temperature")
                HexMapManager.setMode(3)
            if event.key == pg.K_5:
                print("mode switch: moisture")
                HexMapManager.setMode(4)
            if event.key == pg.K_r:
                print("activating rivers")
                if HexMapManager.riverMode:
                    HexMapManager.setRiverMode(False)
                    print("Set rivers false")
                else:
                    HexMapManager.setRiverMode(True)
                    print("Set rivers true")
            if event.key == pg.K_z:
                print("zooming in")
                tileSize = tileSize + 2
                HexMapManager.zoom(tileSize)
            if event.key == pg.K_x:
                if tileSize - 2 < 2:
                    pass
                else:
                    print("zooming out")
                    tileSize = tileSize - 2
                    HexMapManager.zoom(tileSize)
            if event.key == pg.K_n:
                print("Regen")
                HexMapManager.createMap(
                    size, tileSize, nPlates, ratio, zeta, nIterationsMoisture
                )
            if event.key == pg.K_UP:
                screenFocus = (screenFocus[0], screenFocus[1] + tileSize)
                HexMapManager.pan(screenFocus)
            if event.key == pg.K_DOWN:
                screenFocus = (screenFocus[0], screenFocus[1] - tileSize)
                HexMapManager.pan(screenFocus)
            if event.key == pg.K_LEFT:
                screenFocus = (screenFocus[0] + tileSize, screenFocus[1])
                HexMapManager.pan(screenFocus)
            if event.key == pg.K_RIGHT:
                screenFocus = (screenFocus[0] - tileSize, screenFocus[1])
                HexMapManager.pan(screenFocus)
            if event.key == pg.K_c:
                tileSize = originalTileSize
                screenFocus = (0, 0)
                HexMapManager.setView(tileSize, screenFocus)

    HexMapManager.update()

    pg.display.flip()
