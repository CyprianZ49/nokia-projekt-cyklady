from random import randint, shuffle

class Randomizer:
    def load(self, file):
        if file is None:
            self.randint_data = None
            self.shuffle_data = None
        else:
            with open(file, 'r') as f:
                bef, af = f.read().split('sep')
                self.randint_data=list(map(int, bef.split()))
                self.shuffle_data=list(map(int, af.split()))
        self.randint_idx=0
        self.shuffle_idx=0
        print(self.randint_data, self.shuffle_data)

    def randint(self, a, b):
        if not self.randint_data:
            return randint(a, b)
        else:
            val = self.randint_data[self.randint_idx]
            self.randint_idx+=1
            if self.randint_idx == len(self.randint_data):
                self.randint_idx = 0
            return a+val%(b-a)
        
    def randint2(self, a, b):
        val = self.shuffle_data[self.shuffle_idx]
        self.shuffle_idx+=1
        if self.shuffle_idx == len(self.shuffle_data):
            self.shuffle_idx = 0
        return a+val%(b-a)
        
    def shuffle(self, l):
        if not self.shuffle_data:
            shuffle(l)
        else:
            for i in range(0,len(l)-1):
                pos = self.randint2(i,len(l)-1)
                l[pos],l[i]=l[i],l[pos]

random = Randomizer()