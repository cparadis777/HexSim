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
        hitExistingRiver = False
        while (
                self.cells[-1].elevation > 0
                and self.cells[-1].riverOut is None
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
                elif neighbor.hasRiver():
                    cellToAdd = neighbor
                    chosenDirection = direction
                    hitExistingRiver = True
                elif not hitExistingRiver:
                    differential = currentCell.elevation - neighbor.elevation
                    if differential > greatestGradient:
                        greatestGradient = differential
                        cellToAdd = neighbor
                        chosenDirection = direction

            if cellToAdd is None:
                currentCell.riverEnd = True
                self.end = currentCell
                print("river end")
            else:
                currentCell.riverOut = chosenDirection
                cellToAdd.riverIn.append(chosenDirection.opposite())
                cellToAdd.riverStart = False
                cellToAdd.riverEnd = False
                self.cells.append(cellToAdd)

        self.end = self.cells[-1]
        inDirection = self.end.riverIn[0]

        # if self.end.getNeighbor(inDirection.opposite()).hasRiver() and self.end.getNeighbor(
        #         inDirection.opposite()) is not None:
        #     self.end.riverOut = inDirection.opposite()
        #     self.end.riverEnd = False
        #     hitExistingRiver = True
        #
        # elif self.end.getNeighbor(inDirection.opposite().previous()).hasRiver() and self.end.getNeighbor(
        #         inDirection.opposite().previous()) is not None:
        #     self.end.riverOut = inDirection.opposite().previous()
        #     self.end.riverEnd = False
        #     hitExistingRiver = True
        # elif self.end.getNeighbor(inDirection.opposite().next()).hasRiver() and self.end.getNeighbor(
        #         inDirection.opposite().next()) is not None:
        #     self.end.riverOut = inDirection.opposite().next()
        #     self.end.riverEnd = False
        #     hitExistingRiver = True

        if not hitExistingRiver:
            self.end.riverEnd = True
