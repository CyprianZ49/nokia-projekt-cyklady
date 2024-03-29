from constants import boardSize
from legalMoves import *
from custom_rand import random

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

class TooMuchSmiting(Exception):
    pass

class CannotBeSmitten(Exception):
    pass

class InvalidMoveError(Exception):
    pass

#for anyone reading the code: kto means who in polish and is used to refer to the player performing an action

def get_battle_move(bot):
    if bot.skipping:
        return ["0"]
    return bot.get_move()

def Metropolizacja(plansza, kto):
    if kto.skipping:
        return
    k=0
    for i in range(1, 5):
        for tile in kto.ownedTiles:
            if plansza.pola[tile[0]][tile[1]].typ=='capital' and i in plansza.pola[tile[0]][tile[1]].buildings:
                k+=1
                break
    if k==4:
        kto.send_move(-7, "buildings")
        kto.isBuildingMetropolis = True
        legal = getLegalMoves(plansza, kto)
        move = kto.get_move()
        odp = list(map(int, move))
        if " ".join(move) not in legal:
            raise InvalidMoveError
        if len(odp)!=14:
            raise InvalidMove
        for i in range(1, 5):
            tile = plansza.pola[odp[0+(i-1)*3]][odp[1+(i-1)*3]]
            slot = odp[2+(i-1)*3]
            kto.send_move(-1, f"{tile.buildings[slot]}")
            if tile.typ!='capital' or tile.owner!=kto or len(tile.buildings)<slot or tile.buildings[slot]!=i:
                raise InvalidMove
        if plansza.pola[odp[12]][odp[13]].typ!='capital' or plansza.pola[odp[12]][odp[13]].owner!=kto:
            raise InvalidMove
        for i in range(1, 5):
            tile = plansza.pola[odp[0+(i-1)*3]][odp[1+(i-1)*3]]
            slot = odp[2+(i-1)*3]
            tile.buildings[slot]=0
        plansza.buildMetropolis(kto, odp[12], odp[13])
        kto.isBuildingMetropolis = False
    elif kto.philosophers>=4:
        kto.send_move(-7, "philosophers")
        kto.isBuildingMetropolis = True
        legal = getLegalMoves(plansza, kto)
        move = kto.get_move()
        odp = list(map(int, move))
        if " ".join(move) not in legal:
            raise InvalidMoveError
        if len(odp)!=2:
            raise InvalidMove
        plansza.buildMetropolis(kto, odp[0], odp[1])
        kto.philosophers-=4
        kto.isBuildingMetropolis = False

def seaBattle(plansza, x, y, kto, ile):
    plansza.attackerPower = ile
    plansza.defenderPower = plansza.pola[x][y].strength
    kto.send_move(-8, f"attacking {x} {y}")
    other=plansza.pola[x][y].owner
    other.send_move(-8, f"defending {x} {y}")
    plansza.attackerColor = kto
    plansza.defenderColor = other
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

    if ile+k1 >= sila+k2:
        other.send_move(-10, "friendly")
        kto.send_move(-10, "enemy")
        plansza.pola[x][y].strength-=1
                
    if ile+k1 <= sila+k2:
        kto.send_move(-10, "friendly")
        other.send_move(-10, "enemy")
        ile-=1

    if ile==0 or plansza.pola[x][y].strength == 0:
        if ile > 0:
            plansza.changeOwnership(x, y, kto)
            plansza.pola[x][y].strength = ile
        if plansza.pola[x][y].strength == 0:
            plansza.changeOwnership(x, y, plansza.pusty)
        kto.send_move(-9, "over")
        other.send_move(-9, "over")
        return

    plansza.mayReatreat = other
    other.send_move(-11, "retreat?")
    legal = getLegalMoves(plansza, other)
    move = get_battle_move(other)
    odp1 = list(map(int, move))
    if " ".join(move) not in legal:
        raise InvalidMoveError
    plansza.mayReatreat = plansza.pusty
    if odp1[0]==1:
        if not(plansza.isNeightbour(x, y, odp1[1], odp1[2])):
            raise InvalidMove
        if plansza.pola[odp1[1]][odp1[2]].owner!=other and plansza.pola[odp1[1]][odp1[2]].owner!=plansza.pusty:
            raise InvalidMove
        plansza.changeOwnership(odp1[1], odp1[2], other)
        plansza.pola[odp1[1]][odp1[2]].strength+=plansza.pola[x][y].strength
        plansza.changeOwnership(x, y, kto)
        plansza.pola[x][y].strength=ile
        kto.send_move(-9, "over")
        other.send_move(-9, "over")
    else:
        plansza.mayReatreat = kto
        kto.send_move(-11, "retreat?")
        legal = getLegalMoves(plansza, kto)
        move = get_battle_move(kto)
        odp2 = list(map(int, move))
        if " ".join(move) not in legal:
            raise InvalidMoveError
        plansza.mayReatreat = plansza.pusty
        if odp2[0]==1:
            if not(plansza.isNeightbour(x, y, odp2[1], odp2[2])):
                raise InvalidMove
            if plansza.pola[odp2[1]][odp2[2]].owner!=kto and plansza.pola[odp2[1]][odp2[2]].owner!=plansza.pusty:
                raise InvalidMove
            plansza.changeOwnership(odp2[1], odp2[2], kto)
            plansza.pola[odp2[1]][odp2[2]].strength+=ile
            kto.send_move(-9, "over")
            other.send_move(-9, "over")
        else:
            seaBattle(plansza, x, y, kto, ile)

