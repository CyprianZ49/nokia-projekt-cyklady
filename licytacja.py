class InvalidMoveError(Exception):
    pass

class Licytacja:
    def __init__(self, bots):
        self.bots=bots
        self.bids={'ze':(0,-1),'ar':(0,-1),'po':(0,-1),'at':(0,-1),'ap':[]}
        self.last_god='ze'
        self.outbid = False
        
    def get_bid(self, bot):
        legal_moves = self.get_legal_moves(bot)
        bot.send_move(-2, "|".join(legal_moves))
        if bot.skipping:
            l = ["l", "ap", "1"]
        else:
            l = bot.get_move()
        while " ".join(l) not in legal_moves:
            bot.send_move(-3, "InvalidMoveError")
            bot.increment_errors()
            if bot.skipping:
                l = ["l", "ap", "1"]
            else:
                l = bot.get_move()

        op,god,value=l
        try:
            value = int(value)
        except ValueError as e:
            bot.send_move(-3, "InvalidMoveError")
            bot.increment_errors()
            raise InvalidMoveError.with_traceback(e)
        print(op,god,value)
        self.last_god = god
        bot.god = god
        return op,god,value
    
    def do_bid(self,i,_,god,value):
        for bot in self.bots:
            bot.send_move(self.bots[i].name,(_,god,value))
        if god=='ap':
            self.bids[god].append(i)
        else:
            if self.bids[god][1]!=-1:
                outb=self.bids[god][1]
                self.outbid = True
                self.bids[god]=(value,i)
                _,ngod,nvalue=self.get_bid(self.bots[outb])
                self.do_bid(outb,_,ngod,nvalue)
            else:
                self.bids[god]=(value,i)
        self.outbid = False

    def perform(self):
        for i,bot in enumerate(self.bots):
            _,god,value=self.get_bid(bot)
            self.do_bid(i,_,god,value)
        return self.bids
    
    def get_legal_moves(self, bot):
        min_values={g:(v[0]+1) for g,v in self.bids.items() if g not in (self.last_god, 'ap')}
        legal_moves=[]
        for g,min_v in min_values.items():
            for v in range(min_v, bot.coins+bot.priests+1):
                legal_moves.append(f'l {g} {v}')
        if not self.outbid:
            min_v=self.bids[self.last_god][0]+1
            for v in range(min_v, bot.coins+bot.priests+1):
                legal_moves.append(f'l {self.last_god} {v}')
        legal_moves.append('l ap 1')
        return legal_moves