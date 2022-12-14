import sys
from random import randint, seed

import opensimplex
import pygame as pg

import HexMapManager as hmm

###### SETTINGS ######
# chosenSeed = 47894561
chosenSeed = randint(0, 99999999)
# size = [150, 100]
size = [40, 30]
nPlates = 5
ratio = 0.4
tileSize = 20
zeta = 0.5
nIterationsMoisture = 600
axialTilt = 3
############

###### RUNTIME VARIABLES #########
screenFocus = (0, 0)
originalTileSize = tileSize
black = (0, 0, 0)
seed(chosenSeed)
opensimplex.seed(chosenSeed)
HexMapManager = hmm.HexMapManager()
HexMapManager.createMap(size, tileSize, nPlates, ratio, zeta, axialTilt, nIterationsMoisture)
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
                    size, tileSize, nPlates, ratio, zeta, axialTilt, nIterationsMoisture
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
            if event.key == pg.K_s:
                print("Initiating simulation")
                HexMapManager.startSim()
            if event.key == pg.K_b:
                print("Toggling borders")
                HexMapManager.toggleBorders()
            if event.key == pg.K_d:
                print("Stepping simulation")
                HexMapManager.stepSimulation()

    HexMapManager.update()

    pg.display.flip()
