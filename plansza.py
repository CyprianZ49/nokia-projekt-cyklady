from bot import Bot

class MetropilsAlreadyPresent(Exception):
    pass

class InvalidBuildingSlot(Exception):
    pass

class AttemptedBuildingOnNotOwnedTile(Exception):
    pass

class TryingToBuildOnWater(Exception):
    pass

class Pole:
    def __init__(self, typ, value, owner, maxBuildings=0, id=[1]):
        self.id=id[0]
        id[0]+=1
        self.typ=typ
        self.value=value
        self.owner=owner
        self.isMetropolis=False
        self.buildings=['plains' for i in range(maxBuildings)]
        self.neighbours={}
    def __hash__(self):
        return self.id
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
        self.pola={}
    def generateBoard(self):
        self.pola.add(Pole('woda', 0, 'jan'))
        self.pola.add(Pole('wyspa', 2, 'Kuba', 4))
        #......... tu najpierw genereujemy wszystkie pola, a następnie przypisujemy im jakich mają sąsiadów
    def build(self, kto, gdzie, co, slot):
        if self.pola[gdzie].owner!=kto:
            raise AttemptedBuildingOnNotOwnedTile
        if self.pola[gdzie].typ=='woda':
            raise TryingToBuildOnWater
        self.pola[gdzie].build(co, slot)
    def buildMetropolis(self, kto, gdzie):
        if self.pola[gdzie].owner!=kto:
            raise AttemptedBuildingOnNotOwnedTile
        self.pola[gdzie].buildMetropolis()


