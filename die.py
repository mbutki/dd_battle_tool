import random

class Die():
    def __init__(self, die_type):
        self.die_type = die_type
        self.roll()

    def roll(self):
        self.val = random.randint(1, self.die_type)

    def getVal(self):
        return self.val

    def __str__(self):
        return '{0}d:{1}'.format(self.die_type, self.val)

    def __add__(self, val):
        print 'add', self, self.getVal, val
        return self.getVal + val

    def __radd__(self, val):
        return self.getVal() + val
