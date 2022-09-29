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


"""
    def flow(self):
        hitExistingRiver = False
        lowestCell = False
        while (
                self.cells[-1].elevation > 0
                and not lowestCell
                # and self.cells[-1].riverOut is None
                and not self.cells[-1].riverEnd
                and not hitExistingRiver
        ):
            currentCell = self.cells[-1]
            greatestGradient = -10
            cellToAdd = None
            chosenDirection = None
            for direction in HexDirection.HexDirection:

                neighbor = currentCell.getNeighbor(direction)
                if neighbor is None:
                    pass
                elif not hitExistingRiver:
                    differential = currentCell.elevation - neighbor.elevation
                    if differential > greatestGradient:
                        greatestGradient = differential
                        cellToAdd = neighbor
                        chosenDirection = direction

            currentElevation = currentCell.elevation
            lowestCell = any(currentElevation < neighbor.elevation for neighbor in currentCell.getNeighbors() if
                             neighbor is not None)
            if lowestCell:
                currentCell.riverEnd = True
                self.end = currentCell
                print("river end")
            else:
                currentCell.riverOut = chosenDirection
                cellToAdd.riverIn.append(chosenDirection.opposite())
                cellToAdd.riverStart = False
                cellToAdd.riverEnd = False
                self.cells.append(cellToAdd)

                print(f"\r    {len(self.cells)} cells flowed", end="")
            print(
                f"\r     {len(self.cells)} cells flowed"
            )
        self.end = self.cells[-1]

        if not hitExistingRiver:
            self.end.riverEnd = True
        print("Done Flowing")
"""
