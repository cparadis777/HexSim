from enum import Enum


class HexDirection(Enum):
    W = 0
    NW = 1
    NE = 2
    E = 3
    SE = 4
    SW = 5

    def distance(self, direction: "HexDirection") -> int:
        distanceCenter = abs(self.value - direction.value)
        distanceLeft = abs(self.value - 6 - direction.value)
        distanceRight = abs(self.value + 6 - direction.value)
        distance = min(distanceCenter, distanceLeft, distanceRight)

        return distance

    def next(self):
        if self == HexDirection.SW:
            return HexDirection.W
        else:
            return HexDirection(self.value + 1)

    def previous(self):
        if self == HexDirection.W:
            return HexDirection.SW
        else:
            return HexDirection(self.value - 1)

    def opposite(self):
        match self:
            case HexDirection.W:
                return HexDirection.E
            case HexDirection.NW:
                return HexDirection.SE
            case HexDirection.NE:
                return HexDirection.SW
            case HexDirection.E:
                return HexDirection.W
            case HexDirection.SE:
                return HexDirection.NW
            case HexDirection.SW:
                return HexDirection.NE
