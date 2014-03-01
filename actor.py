from die import Die
from color import Color

class Actor(object):
    def __init__(self, stats):
        self.stats = stats

    def __str__(self):
        pass

    def __cmp__(self, other):
        return self.stats['init'].__cmp__(other.stats['init'])

class Player(Actor):
    names = ['name', 'init', 'ac', 'fort', 'ref', 'will']

    def __init__(self, stats):
        super(Player, self).__init__(stats)
        self.stats['init'] = None

    def __str__(self):
        out = ['{0}:{1}'.format(name, self.stats[name]) for name in Player.names]
        out = ' '.join(out)
        return out

    def printLong(self):
        print 'Name:{0}    Init:{1}'.format(self.stats['name'], self.stats['init'])
        print 'AC:{0}    Fortitude:{1}    Reflex:{2}    Will:{3}'.format(self.stats['ac'], self.stats['fort'], self.stats['ref'], self.stats['will'])

class Monster(Actor):
    names = ['name', 'init', 'ac', 'fort', 'ref', 'will', 'hp']

    def __init__(self, stats):
        super(Monster, self).__init__(stats)
        stats['init'] += Die(20)
        stats['statuses'] = []
        stats['max_hp'] = stats['hp']
        self.bloodied = False

    def __str__(self):
        out = ['{0}:{1}'.format(name, self.stats[name]) for name in Monster.names]
        out = ' '.join(out)
        out += ' status:['
        out += ', '.join('{0}.{1}'.format(i, x) for i, x in enumerate(self.stats['statuses']))
        out += ']'
        return out

    def printLong(self):
        print 'Name:{0}    HP:{1}/{2}    Init:{3}'.format(self.stats['name'], self.stats['hp'], self.stats['max_hp'], self.stats['init'])
        print 'AC:{0}    Fortitude:{1}    Reflex:{2}    Will:{3}'.format(self.stats['ac'], self.stats['fort'], self.stats['ref'], self.stats['will'])
        if len(self.stats['statuses']) > 0:
            print Color.RED +'status: ' + ' '.join(['{0}.{1}'.format(i, status) for i, status in enumerate(self.stats['statuses'])]) + Color.END
        else:
            print 'status: ' + ' '.join(['{0}.{1}'.format(i, status) for i, status in enumerate(self.stats['statuses'])])
        if self.stats['hp'] <= (self.stats['max_hp']/2.0):
            print '{0}Bloodied{1}'.format(Color.RED,Color.END)