def islandBattle(plansza, x, y, kto, ile):
    plansza.attackerPower = ile
    plansza.defenderPower = plansza.pola[x][y].strength
    kto.send_move(-8, f"attacking {x} {y}")
    other=plansza.pola[x][y].owner
    other.send_move(-8, f"defending {x} {y}")
    sila=plansza.pola[x][y].strength
    plansza.attackerColor = kto
    plansza.defenderColor = other
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

    if ile+k1 >= sila+k2:
        other.send_move(-10, "friendly")
        kto.send_move(-10, "enemy")
        plansza.pola[x][y].strength-=1
                
    if ile+k1 <= sila+k2:
        kto.send_move(-10, "friendly")
        other.send_move(-10, "enemy")
        ile-=1

    if ile==0 or plansza.pola[x][y].strength == 0:
        if ile > 0:
            plansza.changeOwnership(x, y, kto)
            plansza.pola[x][y].strength = ile
        kto.send_move(-9, "over")
        other.send_move(-9, "over")
        return
    
    plansza.mayReatreat = other
    other.send_move(-11, "retreat?")
    legal = getLegalMoves(plansza, other)
    move = get_battle_move(other)
    odp1 = list(map(int, move))
    if " ".join(move) not in legal:
        raise InvalidMoveError
    plansza.mayReatreat = plansza.pusty
    if odp1[0]==1:
        if not(plansza.isBridge(x, y, other, odp1[1], odp1[2])):
            raise InvalidMove
        if plansza.pola[odp1[1]][odp1[2]].owner!=other and plansza.pola[odp1[1]][odp1[2]].owner!=plansza.pusty:
            raise InvalidMove
        plansza.changeOwnership(odp1[1], odp1[2], other)
        plansza.pola[odp1[1]][odp1[2]].strength+=plansza.pola[x][y].strength
        plansza.changeOwnership(x, y, kto)
        plansza.pola[x][y].strength=ile
        kto.send_move(-9, "over")
        other.send_move(-9, "over")
    else:
        plansza.mayReatreat = kto
        kto.send_move(-11, "retreat?")
        legal = getLegalMoves(plansza, kto)
        move = get_battle_move(kto)
        odp2 = list(map(int, move))
        if " ".join(move) not in legal:
            raise InvalidMoveError
        plansza.mayReatreat = plansza.pusty
        if odp2[0]==1:
            if not(plansza.isBridge(x, y, kto, odp2[1], odp2[2])):
                raise InvalidMove
            if plansza.pola[odp2[1]][odp2[2]].owner!=kto and plansza.pola[odp2[1]][odp2[2]].owner!=plansza.pusty:
                raise InvalidMove
            plansza.changeOwnership(odp2[1], odp2[2], kto)
            plansza.pola[odp2[1]][odp2[2]].strength+=ile
            kto.send_move(-9, "over")
            other.send_move(-9, "over")
        else:
            islandBattle(plansza, x, y, kto, ile)

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
        self.plansza.makeSolider(x, y, kto)
        kto.coins-=koszt
        self.ktora+=1
    def buduj(self, kto, x, y, slot):
        if(kto.coins<2):
            raise InvalidFunds
        self.plansza.build(kto, x, y, 3, slot)
        kto.coins-=2
    def ruch(self, kto, x, y, ile, x1, y1):
        if self.plansza.pola[x][y].typ!='capital' or self.plansza.pola[x1][y1].typ!='capital' or not(self.plansza.isBridge(x, y, kto, x1, y1)):
            raise InvalidMove
        posiadane = 0
        if self.plansza.pola[x1][y1].owner!=self.plansza.pusty:
            for tile in self.plansza.pola[x1][y1].owner.ownedTiles:
                if self.plansza.pola[tile[0]][tile[1]].typ=='capital':
                    posiadane+=1
        else:
            posiadane = 10
        metro = 0
        for tile in kto.ownedTiles:
            if self.plansza.pola[tile[0]][tile[1]].typ=='capital' and self.plansza.pola[tile[0]][tile[1]].isMetropolis:
                metro+=1
        if self.plansza.pola[x][y].owner!=kto or self.plansza.pola[x][y].strength<ile or (posiadane==1 and not(metro>0) and self.plansza.pola[x1][y1].owner!=self.plansza.pusty):
            raise InvalidMove
        koszt = 1
        if kto.actionDiscount>0:
            kto.actionDiscount-=1
            koszt = 0
        if koszt>kto.coins:
            raise InvalidFunds
        kto.coins-=koszt
        self.plansza.pola[x][y].strength-=ile
        if self.plansza.pola[x1][y1].owner==kto or self.plansza.pola[x1][y1].owner==self.plansza.pusty or self.plansza.pola[x1][y1].strength == 0:
            self.plansza.changeOwnership(x1, y1, kto)
            self.plansza.pola[x1][y1].strength+=ile
        else:
            self.plansza.isFight = True
            self.plansza.whereFight = (x1, y1)
            self.plansza.pola[x][y].fighting = True
            self.plansza.pola[x1][y1].fighting = True
            self.plansza.isBridge(x, y, kto, x1, y1, True)
            islandBattle(self.plansza, x1, y1, kto, ile)
            self.plansza.isBridge(x, y, kto, x1, y1, True)
            self.plansza.pola[x][y].fighting = False
            self.plansza.pola[x1][y1].fighting = False
            self.plansza.isFight = False

