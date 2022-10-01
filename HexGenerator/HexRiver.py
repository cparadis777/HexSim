from . import HexDirection


class HexRiver:
    def __init__(self, id: int, source):
        self.surfaceCenter = None
        self.image = None
        self.id = id
        self.source = source
        self.end = None
        self.cells = [source]
        self.source.riverStart = True
        self.source.moisture = self.source.moisture + 20
        self.flow()

    def flow(self):
        stopFlow = False
        while not stopFlow:
            currentCell = self.cells[-1]
            greatestGradient = 0
            cellToAdd = None
            currentDirection = None
            for direction in HexDirection.HexDirection:
                neighbor = currentCell.getNeighbor(direction)
                if neighbor is not None:
                    gradient = currentCell.elevation - neighbor.elevation
                    if gradient > greatestGradient:
                        greatestGradient = gradient
                        cellToAdd = neighbor
                        currentDirection = direction

            if cellToAdd is None:
                stopFlow = True
            else:
                currentCell.riverOut = currentDirection
                cellToAdd.riverIn.append(currentDirection.opposite())
                cellToAdd.riverStart = False
                cellToAdd.riverEnd = False
                self.cells.append(cellToAdd)
                cellToAdd.moisture = cellToAdd.moisture + 20
                if cellToAdd.elevation <= 0:
                    stopFlow = True
        self.end = self.cells[-1]
        self.end.riverEnd = True
