from sys import stdout

class Log:
    def __init__(self, fname):
        self.orig = stdout
        self.f = open(fname, 'w', encoding='utf-8')
    def write(self, data):
        self.f.write(data)
        self.f.flush()
        self.orig.write(data)
        self.orig.flush()
    def __del__(self):
        self.f.close()