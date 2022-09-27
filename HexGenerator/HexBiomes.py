import utils


def mountainBiomes(cell):
    if cell.temperature <= 0:
        cell.biome = "Glacier"
        cell.setBiomeColor((204, 202, 202))
    elif cell.temperature > 0:
        cell.biome = "Mountain"
        cell.setBiomeColor((166, 172, 173))


def oceanBiomes(cell):
    color = utils.colorLerp(cell.elevation, -100, 0, (0, 31, 179), (0, 45, 255))
    cell.biome = "Ocean"
    cell.setBiomeColor(color)


def borealBiomes(cell):
    if cell.moisture > 50:
        cell.biome = "Boreal Forest"
        cell.setBiomeColor((110, 180, 131))
    elif cell.moisture <= 50:
        cell.biome = "Tundra"
        cell.setBiomeColor((186, 214, 165))


def polarBiomes(cell):
    cell.biome = "Polar Desert"
    cell.setBiomeColor((227, 227, 227))


def tropicalBiomes(cell):
    if cell.moisture >= 50:
        cell.biome = "Tropical Rain Forest"
        cell.setBiomeColor((29, 174, 0))
    elif 25 < cell.moisture < 50:
        cell.biome = "Tropical Desert"
        cell.setBiomeColor((189, 212, 36))
    elif cell.moisture <= 25:
        cell.biome = "Arid Desert"
        cell.setBiomeColor((246, 239, 0))


def temperateBiomes(cell):
    if cell.moisture > 50:
        cell.biome = "Temperate Wet Forest"
        cell.setBiomeColor((34, 194, 2))
    if cell.moisture <= 50:
        cell.biome = "Temperate Dry Forest"
        cell.setBiomeColor((50, 192, 58))
