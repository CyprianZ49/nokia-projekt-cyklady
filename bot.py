#graczy w sensie gry nazywami botami

class Bot:
    def __init__(self, name, filename=''):
        self.name=name
        self.coins=0
        self.philosophers=0
        self.ownedTiles={}
    def __hash__(self):
        return hash(self.name)
    def get_move(self):
        return input().split()
    def send_move(self,player,move):
        print(player, move)

if __name__=='__main__':
    b = Bot()
    m = b.get_move()
    b.send_move(1,m)