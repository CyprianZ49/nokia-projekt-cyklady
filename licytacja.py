class InvalidMoveError(Exception):
    pass

class Licytacja:
    def __init__(self, bots):
        self.bots=bots
        self.bids={'ze':(0,-1),'ar':(0,-1),'po':(0,-1),'at':(0,-1),'ap':[]}
    def get_bid(self, bot):
        ok = 0
        while not ok:
            try:
                op,god,value=bot.get_move()
                print(op,god,value)
                value = int(value)
                if op!='l' or god not in self.bids or (god!='ap' and (value>bot.coins or self.bids[god][0]>=value)):
                    raise InvalidMoveError
            except Exception as e:
                bot.send_move(-3, type(e).__name__)
            else:
                ok = 1
        return op,god,value
    
    def do_bid(self,i,_,god,value):
        for bot in self.bots:
            bot.send_move(self.bots[i].name,(_,god,value))
        if god=='ap':
            self.bids[god].append(i)
        else:
            if self.bids[god][1]!=-1:
                outb=self.bids[god][1]
                ok=0
                while not ok:
                    _,ngod,nvalue=self.get_bid(self.bots[outb])
                    if god==ngod:
                        self.bots[outb].send_move(-3, "AlreadyBetError")
                    else:
                        ok=1
                self.bids[god]=(value,i)
                self.do_bid(outb,_,ngod,nvalue)
            else:
                self.bids[god]=(value,i)

    def perform(self):
        for i,bot in enumerate(self.bots):
            _,god,value=self.get_bid(bot)
            self.do_bid(i,_,god,value)
        return self.bids