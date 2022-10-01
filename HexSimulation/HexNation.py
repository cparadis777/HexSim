class HexNation:
    def __init__(self, color, capital):
        self.color = color
        self.cells = [capital]
        self.capital = capital
        self.borderCells = [capital]
        self.foodStockpile = 0

    def step(self):
        self.gatherRessources()
        self.consumeRessources()
        print(self.foodStockpile)
        if self.foodStockpile > 100:
            self.expand()
            self.foodStockpile = self.foodStockpile % 100

    def gatherRessources(self):
        for cell in self.cells:
            self.foodStockpile += cell.fertility

    def consumeRessources(self):
        for cell in self.cells:
            self.foodStockpile -= 25

    def expand(self):
        currentBorder = self.borderCells
        nextBorder = []
        for cell in currentBorder:
            for neighbor in cell.getNeighbors():
                if neighbor is None:
                    pass
                elif neighbor.nation is not None:
                    pass
                elif neighbor.elevation < 0:
                    pass
                else:
                    neighbor.nation = self
                    nextBorder.append(neighbor)
        self.borderCells = nextBorder
