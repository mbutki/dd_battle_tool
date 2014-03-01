#!/usr/bin/env python

import random
from parser import Parser
from glob import glob
from die import Die
from actor import Player, Monster
import sys
import os
from color import Color
import Tkinter

class Encounter():
    def __init__(self):
        self.actors = list()
        self.current = 0

    def addActor(self, actor):
        self.actors.append(actor)

    def printHeader(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print ''
        print ''
        self.printActors()        
        print ''
        print ''
        self.printCurActor()
        print ''
        print ''

    def printCurActor(self):
        actor = self.actors[self.current]
        actor.printLong()

    def printActors(self):
        #self.actors.sort(reverse=True)
        for i, actor in enumerate(self.actors):
            if i == self.current:
                print '{0}{1}) {2}{3}'.format(Color.GREEN, i, str(actor), Color.END)
            else:
                print '{0}) {1}'.format(i, str(actor))

    def initOrder(self):
        self.actors.sort(reverse=True)
 
    def shiftUp(self):
        tmp = self.actors[self.current]
        self.actors[self.current] = self.actors[self.previousNum()]
        self.actors[self.previousNum()] = tmp
        self.current = self.previousNum()
        self.printHeader()
           
    def shiftDown(self):
        tmp = self.actors[self.current]
        self.actors[self.current] = self.actors[self.nextNum()]
        self.actors[self.nextNum()] = tmp
        self.current = self.nextNum()
        self.printHeader()

    def nextNum(self):
        num = (self.current + 1) % len(self.actors)
        return num

    def previousNum(self):
        num = self.current - 1
        if num == -1:
            num = len(self.actors) -1
        return num

    def nextOne(self):
        self.current = self.nextNum()
        self.printHeader()

    def previous(self):
        self.current = self.previousNum()
        self.printHeader()

    def removeStatus(self, target, indexes):
        actor = self.actors[target]
        indexes.sort(reverse=True)
        print 'indexes', indexes
        for index in indexes:
            del actor.stats['statuses'][index]
        self.printHeader()

    def attack(self, target, damnage, statuses):
        actor = self.actors[target]
        actor.stats['hp'] -= damnage
        for status in statuses:
            if status not in actor.stats['statuses']:
                actor.stats['statuses'].append(status)
        self.printHeader()
        self.checkActor(actor)
        return self.checkEnd()

    def checkEnd(self):
        if sum(1 for x in self.actors if type(x) is Monster) == 0:
            print 'You Win!'
            return True
        return False

    def checkActor(self, actor):
        if actor.stats['hp'] <= 0:
            self.actors.remove(actor)
            self.current = self.current % len(self.actors)
            self.printHeader()
            print '{0}{1} is DEAD at {2} HP!{3}\n'.format(Color.RED, actor.stats['name'], actor.stats['hp'], Color.END)
        elif actor.bloodied == False and actor.stats['hp'] <= (actor.stats['max_hp']/2.0):
            actor.bloodied = True
            self.printHeader()
            print '{0}{1} is Bloodied at {2} HP!{3}\n'.format(Color.RED, actor.stats['name'], actor.stats['hp'], Color.END)
        else:
            print '{0}{1} has {2} HP left{3}\n'.format(Color.RED, actor.stats['name'], actor.stats['hp'], Color.END)

    def autoRemoveStatus(self, indexes):
        actor = self.actors[self.current]
        if not type(actor) is Monster:
            return False
        statuses = actor.stats['statuses']

        if len(indexes) == 0:
            indexes = range(len(statuses))

        removed = []
        indexes.sort(reverse=True)
        for index in indexes:
            if Die(20).getVal() >= 10:
                removed.append(actor.stats['statuses'][index])
                del actor.stats['statuses'][index]
        self.printHeader()
        print 'Removed: {0}{1}{2}\n'.format(Color.RED, removed, Color.END)
        print 'Remaining: {0}{1}{2}\n'.format(Color.RED, actor.stats['statuses'], Color.END)

class Application(Tkinter.Frame):
    def __init__(self, master):
        Tkinter.Frame.__init__(self, master)
        self.master.minsize(width=100, height=100)
        self.master.config()

        self.master.bind('<Left>', self.left_key)
        self.master.bind('<Right>', self.right_key)
        self.master.bind('<Up>', self.up_key)
        self.master.bind('<Down>', self.down_key)
        self.master.bind('<Return>', self.enter_key)

        self.main_frame = Tkinter.Frame()
        self.main_frame.pack(fill='both', expand=True)
        self.pack()

        self.tbox = Tkinter.Text(self.master)
        self.tbox.pack()
        self.tbox.focus_set()    

        ######################
        self.completekey = None
        self.state = 'new'
        self.encounter = Encounter()

        os.system('cls' if os.name == 'nt' else 'clear')
        self.loadActors('data/players.txt', Player)
        
        print 'what monster file do you want?'
        m_fps = glob('data/monsters*.txt')
        m_fps.sort()
        for i, fp in enumerate(m_fps):
            print '{0}) {1}'.format(i, fp)
        reply = int(raw_input('--> '))
        if reply < len(m_fps):
            self.loadActors(m_fps[reply], Monster)
        else:
            print 'error'

        self.getInit()
        self.encounter.printHeader()

    def enter_key(self, event):
        try:
            text = self.tbox.get(1.0,Tkinter.END)
            self.tbox.delete(1.0,Tkinter.END)

            action = text.strip().split()[0]
            text = text.strip().split()[1:]
            print text
            if action == 'a':
                target = int(text[0])
                damnage = int(text[1])
                statuses = text[2:]

                end = self.encounter.attack(target, damnage, statuses)

            elif action == 'load':
                self.encounter = Encounter()
                self.preloop()

            elif action == 'roll':
                if text:
                    dice, singles = Parser.parseRoll(text)
                    for d in dice:
                        print d
                    print 'singles', singles

            elif action == 'exit':
                os.exit(0)

            elif action[0] == 'init':
                self.getInit()
                print '\n'

            elif action == 's':
                target = int(text[0])
                indexes = [int(x) for x in text[1:]]

                self.encounter.removeStatus(target, indexes)

            elif action == 'ss':
                indexes = [int(x) for x in text]
                self.encounter.autoRemoveStatus(indexes)
        except:
            print 'Input error, try again'

    def getInit(self):
        print 'Enter init for:'
        for actor in self.encounter.actors:
            if type(actor) is Player:
                print actor.stats['name']
                reply = int(raw_input('--> '))
                actor.stats['init'] = int(reply)
        self.encounter.initOrder()

    def loadActors(self, filepath, actor_type):
        actors = Parser.readActors(filepath, actor_type)
        for actor in actors:
            self.encounter.addActor(actor)

    def left_key(self, event):
        if len(self.tbox.get(1.0,Tkinter.END)) == 1:
            self.encounter.shiftUp()

    def right_key(self, event):
        if len(self.tbox.get(1.0,Tkinter.END)) == 1:
            self.encounter.shiftDown()

    def up_key(self, event):
        if len(self.tbox.get(1.0,Tkinter.END)) == 1:
            self.encounter.previous()

    def down_key(self, event):
        if len(self.tbox.get(1.0,Tkinter.END)) == 1:
            self.encounter.nextOne()

def main():
    root = Tkinter.Tk()
    app = Application(root)
    app.mainloop()

if __name__ == '__main__':
    main()
