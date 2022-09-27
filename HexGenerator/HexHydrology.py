import utils
from . import HexDirection


def propagateMoisture(cells: list) -> list:
    frontier = []
    for cell in cells:
        for direction in HexDirection.HexDirection:
            neighbor = cell.getNeighbor(direction)
            if neighbor is None:
                pass
            elif neighbor.elevation > 0:
                windFactors = [1, 0.8, 0.3, 0]
                windComponent = cell.windDirection.distance(direction)
                windFactor = windFactors[windComponent]

                deltaElevation = neighbor.elevation - cell.elevation
                elevationFactor = 1
                if deltaElevation <= 0:
                    elevationFactor = 1
                elif deltaElevation > 0:
                    elevationFactor = utils.numericalLerp(deltaElevation, 0, 50, 1, 0)

                moistureToPropagate = (
                        1 * cell.moisture * windFactor + 0 * cell.moisture * elevationFactor
                )
                if neighbor.moisture < moistureToPropagate:
                    neighbor.moisture = moistureToPropagate
                    if neighbor not in frontier:
                        frontier.append(neighbor)
    return frontier
