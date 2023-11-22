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
        if(ktora>=4):
            raise TooManyRecruitments
        koszt=0
        if(ktora>0):
            koszt+=ktora+1
        if(kto.coins<koszt):
            raise InvalidFunds
        kto.tempsoldiers+=1
        kto.coins-=koszt
        ktora+=1
    def buduj(self, kto, x, y, slot):
        if(kto.coins<2):
            raise InvalidFunds
        self.plansza.build(kto, x, y, 3, slot)
        kto.coins-=2
    def reset(self):
        self.ktora=0

class Zeus:
    def __init__(self, plansza):
        self.plansza=plansza
    def buduj(self, kto, x, y, slot):
        koszt=2
        if(kto.coins<koszt):
            raise InvalidFunds
        self.plansza.build(kto, x, y, 2, slot)
        kto.coins-=2
    def reset(self):
        pass

class Poseidon:
    def __init__(self, plansza):
        self.ktora=0
        self.plansza=plansza
    def rekrutuj(self, kto):
        if(ktora>=4):
            raise TooManyRecruitments
        koszt=0
        if(ktora>0):
            koszt+=ktora
        if(kto.coins<koszt):
            raise InvalidFunds
        kto.tempfleets+=1
        kto.coins-=koszt
        ktora+=1
    def buduj(self, kto, x, y, slot):
        if(kto.coins<2):
            raise InvalidFunds
        self.plansza.build(kto, x, y, 4, slot)
        kto.coins-=2
    def reset(self):
        self.ktora=0

class Athena:
    def __init__(self, plansza):
        self.ktora=0
        self.plansza=plansza
    def rekrutuj(self, kto):
        if(ktora>=2):
            raise TooManyRecruitments
        koszt=0
        if(ktora>0):
            koszt+=4
        if(kto.coins<koszt):
            raise InvalidFunds
        kto.philosophers+=1
        kto.coins-=koszt
        ktora+=1
    def buduj(self, kto, x, y, slot):
        if(kto.coins<2):
            raise InvalidFunds
        self.plansza.build(kto, x, y, 1, slot)
        kto.coins-=2
    def reset(self):
        self.ktora=0

class Apollo:
    def __init__(self, plansza):
        self.plansza=plansza
        self.ktory=0
        self.wykonane=set()
    def praise(self, kto, x, y):
        if kto in self.wykonane:
            raise TooMuchPraising
        self.wykonane.add(kto)
        ileWysp=0
        for wys in kto.ownedTiles:
            if self.plansza.pola[wys[0]][wys[1]].type=='wyspa':
                ileWysp+=1
        if ileWysp<=1:
            kto.coins+=4
        else:
            kto.coins+=1
        if self.ktory==0:
            self.plansza.raiseValue(kto, x, y)
        self.ktory+=1