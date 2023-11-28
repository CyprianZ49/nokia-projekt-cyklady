from bot import Bot
from plansza import Plansza
from constants import boardSize

class InvalidFunds(Exception):
    pass

class TooManyRecruitments(Exception):
    pass

class TooMuchPraising(Exception):
    pass

class TooManyPiecesOfThisType(Exception):
    pass

class InvalidMove(Exception):
    pass

def Metropolizacja(plansza, kto):
    k=0
    for i in range(1, 5):
        for tile in kto.ownedTiles:
            if plansza.pola[tile[0]][tile[1]].typ=='capital' and i in plansza.pola[tile[0]][tile[1]].buildings:
                k+=1
                break
    if k==4:
        kto.send_move(-1, "zbuduj wasc metropolie - z budynkow!\n")
        odp = list(map(int, kto.get_move()))
        if len(odp)!=14:
            raise InvalidMove
        for i in range(1, 5):
            tile = plansza.pola[odp[0+(i-1)*3]][odp[1+(i-1)*3]]
            slot = odp[2+(i-1)*3]
            if tile.typ!='capital' or tile.owner!=kto or len(tile.buildings<slot) or tile.buildings[slot]!=i:
                raise InvalidMove
        if plansza.pola[odp[12]][odp[13]].typ!='capital' or plansza.pola[odp[12]][odp[13]].owner!=kto:
            raise InvalidMove
        for i in range(1, 5):
            tile = plansza.pola[odp[0+(i-1)*3]][odp[1+(i-1)*3]]
            slot = odp[2+(i-1)*3]
            tile.buildings[slot]=0
        plansza.buildMetropolis(kto, odp[12], odp[13])
    elif kto.philosophers>=4:
        kto.send_move(-1, "zbuduj wasc metropolie - z filozofow!\n")
        odp = list(map(int, kto.get_move()))
        if len(odp)!=2:
            raise InvalidMove
        plansza.buildMetropolis(kto, odp[0], odp[1])
        kto.philosophers-=4


class Ares:
    def __init__(self, plansza):
        self.ktora=0
        self.plansza=plansza
    def rekrutuj(self, kto, x, y):
        if(self.ktora>=4):
            raise TooManyRecruitments
        koszt=0
        if(self.ktora>0):
            koszt+=self.ktora+1
        if(kto.coins<koszt):
            raise InvalidFunds
        if(kto.soliderLimit==0):
            raise TooManyPiecesOfThisType
        self.plansza.makeSolider(x, y, kto)
        kto.coins-=koszt
        kto.soliderLimit-=1
        self.ktora+=1
    def buduj(self, kto, x, y, slot):
        if(kto.coins<2):
            raise InvalidFunds
        self.plansza.build(kto, x, y, 3, slot)
        kto.coins-=2
    def move(self, x, y, ile, x1, y1):
        pass
        #potrzebna funkcja pomocnicza, czy wyspa a i b są połączone statkami gracza, funkcja ewidentnie planszowa
        #zamiast się męczyć z pełnym DFSem można robić bardzo pałowego BFSa z wykorzystaniem limitu morskich pól posiadanych przez gracza (8)

class Zeus:
    def __init__(self, plansza):
        self.plansza=plansza
        self.ktora=0
    def rekrutuj(self, kto):
        if(self.ktora>=2):
            raise TooManyRecruitments
        koszt=0
        if(self.ktora>0):
            koszt+=4
        if(kto.coins<koszt):
            raise InvalidFunds
        kto.priests+=1
        kto.coins-=koszt
        self.ktora+=1
    def buduj(self, kto, x, y, slot):
        koszt=2
        if(kto.coins<koszt):
            raise InvalidFunds
        self.plansza.build(kto, x, y, 2, slot)
        kto.coins-=2

class Poseidon:
    def __init__(self, plansza):
        self.ktora=0
        self.plansza=plansza
    def rekrutuj(self, kto, x, y):
        if(self.ktora>=4):
            raise TooManyRecruitments
        koszt=0
        if(self.ktora>0):
            koszt+=self.ktora
        if(kto.coins<koszt):
            raise InvalidFunds
        if(kto.fleetLimit==0):
            raise TooManyPiecesOfThisType
        self.plansza.makeFleet(x, y, kto)
        kto.fleetLimit-=1
        kto.coins-=koszt
        self.ktora+=1
    def buduj(self, kto, x, y, slot):
        if(kto.coins<2):
            raise InvalidFunds
        self.plansza.build(kto, x, y, 4, slot)
        kto.coins-=2
    def ruch(self, kto, x, y, ile, x1, y1):
        pass
        #nastąpiła kompletna zmiana idei, bo stara był frankly fatalna, kod usunięty, ale mam ŁADNY pomysł nie ruszać beze mnie -C
    

class Athena:
    def __init__(self, plansza):
        self.ktora=0
        self.plansza=plansza
    def rekrutuj(self, kto):
        if(self.ktora>=2):
            raise TooManyRecruitments
        koszt=0
        if(self.ktora>0):
            koszt+=4
        if(kto.coins<koszt):
            raise InvalidFunds
        kto.philosophers+=1
        kto.coins-=koszt
        self.ktora+=1
    def buduj(self, kto, x, y, slot):
        if(kto.coins<2):
            raise InvalidFunds
        self.plansza.build(kto, x, y, 1, slot)
        kto.coins-=2

class Apollo:
    def __init__(self, plansza):
        self.plansza=plansza
        self.ktory=0
        self.wykonane=set()
    def praise(self, kto, x, y):
        if kto in self.wykonane:
            raise TooMuchPraising
        if self.ktory==0:
            self.plansza.raiseValue(kto, x, y)
        self.wykonane.add(kto)
        self.ktory+=1
        ileWysp=0
        for wys in kto.ownedTiles:
            if self.plansza.pola[wys[0]][wys[1]].typ=='capital':
                ileWysp+=1
        if ileWysp<=1:
            kto.coins+=4
        else:
            kto.coins+=1

def reset(zeus, atena, ares, poseidon, apollo):
    zeus.ktora=0
    atena.ktora=0
    ares.ktora=0
    poseidon.ktora=0
    apollo.ktora=0
    apollo.wykonane=set()