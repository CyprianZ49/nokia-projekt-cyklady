from bot import Bot
from plansza import Plansza

class InvalidFunds(Exception):
    pass

class TooManyRecruitments(Exception):
    pass

class TooMuchPraising(Exception):
    pass

class Ares:
    def __init__(self, plansza):
        self.ktora=0
        self.plansza=plansza
    def rekrutuj(self, kto):
        if(self.ktora>=4):
            raise TooManyRecruitments
        koszt=0
        if(self.ktora>0):
            koszt+=self.ktora+1
        if(kto.coins<koszt):
            raise InvalidFunds
        kto.tempsoldiers+=1
        kto.coins-=koszt
        self.ktora+=1
    def buduj(self, kto, x, y, slot):
        if(kto.coins<2):
            raise InvalidFunds
        self.plansza.build(kto, x, y, 3, slot)
        kto.coins-=2

class Zeus:
    def __init__(self, plansza):
        self.plansza=plansza
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
    def rekrutuj(self, kto):
        if(self.ktora>=4):
            raise TooManyRecruitments
        koszt=0
        if(self.ktora>0):
            koszt+=self.ktora
        if(kto.coins<koszt):
            raise InvalidFunds
        kto.tempfleets+=1
        kto.coins-=koszt
        self.ktora+=1
    def buduj(self, kto, x, y, slot):
        if(kto.coins<2):
            raise InvalidFunds
        self.plansza.build(kto, x, y, 4, slot)
        kto.coins-=2

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