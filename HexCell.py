import hexy as hx
import numpy as np
import pygame as pg
from hexy.hex_tile import HexTile

from HexGenerator.HexDirection import HexDirection
# from random import randint
from HexPlate import TectonicPlate


class HexCell(HexTile):
    def __init__(
            self, axial_coordinates, radius, elevation, tile_id, hexMap, screensize
    ):
        super().__init__(axial_coordinates, radius, tile_id)
        self.border = None
        self.screensize = screensize
        self.axial_coordinates = np.array([axial_coordinates])
        self.cube_coordinates = hx.axial_to_cube(self.axial_coordinates)
        self.position = hx.axial_to_pixel(self.axial_coordinates, radius)
        self.position = (
            self.position[0][0] + screensize[0] / 2,
            self.position[0][1] + screensize[0] / 2,
        )
        self.neighbors = []
        self.corners = None
        self.edges = None
        self.image = None
        self.colors = [(125, 125, 125) for i in range(5)]
        self.tectonicColor = None
        self.tectonicActivity = 0
        self.biomeColor = None
        self.tectonicPlate = None
        self.hexMap = hexMap
        self.elevation = elevation
        self.temperature = 0
        self.windDirection = None
        self.windSpeed = 0
        self.moisture = 0
        self.riverStart = False
        self.riverEnd = False
        self.riverIn = []
        self.riverOut = None
        self.biome = None
        self.fertility = 0
        self.nation = None
        self.setCorners()

    def draw(self, mode, riverMode, radius=None, border=False, borderColor=None):
        if radius is None:
            radius = self.radius
        else:
            self.radius = radius
            self.position = hx.axial_to_pixel(self.axial_coordinates, radius)
            self.position = (
                self.position[0][0] + self.screensize[0] / 2,
                self.position[0][1] + self.screensize[1] / 2,
            )
        if border:
            self.image = self.makeHexSurface(self.colors[mode], self.radius, riverMode, border=border,
                                             border_color=borderColor)
        else:
            self.image = self.makeHexSurface(self.colors[mode], self.radius, riverMode)

    def setCorners(self):
        angles_in_radians = np.deg2rad([60 * i + 30 for i in range(6)])
        x = self.radius * np.cos(angles_in_radians) + self.getPosition()[0]
        y = self.radius * np.sin(angles_in_radians) + self.getPosition()[1]
        points = np.round(np.vstack([x, y]).T)
        self.corners = points
        self.setEdges()

    def setEdges(self):
        # Weird order to make the order of edges coherent with the order of HexDirections
        self.edges = [
            (self.corners[3], self.corners[2]),
            (self.corners[4], self.corners[3]),
            (self.corners[5], self.corners[4]),
            (self.corners[0], self.corners[5]),
            (self.corners[1], self.corners[0]),
            (self.corners[2], self.corners[1]),
        ]

    def setTectonicColor(self, color) -> None:
        self.tectonicColor = color
        self.colors[0] = color
        # print(f"{self.colors[0]}, {self.getTectonicPlate().color}")

    def setBiomeColor(self, color) -> None:
        self.biomeColor = color
        self.colors[1] = color

    def setMoistureColor(self, color):
        self.colors[4] = color

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

    def setWindDirection(self, direction: HexDirection) -> None:
        self.windDirection = direction

    def calculateWind(self):
        maxDifferential = -100
        maxDifferentialDirection = HexDirection.E
        for direction in HexDirection:
            if self.getNeighbor(direction) is not None:
                differential = (
                        self.temperature - self.getNeighbor(direction).temperature
                )
                if differential > maxDifferential:
                    maxDifferential = differential
                    maxDifferentialDirection = direction

        if self.getNeighbor(maxDifferentialDirection).elevation > 90:
            lowestNeighbor = maxDifferentialDirection
            lowestElevation = self.getNeighbor(maxDifferentialDirection).elevation
            if self.getNeighbor(maxDifferentialDirection.next()) is not None:
                if self.getNeighbor(maxDifferentialDirection.next()).elevation < lowestElevation:
                    lowestNeighbor = maxDifferentialDirection.next()
                    lowestElevation = self.getNeighbor(maxDifferentialDirection.next()).elevation
            if self.getNeighbor(maxDifferentialDirection.previous()) is not None:
                if self.getNeighbor(maxDifferentialDirection.previous()).elevation < lowestElevation:
                    lowestNeighbor = maxDifferentialDirection.previous()
                    lowestElevation = self.getNeighbor(maxDifferentialDirection.previous())
            maxDifferentialDirection = lowestNeighbor
            maxDifferential = self.temperature - self.getNeighbor(maxDifferentialDirection).temperature

        self.windDirection = maxDifferentialDirection
        self.windSpeed = maxDifferential

    def getEdge(self, direction: int):
        return self.edges[direction]

    def getPosition(self):
        return self.position

    def getTectonicPlate(self) -> TectonicPlate:
        return self.tectonicPlate

    def setNeighbors(self) -> None:
        self.neighbors = []
        for direction in HexDirection:
            self.neighbors.append(self.calculateNeighbor(direction))
        self.neighbors = self.getNeighbors()

    def getNeighbors(self):
        return self.neighbors

    def getNeighbor(self, direction):
        return self.neighbors[direction.value]

    def setTectonicActivity(self, activity) -> None:
        self.tectonicActivity = activity

    def getTectonicActivity(self) -> int:
        return self.tectonicActivity

    def setHeightColor(self, color) -> None:
        self.colors[2] = color

    def hasRiver(self) -> bool:
        if (
                self.riverEnd
                or self.riverStart
                or self.riverOut is not None
                or len(self.riverIn) != 0
        ):
            return True
        else:
            return False

    def calculateNeighbor(self, direction) -> HexTile:
        SE = np.array((1, 0, -1))
        SW = np.array((0, 1, -1))
        W = np.array((-1, 1, 0))
        NW = np.array((-1, 0, 1))
        NE = np.array((0, -1, 1))
        E = np.array((1, -1, 0))
        ALL_DIRECTIONS = np.array([W, NW, NE, E, SE, SW])

        neighborCoord = hx.get_neighbor(
            self.cube_coordinates, ALL_DIRECTIONS[direction.value]
        )

        neighborCoord = hx.cube_to_axial(neighborCoord)

        neighborCoord = f"{neighborCoord[0][0]},{neighborCoord[0][1]}"
        try:
            neighbor = self.hexMap._map[neighborCoord]
        except Exception:
            neighbor = None
            """"
            offsetCoord = utils.axial_to_offset(self.axial_coordinates)
            neighborOffset = np.array([[offsetCoord[0][0], offsetCoord[0][1]]])
            neighborOffset[0][0] = -1 * neighborOffset[0][0]
            match direction:
                case HexDirection.NE:
                    neighborOffset[0][1] = neighborOffset[0][1] - 1
                case HexDirection.NW:
                    neighborOffset[0][1] = neighborOffset[0][1] - 1
                case HexDirection.SE:
                    neighborOffset[0][1] = neighborOffset[0][1] + 1
                case HexDirection.SW:
                    neighborOffset[0][1] = neighborOffset[0][1] + 1
                case _:
                    pass
            try:
                neighborCoord = utils.offset_to_axial(neighborOffset)
                neighborCoord = hx.axial_to_cube(neighborCoord)
                neighborCoord = f"{neighborCoord[0][0]},{neighborCoord[0][1]}"
                neighbor = self.hexMap._map[neighborCoord]
            except Exception:
                neighbor = None
        """
        return neighbor

    def makeHexSurface(
            self,
            color,
            radius,
            riverMode=False,
            border_color=(100, 100, 100),
            border=False,
            hollow=False,
    ):
        """
        Draws a hexagon with gray borders on a pygame surface.
        :param self:
        :param color: The fill color of the hexagon.
        :param radius: The radius (from center to any corner) of the hexagon.
        :param riverMode: Whether to draw rivers on the surface
        :param border_color: Color of the border.
        :param border: Draws border if True.
        :param hollow: Does not fill hex with color if True.
        :return: A pygame surface with a hexagon drawn on it
        """
        angles_in_radians = np.deg2rad([60 * i + 30 for i in range(6)])
        x = radius * np.cos(angles_in_radians)
        y = radius * np.sin(angles_in_radians)
        x_border = radius * 0.9 * np.cos(angles_in_radians)
        y_border = radius * 0.9 * np.sin(angles_in_radians)

        points = np.round(np.vstack([x, y]).T)
        points = np.flipud(points)
        points = np.roll(points, -2, 0)

        points_border = np.round(np.vstack([x_border, y_border]).T)
        points_border = np.flipud(points_border)
        points_border = np.roll(points_border, -2, 0)

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
            for i, neighbor in enumerate(self.neighbors):
                if neighbor is None:
                    pass
                elif neighbor.nation == self.nation:
                    pass
                else:
                    if i == 5:
                        index = 0
                    else:
                        index = i + 1
                    pg.draw.line(surface, border_color, points_border[i] + center, points_border[index] + center,
                                 max(round(radius * 0.1), 5))

            # pg.draw.lines(surface, border_color, True, points_border + center, max(round(radius * 0.1), 2))

        if riverMode:
            self.drawRiver(points, surface, center, radius)
        return surface

    def drawRiver(self, points, surface, center, radius):
        if self.hasRiver():
            if self.riverStart:
                pass
                # pg.draw.circle(surface, (50, 50, 255), center, radius / 2)

            if self.riverOut is None:
                pass
                # pg.draw.circle(surface, (0, 0, 255), center, radius / 2.5)

            else:
                outgoingEdge = None
                match self.riverOut:
                    case HexDirection.W:
                        outgoingEdge = (points[0, :], points[1, :])
                    case HexDirection.NW:
                        outgoingEdge = (points[1, :], points[2, :])
                    case HexDirection.NE:
                        outgoingEdge = (points[2, :], points[3, :])
                    case HexDirection.E:
                        outgoingEdge = (points[3, :], points[4, :])
                    case HexDirection.SE:
                        outgoingEdge = (points[4, :], points[5, :])
                    case HexDirection.SW:
                        outgoingEdge = (points[5, :], points[0, :])
                    case _:
                        raise ValueError("Invalid direction")

                endPoint = (
                    (outgoingEdge[0][0] + outgoingEdge[1][0]) / 2,
                    (outgoingEdge[0][1] + outgoingEdge[1][1]) / 2,
                )
                endPoint = (endPoint[0] + center[0], endPoint[1] + center[1])
                pg.draw.line(surface, (0, 0, 255), center, endPoint, 3)

            if len(self.riverIn) != 0:
                for incomingRiverDirection in self.riverIn:
                    incomingEdge = None
                    match incomingRiverDirection:
                        case HexDirection.W:
                            incomingEdge = (points[0, :], points[1, :])
                        case HexDirection.NW:
                            incomingEdge = (points[1, :], points[2, :])
                        case HexDirection.NE:
                            incomingEdge = (points[2, :], points[3, :])
                        case HexDirection.E:
                            incomingEdge = (points[3, :], points[4, :])
                        case HexDirection.SE:
                            incomingEdge = (points[4, :], points[5, :])
                        case HexDirection.SW:
                            incomingEdge = (points[5, :], points[0, :])
                        case _:
                            raise ValueError("Invalid direction")
                    startPoint = (
                        (incomingEdge[0][0] + incomingEdge[1][0]) / 2,
                        (incomingEdge[0][1] + incomingEdge[1][1]) / 2,
                    )
                    startPoint = (startPoint[0] + center[0], startPoint[1] + center[1])
                    pg.draw.line(surface, (0, 0, 255), startPoint, center, 3)
