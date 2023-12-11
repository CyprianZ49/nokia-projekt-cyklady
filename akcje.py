from bot import Bot
from plansza import Plansza
from constants import boardSize
import random

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

#nie wytestowane rzeczy: bitwy lądowa i morska, ruchy lądowy i morski, rekrutacja tylko częściowo

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

def bitwaMorska(plansza, x, y, kto, ile):
    other=plansza.pola[x][y].owner
    sila=plansza.pola[x][y].strength
    for tile in other.ownedTiles:
        if plansza.pola[tile[0]][tile[1]].typ=='capital' and plansza.isNeightbour(tile[0], tile[1], x, y):
            if plansza.pola[tile[0]][tile[1]].isMetropolis:
                sila+=1
            for i in plansza.pola[tile[0]][tile[1]].buildings:
                if i==4:
                    sila+=1
    k1=random.randint(0, 5)
    k2=random.randint(0, 5)
    konwersja = [0, 1, 1, 2, 2, 3]
    k1=konwersja[k1]
    k2=konwersja[k2]
    isOver=False
    if ile+k1 >= sila+k2:
        plansza.pola[x][y].strength-=1
        if plansza.pola[x][y].strength==0:
            isOver=True
            if ile>0:
                plansza.changeOwnership(x, y, kto)
                plansza.pola[x][y].strength=ile
            else:
                plansza.changeOwnership(x, y, plansza.pusty)
                plansza.pola[x][y].strength=0
                
    if ile+k1 <= sila+k2:
        ile-=1
        if ile==0:
            isOver=True
    if isOver:
        return
    other.send_move(-1, f"czy wycofujesz z {x, y}")
    odp1 = list(map(int, other.get_move()))
    if odp1[0]==1:
        if not(plansza.isNeightbour(x, y, odp1[1], odp1[2])):
            raise InvalidMove
        if plansza.pola[odp1[1]][odp1[2]].owner!=other and plansza.pola[odp1[1]][odp1[2]].owner!=plansza.pusty:
            raise InvalidMove
        plansza.changeOwnership(odp1[1], odp1[2], other)
        plansza.pola[odp1[1]][odp1[2]].strength+=plansza.pola[x][y].strength
        plansza.changeOwnership(x, y, kto)
        plansza.pola[x][y].strength=ile
    else:
        kto.send_move(-1, f"czy wycofujesz z {x, y}")
        odp2=list(map(int, kto.get_move()))
        if odp2[0]==1:
            if not(plansza.isNeightbour(x, y, odp2[1], odp2[2])):
                raise InvalidMove
            if plansza.pola[odp2[1]][odp2[2]].owner!=kto and plansza.pola[odp2[1]][odp2[2]].owner!=plansza.pusty:
                raise InvalidMove
            plansza.changeOwnership(odp2[1], odp2[2], kto)
            plansza.pola[odp2[1]][odp2[2]].strength+=ile
        else:
            bitwaMorska(plansza, x, y, kto, ile)

