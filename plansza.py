from bot import Bot
from constants import boardSize

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
    def __hash__(self):
        return self.x*boardSize+self.y
    def increaseValue(self):
        self.value+=1
    def changeOwner(self, newOwner):
        self.owner.ownedTiles.remove(self)
        newOwner.ownedTiles.add(self)
        self.owner=newOwner

class Void:
    def __init__(self, x, y):
        self.x=x
        self.y=y
        self.typ='void'
    def __hash__(self):
        return self.x*boardSize+self.y

class Island:
    def __init__(self, x, y, capital):
        self.x=x
        self.y=y
        self.capital=capital
        self.typ='island'
    def __hash__(self):
        return self.x*boardSize+self.y

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
    def __hash__(self):
        return self.x*boardSize+self.y
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
        self.owner.ownedTiles.remove(self)
        newOwner.ownedTiles.add(self)
        self.owner=newOwner

class Plansza:
    def __init__(self):
        self.pola=[[]]
    def generateBoard(self):
        for x in range(boardSize):
            for y in range(boardSize):
                self.pola.insert(x, Void(x, y))
        for x in range(3, 9):
            self.pola[x][1]=Water(x, 1, 0, 'nobody')
        for x in range(3, 10):
            self.pola[x][1]=Water(x, 1, 0, 'nobody')
        for x in range(2, 10):
            self.pola[x][1]=Water(x, 1, 0, 'nobody')
        for x in range(2, 11):
            self.pola[x][1]=Water(x, 1, 0, 'nobody')
        for x in range(1, 11):
            self.pola[x][1]=Water(x, 1, 0, 'nobody')
        for x in range(1, 12):
            self.pola[x][1]=Water(x, 1, 0, 'nobody')
        for x in range(1, 9):
            self.pola[x][1]=Water(x, 1, 0, 'nobody')
        for x in range(3, 9):
            self.pola[x][1]=Water(x, 1, 0, 'nobody')

    def build(self, kto, gdzie, co, slot):
        if self.pola[gdzie].typ!='capital':
            raise TryingToBuildOnWater
        if self.pola[gdzie].owner!=kto:
            raise AttemptedBuildingOnNotOwnedTile
        self.pola[gdzie].build(co, slot)
    def buildMetropolis(self, kto, gdzie):
        if self.pola[gdzie].typ!='capital':
            raise TryingToBuildOnWater
        if self.pola[gdzie].owner!=kto:
            raise AttemptedBuildingOnNotOwnedTile
        self.pola[gdzie].buildMetropolis()
    def raiseValue(self, kto, gdzie):
        if self.pola[gdzie].owner!=kto:
            raise AttemptedBuildingOnNotOwnedTile
        self.pola[gdzie].increaseValue


