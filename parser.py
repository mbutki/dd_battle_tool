from die import Die
from actor import Player, Monster

class Parser():
    @staticmethod
    def parseRoll(die_str):
        die_list = die_str.split('+')
        dice = []
        singles = []
        for die in die_list:
            die = [int(x) for x in die.split('d')]
            if len(die) == 1:
                singles.append(die[0])
            elif len(die) == 2:
                for i in range(die[0]):
                    dice.append(Die(die[1]))
            else:
                print 'die parse error'
                return None
        return dice, singles

    @staticmethod
    def readActors(filepath, actor_type):
        m_file = open(filepath)
        actors = []
        names = None
        for i, line in enumerate(m_file):
            if line[0] == '#':
                continue
            vals = line.split()
            if i == 0:
                names = vals
                continue
            stats = {}
            for j, val in enumerate(vals):
                try:
                    val = int(val)
                except ValueError:
                    pass
                stats[names[j]] = val
            actors.append(actor_type(stats))
        return actors
#name    ac  will    fort    ref hp  init
#A       1   1       1       1   1   1
