from bot import Bot
from plansza import Plansza

class InvalidFunds(Exception):
    pass

class TooManyRecruitments(Exception):
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
    def buduj(self, kto, gdzie):
        if(kto.coins<2):
            raise InvalidFunds
        self.plansza.build(kto, gdzie, 'twierdza')
        kto.coins-=2

class Zeus:
    def __init__(self, plansza):
        self.plansza=plansza
    def buduj(self, kto, gdzie):
        koszt=2
        if(kto.coins<koszt):
            raise InvalidFunds
        self.plansza.build(kto, gdzie, 'temple')
        kto.coins-=2

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
    def buduj(self, kto, gdzie):
        if(kto.coins<2):
            raise InvalidFunds
        self.plansza.build(kto, gdzie, 'port')
        kto.coins-=2

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
    def buduj(self, kto, gdzie):
        if(kto.coins<2):
            raise InvalidFunds
        self.plansza.build(kto, gdzie, 'uniwersytet')
        kto.coins-=2

class Apollo:
    def __init__(self, plansza):
        self.plansza=plansza
        self.ktory=0
        self.wykonane=set()
    def praise(self, kto, gdzie):
        if kto in self.wykonane:
            return
        self.wykonane.add(kto)
        ileWysp=0
        for wys in kto.ownedTiles:
            if wys.type=='wyspa':
                ileWysp+=1
        if ileWysp<=1:
            kto.coins+=4
        else:
            kto.coins+=1
        if self.ktory==0:
            self.plansza.raiseValue(kto, gdzie)
        self.ktory+=1

def reset(zeus, atena, ares, poseidon, apollo):
    zeus.ktora=0
    atena.ktora=0
    ares.ktora=0
    poseidon.ktora=0
    apollo.ktora=0
    apollo.wykonane=set()


'''

po licytacji mamy dla każdego boga który bot go  wylicytował
iterować po bogach, jeśli bóg był przez kogoś wylicytowany to dajemu temu botowi mu sygnał, że jest jego kolej
odbieramy od niego ruchy i wywołujemy adekwatne funkcje akcji

tutaj *jeżel w trackie ruchów spełni warunek metropoli -> powiedział gdzie i jak ją buduje

potem kończy kolejkę

reset licytacj, to jest ustawienie botów w odwrotnej kolejności do tego jak grały oraz
randomizacja kolejności 4 głównych bogów

'''

