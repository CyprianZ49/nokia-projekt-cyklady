from bot import Bot

class MetropilsAlreadyPresent(Exception):
    pass

class InvalidBuildingSlot(Exception):
    pass

class AttemptedBuildingOnNotOwnedTile(Exception):
    pass

class TryingToBuildOnWater(Exception):
    pass

class CannotBeOwned(Exception):
    pass

class Water:
    def __init__(self, x, y, value, owner):
        self.x=x
        self.y=y
        self.value=value
        self.owner=owner
        self.typ='water'
        self.strength=0
    def changeOwner(self, newOwner):
        self.owner.ownedTiles.remove((self.x, self.y))
        newOwner.ownedTiles.append((self.x, self.y))
        self.owner=newOwner
    def increaseValue(self):
        self.value+=1

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
        self.buildings=[0 for i in range(maxBuildings)]
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
        self.owner.ownedTiles.remove((self.x, self.y))
        newOwner.ownedTiles.append((self.x, self.y))
        self.owner=newOwner

class Plansza:
    def __init__(self, pusty):
        self.pola=[[]]
        self.pusty=pusty
    def generateBoard(self):
        for x in range(13):
            self.pola.append([])
            for y in range(13):
                self.pola[x].append(Void(x, y))
        for y in range(1, 7):
            for x in range(1, 6+y):
                self.pola[x][y]=Water(x, y, 0, self.pusty)
        for y in range(7, 12):
            for x in range(y-5, 12):
                self.pola[x][y]=Water(x, y, 0, self.pusty)
        self.pola[1][1].increaseValue()
        self.pola[6][1].increaseValue()
        self.pola[1][6].increaseValue()
        self.pola[11][6].increaseValue()
        self.pola[6][11].increaseValue()
        self.pola[11][11].increaseValue()

        self.pola[2][2]=Island(2, 2, [3, 3])
        self.pola[3][2]=Island(3, 2, [3, 3])
        self.pola[3][3]=Capital(3, 3, 0, self.pusty, 3, [[2, 2], [3, 2], [3, 3]])

        self.pola[1][4]=Island(1, 4, [2, 4])
        self.pola[1][5]=Island(1, 5, [2, 4])
        self.pola[2][4]=Capital(2, 4, 0, self.pusty, 3, [[1, 4], [1, 5], [2, 4]])

        self.pola[5][1]=Island(5, 1, [5, 3])
        self.pola[5][2]=Island(5, 2, [5, 3])
        self.pola[5][3]=Capital(5, 3, 0, self.pusty, 3, [[5, 1], [5, 2], [5, 3]])

        self.pola[7][2]=Island(7, 2, [10, 5])
        self.pola[8][3]=Island(8, 3, [10, 5])
        self.pola[9][4]=Island(9, 4, [10, 5])
        self.pola[10][5]=Capital(10, 5, 0, self.pusty, 4, [[7, 2], [8, 3], [9, 4], [10, 5]])

        self.pola[7][4]=Capital(7, 4, 2, self.pusty, 1, [[7, 4]])

        self.pola[7][6]=Capital(7, 6, 2, self.pusty, 1, [[7, 6]])

        self.pola[3][7]=Capital(3, 7, 2, self.pusty, 1, [[3, 7]])

        self.pola[4][9]=Island(4, 9, [5, 9])
        self.pola[5][10]=Island(5, 10, [5, 9])
        self.pola[6][10]=Island(6, 10, [5, 9])
        self.pola[5][9]=Capital(5, 9, 0, self.pusty, 4, [[4, 9], [5, 10], [6, 10], [5, 9]])

        self.pola[4][6]=Island(4, 6, [4, 5])
        self.pola[4][5]=Capital(4, 5, 1, self.pusty, 2, [[4, 6], [4, 5]])

        self.pola[6][8]=Island(6, 8, [6, 7])
        self.pola[6][7]=Capital(6, 7, 1, self.pusty, 2, [[6, 8], [6, 7]])

        self.pola[9][11]=Island(9, 11, [9, 10])
        self.pola[9][10]=Capital(9, 10, 1, self.pusty, 2, [[9, 10], [9, 11]])

        self.pola[9][8]=Island(9, 8, [8, 8])
        self.pola[8][8]=Capital(8, 8, 1, self.pusty, 2, [[9, 8], [8, 8]])

        self.pola[11][8]=Island(11, 8, [10, 7])
        self.pola[10][7]=Capital(10, 7, 1, self.pusty, 2, [[11, 8], [10, 7]])
    
    def isAdj(self, x1, y1, x2, y2):
        if x1+1==x2 and y1==y2:
            return True
        if x1-1==x2 and y1==y2:
            return True
        if x1==x2 and y1+1==y2:
            return True
        if x1==x2 and y1-1==y2:
            return True
        if x1+1==x2 and y1+1==y2:
            return True
        if x1-1==x2 and y1-1==y2:
            return True
        if x1==x2 and y1==y2:
            return True
        return False
    def isNeightbour(self, x1, y1, x2, y2):
        if self.pola[x1][y1].typ=='island':
            return self.isNeightbour(self.pola[x1][y1].capital[0], self.pola[x1][y1].capital[1], x2, y2)
        if self.pola[x2][y2].typ=='island':
            return self.isNeightbour(x1, y1, self.pola[x2][y2].capital[0], self.pola[x2][y2].capital[1])
        #pole sąsiaduje z wyspą wtedy i tylko wtedy kiedy sąsiaduje z jej stolicą
        test=self.isAdj(x1, y1, x2, y2)
        if self.pola[x1][y1].typ=='capital':
            for tile in self.pola[x1][y1].territory:
                test = test or self.isAdj(x2, y2, tile[0], tile[1])
        if self.pola[x2][y2].typ=='capital':
            for tile in self.pola[x2][y2].territory:
                test = test or self.isAdj(x1, y1, tile[0], tile[1])      
        #making use of the fact that no two isles can be adjecent
        return test
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
    def changeOwnership(self, x, y, kto):
        if self.pola[x][y].typ!='capital' and self.pola[x][y].typ!='water':
            raise CannotBeOwned
        self.pola[x][y].changeOwner(kto)
    def makeSolider(self, x, y, kto):
        if self.pola[x][y].typ!='capital':
            raise TryingToBuildOnWater
        if self.pola[x][y].owner!=kto:
            raise AttemptedBuildingOnNotOwnedTile
        self.pola[x][y].strength+=1
    def makeFleet(self, x, y, kto):
        if self.pola[x][y].typ!='water':
            raise TryingToBuildOnWater
        if self.pola[x][y].owner!=kto and self.pola[x][y]!=self.pusty:
            raise AttemptedBuildingOnNotOwnedTile
        test = False
        for tile in kto.ownedTiles:
            if self.pola[tile[0]][tile[1]].typ=='capital':
                if(self.isNeightbour(tile[0], tile[1], x, y)):
                    test = True
        if not test:
            raise AttemptedBuildingOnNotOwnedTile
        if self.pola[x][y].owner==self.pusty:
            self.changeOwnership(x, y, kto)
        self.pola[x][y].strength+=1
    def isBridge(self, x1, y1, kto, x2, y2):
        if self.pola[x1][y1].typ!='capital' or self.pola[x2][y2]!='capital' or self.pola[x1][y1].owner!=kto:
            return False
        connected = []
        connected.append([x1, y1])
        for _ in range(8):
            for tile in kto.ownedTiles:
                if self.pola[tile[0]][tile[1]].typ=='water' and tile not in connected:
                    for t in connected:
                        if self.isNeightbour(t[0], t[1], tile[0], tile[1]):
                            connected.append(tile)
                            break
        test = False
        for t in connected:
            if self.isNeightbour(t[0], t[1], x2, y2):
                test = True
        return test
        
