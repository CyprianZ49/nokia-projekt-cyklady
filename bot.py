class Bot:
    def __init__(self, filename=''):
        ...
    def get_move(self):
        return input().split()
    def send_move(self,player,move):
        print(player, move)

if __name__=='__main__':
    b = Bot()
    m = b.get_move()
    b.send_move(1,m)