class Zeus:
    def __init__(self, plansza):
        self.plansza=plansza
        self.ktora=0
        self.ktora2=0
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
    def ruch(self, kto, x, y):
        if(self.ktora2>0):
            raise TooMuchSmiting
        if(self.plansza.pola[x][y].typ!='capital' and self.plansza.pola[x][y].typ!='water'):
            raise CannotBeSmitten
        if(self.plansza.pola[x][y].strength==0):
            raise CannotBeSmitten
        koszt=3
        while koszt>0 and kto.actionDiscount>0:
            koszt-=1
            kto.actionDiscount-=1
        if koszt>kto.coins:
            raise InvalidFunds
        kto.coins-=koszt
        self.ktora2+=1
        self.plansza.pola[x][y].strength-=1
        if self.plansza.pola[x][y].strength==0 and self.plansza.pola[x][y].typ=='water':
            self.plansza.changeOwnership(x, y, self.plansza.pusty)


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
        self.plansza.makeFleet(x, y, kto)
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
        if koszt>0 and kto.actionDiscount>0:
            kto.actionDiscount-=1
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
            self.plansza.isFight = True
            self.plansza.whereFight = (x1, y1)
            self.plansza.pola[x][y].fighting = True
            self.plansza.pola[x1][y1].fighting = True
            seaBattle(self.plansza, x1, y1, kto, ile)
            self.plansza.pola[x][y].fighting = False
            self.plansza.pola[x1][y1].fighting = False
            self.plansza.isFight = False
    

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
    zeus.ktora2=0
    atena.ktora=0
    ares.ktora=0
    poseidon.ktora=0
    poseidon.lastMovex=0
    poseidon.lastMovey=0
    poseidon.ileRuch=0
    apollo.ktora=0
    apollo.wykonane=set()