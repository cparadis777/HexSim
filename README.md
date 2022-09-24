# HexSim

HexSim (name pending) is a hex-based world generator using Python and PyGame.
This is a very rough work in progress, and should not be expected to be fast, polished bug free or working in it's
current state.

## Features overview

- Deterministic seed-based generation.
- Tectonic-based landmass generation
- Humidity simulation using elevation and wind currents.
- River generation based on humidity and elevation.
- Biome generation based on humidity, temperature and elevation

## Usage

Settings for map generation are modified in the main.py file:

- ChosenSeed controls the seed used for generation
- size is the dimension in cells of the map
- nPlates is the number of tectonic plates generated
- ratio is the ratio of continental plates to the total number of tectonic plates
- tileSize is the radius of the hex cells in pixels
- zeta is the transmission factor for tectonic deformation propagation. 0 <= zeta < 1
- nIterationsMoisture is the number of iterations to run for the humidity propagation routine.

Basic controls are offered:

- Arrow keys to pan the view
- Z and X to zoom in and zoom out
- N to regenerate a new map using the same settings
- Number keys for changing views
    - 1: Biomes view
    - 2: Tectonic plates view
    - 3: Elevation view
    - 4: Humidity view
- R to toggle rivers