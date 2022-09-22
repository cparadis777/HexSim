from hexy.hex_tile import HexTile
import numpy as np
import hexy as hx
from HexDirections import HexDirections
import pygame as pg

# from random import randint
from HexPlate import TectonicPlate


def makeHexSurface(
    color, radius, border_color=(100, 100, 100), border=False, hollow=False
):
    """
    Draws a hexagon with gray borders on a pygame surface.
    :param color: The fill color of the hexagon.
    :param radius: The radius (from center to any corner) of the hexagon.
    :param border_color: Color of the border.
    :param border: Draws border if True.
    :param hollow: Does not fill hex with color if True.
    :return: A pygame surface with a hexagon drawn on it
    """
    angles_in_radians = np.deg2rad([60 * i + 30 for i in range(6)])
    x = radius * np.cos(angles_in_radians)
    y = radius * np.sin(angles_in_radians)
    points = np.round(np.vstack([x, y]).T)

    sorted_x = sorted(points[:, 0])
    sorted_y = sorted(points[:, 1])
    minx = sorted_x[0]
    maxx = sorted_x[-1]
    miny = sorted_y[0]
    maxy = sorted_y[-1]

    sorted_idxs = np.lexsort((points[:, 0], points[:, 1]))

    surf_size = np.array((maxx - minx, maxy - miny)) * 2 + 1
    center = surf_size / 2
    surface = pg.Surface(surf_size)
    surface.set_colorkey((0, 0, 0))

    # Set alpha if color has 4th coordinate.
    if len(color) >= 4:
        surface.set_alpha(color[-1])

    # fill if not hollow.
    if not hollow:
        pg.draw.polygon(surface, color, points + center, 0)

    points[sorted_idxs[-1:-4:-1]] += [0, 1]
    # if border is true or hollow is true draw border.
    if border or hollow:
        pg.draw.lines(surface, border_color, True, points + center, 1)

    return surface


class HexCell(HexTile):
    def __init__(
        self, axial_coordinates, radius, elevation, tile_id, hexMap, screensize
    ):
        super().__init__(axial_coordinates, radius, tile_id)
        self.axial_coordinates = np.array([axial_coordinates])
        self.cube_coordinates = hx.axial_to_cube(self.axial_coordinates)
        self.position = hx.axial_to_pixel(self.axial_coordinates, radius)
        self.position = (
            self.position[0][0] + screensize[0] / 2,
            self.position[0][1] + screensize[0] / 2,
        )
        self.corners = None
        self.colors = [None, None, None, None, None, None]
        self.tectonicColor = None
        self.tectonicActivity = 0
        self.biomeColor = None
        self.tectonicPlate = None
        self.hexMap = hexMap
        self.elevation = elevation
        self.temperature = 0
        self.windDirection = None
        self.setCorners()

    def draw(self, mode):
        self.image = makeHexSurface(self.colors[mode], self.radius)

    def setCorners(self):
        angles_in_radians = np.deg2rad([60 * i + 30 for i in range(6)])
        x = self.radius * np.cos(angles_in_radians) + self.getPosition()[0]
        y = self.radius * np.sin(angles_in_radians) + self.getPosition()[1]
        points = np.round(np.vstack([x, y]).T)
        self.corners = points
        self.setEdges()

    def setEdges(self):
        self.edges = [
            (self.corners[0], self.corners[1]),
            (self.corners[1], self.corners[2]),
            (self.corners[2], self.corners[3]),
            (self.corners[3], self.corners[4]),
            (self.corners[4], self.corners[5]),
            (self.corners[5], self.corners[0]),
        ]

    def setTectonicColor(self, color) -> None:
        self.tectonicColor = color
        self.colors[0] = color
        # print(f"{self.colors[0]}, {self.getTectonicPlate().color}")

    def setBiomeColor(self, color) -> None:
        self.biomeColor = color
        self.colors[1] = color

    def setTectonicPlate(self, plate: TectonicPlate) -> None:
        self.tectonicPlate = plate

    def setHexMap(self, hexMap) -> None:
        self.hexMap = hexMap

    def setElevation(self, elevation) -> None:
        self.elevation = elevation

    def setTemperature(self, temperature) -> None:
        self.temperature = temperature

    def setTemperatureColor(self, color) -> None:
        self.colors[3] = color

    def setWindDirection(self, direction: HexDirections) -> None:
        self.windDirection = direction

    def getEdge(self, direction: int):
        return self.edges[direction]

    def getPosition(self):
        return self.position

    def getTectonicPlate(self) -> TectonicPlate:
        return self.tectonicPlate

    def setNeighbors(self) -> None:
        self.neighbors = self.getNeighbors()

    def getNeighbors(self):
        neighbors = []
        for direction in HexDirections:
            neighbor = self.getNeighbor(direction)
            neighbors.append(neighbor)
        return neighbors

    def setTectonicActivity(self, activity) -> None:
        self.tectonicActivity = activity

    def getTectonicActivity(self) -> int:
        return self.tectonicActivity

    def setHeightColor(self, color) -> None:
        self.colors[2] = color

    def getNeighbor(self, direction) -> HexTile:
        SE = np.array((1, 0, -1))
        SW = np.array((0, 1, -1))
        W = np.array((-1, 1, 0))
        NW = np.array((-1, 0, 1))
        NE = np.array((0, -1, 1))
        E = np.array((1, -1, 0))
        ALL_DIRECTIONS = np.array(
            [
                NW,
                NE,
                E,
                SE,
                SW,
                W,
            ]
        )

        neighborCoord = hx.get_neighbor(
            self.cube_coordinates, ALL_DIRECTIONS[direction.value]
        )

        neighborCoord = hx.cube_to_axial(neighborCoord)

        neighborCoord = f"{neighborCoord[0][0]},{neighborCoord[0][1]}"
        try:
            neighbor = self.hexMap._map[neighborCoord]
        except Exception:
            neighbor = None
        return neighbor