def bitwaWyspowa(plansza, x, y, kto, ile):
    other=plansza.pola[x][y].owner
    sila=plansza.pola[x][y].strength
    if plansza.pola[x][y].isMetropolis:
        sila+=1
    for i in plansza.pola[x][y].buildings:
        if i==3:
            sila+=1
    k1=random.randint(0, 5)
    k2=random.randint(0, 5)
    konwersja = [0, 1, 1, 2, 2, 3]
    k1=konwersja[k1]
    k2=konwersja[k2]
    isOver=False
    if ile+k1 >= sila+k2:
        plansza.pola[x][y].strength-=1
        if plansza.pola[x][y].strength==0:
            if ile>0:
                plansza.changeOwnership(x, y, kto)
                plansza.pola[x][y].strength=ile
            isOver=True
    if ile+k1 <= sila+k2:
        ile-=1
        if ile==0:
            isOver=True
    if isOver:
        return
    other.send_move(-1, f"czy wycofujesz z {x, y}")
    odp1 = list(map(int, other.get_move()))
    if odp1[0]==1:
        if not(plansza.isBridge(x, y, other, odp1[1], odp1[2])):
            raise InvalidMove
        if plansza.pola[odp1[1]][odp1[2]].owner!=other and plansza.pola[odp1[1]][odp1[2]].owner!=plansza.pusty:
            raise InvalidMove
        plansza.changeOwnership(odp1[1], odp1[2], other)
        plansza.pola[odp1[1]][odp1[2]].strength+=plansza.pola[x][y].strength
        plansza.changeOwnership(x, y, kto)
        plansza.pola[x][y].strength=ile
    else:
        kto.send_move(-1, f"czy wycofujesz z {x, y}")
        odp2=list(map(int, kto.get_move()))
        if odp2[0]==1:
            if not(plansza.isBridge(x, y, kto, odp2[1], odp2[2])):
                raise InvalidMove
            if plansza.pola[odp2[1]][odp2[2]].owner!=kto and plansza.pola[odp2[1]][odp2[2]].owner!=plansza.pusty:
                raise InvalidMove
            plansza.changeOwnership(odp2[1], odp2[2], kto)
            plansza.pola[odp2[1]][odp2[2]].strength+=ile
        else:
            bitwaWyspowa(plansza, x, y, kto, ile)

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
    def ruch(self, kto, x, y, ile, x1, y1):
        if self.plansza.pola[x][y].typ!='capital' or self.plansza.pola[x1][y1].typ!='capital' or not(self.plansza.isBridge(x, y, kto, x1, y1)):
            raise InvalidMove
        ile = 0
        for tile in self.plansza.pola[x1][y1].owner.ownedTiles:
            if self.plansza.pola[tile[0]][tile[1]].typ=='capital':
                ile+=1
        metro = 0
        for tile in kto.ownedTiles:
            if self.plansza.pola[tile[0]][tile[1]].typ=='capital' and self.plansza.pola[tile[0]][tile[1]].isMetropolis:
                metro+=1
        if self.plansza.pola[x][y].owner!=kto or self.plansza.pola[x][y].strength<ile or (ile==1 and not(metro>1) and self.plansza.pola[x1][y1].owner!=self.plansza.pusty):
            raise InvalidMove
        if 1>kto.coins:
            raise InvalidFunds
        kto.coins-=1
        self.plansza.pola[x][y].strength-=ile
        if self.plansza.pola[x][y].strength==0:
            self.plansza.changeOwnership(x, y, self.plansza.pusty)
        if self.plansza.pola[x1][y1].owner==kto or self.plansza.pola[x1][y1].owner==self.plansza.pusty:
            self.plansza.changeOwnership(x1, y1, kto)
            self.plansza.pola[x1][y1].strength+=ile
        else:
            bitwaWyspowa(self.plansza, x, y, kto, ile)

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
        self.lastMovex=0
        self.lastMovey=0
        self.ileRuch=0
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
        self.ileRuch=10
    def buduj(self, kto, x, y, slot):
        if(kto.coins<2):
            raise InvalidFunds
        self.plansza.build(kto, x, y, 4, slot)
        kto.coins-=2
        self.ileRuch=10
    def ruch(self, kto, x, y, ile, x1, y1):
        if self.plansza.pola[x][y].typ!='water' or self.plansza.pola[x1][y1].typ!='water' or self.plansza.pola[x][y].owner!=kto:
            raise InvalidMove
        if not(self.plansza.isNeightbour(x, y, x1, y1)) or self.plansza.pola[x][y].strength<ile:
            raise InvalidMove
        koszt = 1
        if x==self.lastMovex and y==self.lastMovey and self.ileRuch<3:
            koszt = 0
        if koszt>kto.coins:
            raise InvalidFunds
        kto.coins-=koszt
        if koszt==1:
            self.ileRuch=0
        self.ileRuch+=1
        self.plansza.pola[x][y].strength-=ile
        self.lastMovex=x1
        self.lastMovey=y1
        if self.plansza.pola[x][y].strength==0:
            self.plansza.changeOwnership(x, y, self.plansza.pusty)
        if self.plansza.pola[x1][y1].owner==kto or self.plansza.pola[x1][y1].owner==self.plansza.pusty:
            self.plansza.changeOwnership(x1, y1, kto)
            self.plansza.pola[x1][y1].strength+=ile
        else:
            self.ileRuch=10
            bitwaMorska(self.plansza, x, y, kto, ile)
    

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
    poseidon.lastMovex=0
    poseidon.lastMovey=0
    poseidon.ileRuch=0
    apollo.ktora=0
    apollo.wykonane=set()