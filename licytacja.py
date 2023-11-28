from bot import Bot

class Licytacja:
    def __init__(self, bots):
        self.bots=bots
        self.bids={'ze':(0,-1),'ar':(0,-1),'po':(0,-1),'at':(0,-1),'ap':[]}
    def get_bid(self, bot):
        op,god,value=bot.get_move()
        value = int(value)
        while op!='l' or god not in self.bids or (god!='ap' and (value>bot.coins or self.bids[god][0]>=value)):
            print('invalid move')
            op,god,value=bot.get_move()
            value = int(value)
        return op,god,value
    
    def do_bid(self,i,_,god,value):
        for bot in self.bots:
            bot.send_move(bot.name,(_,god,value))
        if god=='ap':
            self.bids[god].append(i)
        else:
            if self.bids[god][1]!=-1:
                outb=self.bids[god][1]
                _,ngod,nvalue=self.get_bid(self.bots[outb])
                while god==ngod:
                    print('invalid move')
                    _,ngod,nvalue=self.get_bid(self.bots[outb])
                self.bids[god]=(value,i)
                self.do_bid(outb,_,ngod,nvalue)
            else:
                self.bids[god]=(value,i)

    def perform(self):
        for i,bot in enumerate(self.bots):
            _,god,value=self.get_bid(bot)
            self.do_bid(i,_,god,value)
        return self.bids
            
if __name__ == "__main__":
    bots = [Bot(i) for i in range(4)]
    l = Licytacja(bots)
    print(l.perform())