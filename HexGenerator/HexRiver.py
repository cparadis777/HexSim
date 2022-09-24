from . import HexDirection


class HexRiver:
    def __init__(self, id, source):
        self.surfaceCenter = None
        self.image = None
        self.id = id
        self.source = source
        self.cells = [source]
        self.source.riverStart = True
        self.flow()

    def flow(self):
        print("     Started flowing river")
        while (
                self.cells[-1].elevation > 0
                and self.cells[-1].riverOut is None
                and not self.cells[-1].riverEnd
        ):
            currentCell = self.cells[-1]
            greatestGradient = 0
            cellToAdd = None
            chosenDirection = None
            for direction in HexDirection.HexDirection:

                neighbor = currentCell.getNeighbor(direction)
                if neighbor is None:
                    pass
                else:
                    differential = currentCell.elevation - neighbor.elevation
                    if differential > greatestGradient:
                        greatestGradient = differential
                        cellToAdd = neighbor
                        chosenDirection = direction

            if cellToAdd is None:
                currentCell.riverEnd = True
            else:
                currentCell.riverOut = chosenDirection
                cellToAdd.riverStart = False
                self.cells.append(cellToAdd)
                self.cells[-1].riverIn.append(chosenDirection.opposite())
            print(f"         Current River {self.id} is {len(self.cells)} cells")

        self.cells[-1].riverEnd = True
        print("     Stopped Flowing river")
