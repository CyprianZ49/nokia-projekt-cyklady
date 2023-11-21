from bot import Bot

class MetropilsAlreadyPresent(Exception):
    pass

class InvalidBuildingSlot(Exception):
    pass

class AttemptedBuildingOnNotOwnedTile(Exception):
    pass

class TryingToBuildOnWater(Exception):
    pass

class Water:
    def __init__(self, x, y, value, owner):
        self.x=x
        self.y=y
        self.value=value
        self.owner=owner
        self.typ='water'
        self.strength=0
    def increaseValue(self):
        self.value+=1
    def changeOwner(self, newOwner):
        self.owner.ownedTiles.remove([self.x, self.y])
        newOwner.ownedTiles.add([self.x, self.y])
        self.owner=newOwner

class Void:
    def __init__(self, x, y):
        self.x=x
        self.y=y
        self.typ='void'

class Island:
    def __init__(self, x, y, capital):
        self.x=x
        self.y=y
        self.capital=capital
        self.typ='island'

class Capital:
    def __init__(self, x, y, value, owner, maxBuildings, territory):
        self.x=x
        self.y=y
        self.value=value
        self.owner=owner
        self.isMetropolis=False
        self.buildings=['plains' for i in range(maxBuildings)]
        self.territory=territory
        self.typ='capital'
        self.strength=0
    def increaseValue(self):
        self.value+=1
    def build(self, building, slot):
        if(slot>=len(self.buildings)):
            raise InvalidBuildingSlot
        self.buildings[slot]=building
    def buildMetropolis(self):
        if self.isMetropolis:
            raise MetropilsAlreadyPresent
        self.isMetropolis=True
        self.buildings=self.buildings[:-2]
    def changeOwner(self, newOwner):
        self.owner.ownedTiles.remove([self.x, self.y])
        newOwner.ownedTiles.add([self.x, self.y])
        self.owner=newOwner

class Plansza:
    def __init__(self):
        self.pola=[[]]
    def generateBoard(self):
        for x in range(13):
            self.pola.append([])
            for y in range(13):
                self.pola[x].append(Void(x, y))
        for y in range(7):
            for x in range(7+y):
                self.pola[x][y]=Water(x, y, 0, -1)
        for y in range(7, 13):
            for x in range(y-6, 13):
                self.pola[x][y]=Water(x, y, 0, -1)
        self.pola[1][1].increaseValue()
        self.pola[6][1].increaseValue()
        self.pola[1][6].increaseValue()
        self.pola[11][6].increaseValue()
        self.pola[6][11].increaseValue()
        self.pola[11][11].increaseValue()

        self.pola[2][2]=Island(2, 2, [3, 3])
        self.pola[3][2]=Island(3, 2, [3, 3])
        self.pola[3][3]=Capital(3, 3, 0, -1, 3, [[2, 2], [3, 2], [3, 3]])

        self.pola[1][4]=Island(1, 4, [2, 4])
        self.pola[1][5]=Island(1, 5, [2, 4])
        self.pola[2][4]=Capital(2, 4, 0, -1, 3, [[1, 4], [1, 5], [2, 4]])

        self.pola[5][1]=Island(5, 1, [5, 3])
        self.pola[5][2]=Island(5, 2, [5, 3])
        self.pola[5][3]=Capital(5, 3, 0, -1, 3, [[5, 1], [5, 2], [5, 3]])

        self.pola[7][2]=Island(7, 2, [10, 5])
        self.pola[8][3]=Island(8, 3, [10, 5])
        self.pola[9][4]=Island(9, 4, [10, 5])
        self.pola[10][5]=Capital(10, 5, 0, -1, 4, [[7, 2], [8, 3], [9, 4], [10, 5]])

        self.pola[7][4]=Capital(7, 4, 2, -1, 1, [[7, 4]])

        self.pola[7][6]=Capital(7, 6, 2, -1, 1, [[7, 6]])

        self.pola[3][7]=Capital(3, 7, 2, -1, 1, [[3, 7]])

        self.pola[4][9]=Island(4, 9, [5, 9])
        self.pola[5][10]=Island(5, 10, [5, 9])
        self.pola[6][10]=Island(6, 10, [5, 9])
        self.pola[5][9]=Capital(5, 9, 0, -1, 4, [[4, 9], [5, 10], [6, 10], [5, 9]])

        self.pola[4][6]=Island(4, 6, [4, 5])
        self.pola[4][5]=Capital(4, 5, 1, -1, 2, [[4, 6], [4, 5]])

        self.pola[6][8]=Island(6, 8, [6, 7])
        self.pola[6][7]=Capital(6, 7, 1, -1, 2, [[6, 8], [6, 7]])

        self.pola[9][11]=Island(9, 11, [9, 10])
        self.pola[9][10]=Capital(9, 10, 1, -1, 2, [[9, 10], [9, 11]])

        self.pola[9][8]=Island(9, 8, [8, 8])
        self.pola[8][8]=Capital(8, 8, 1, -1, 2, [[9, 8], [8, 8]])

        self.pola[11][8]=Island(11, 8, [10, 7])
        self.pola[10][7]=Capital(10, 7, 1, -1, 2, [[11, 8], [10, 7]])

    def build(self, kto, x, y, co, slot):
        if self.pola[x][y].typ!='capital':
            raise TryingToBuildOnWater
        if self.pola[x][y].owner!=kto:
            raise AttemptedBuildingOnNotOwnedTile
        self.pola[x][y].build(co, slot)
    def buildMetropolis(self, kto, x, y):
        if self.pola[x][y].typ!='capital':
            raise TryingToBuildOnWater
        if self.pola[x][y].owner!=kto:
            raise AttemptedBuildingOnNotOwnedTile
        self.pola[x][y].buildMetropolis()
    def raiseValue(self, kto, x, y):
        if self.pola[x][y].owner!=kto:
            raise AttemptedBuildingOnNotOwnedTile
        self.pola[x][y].increaseValue


board = Plansza()
board.generateBoard()