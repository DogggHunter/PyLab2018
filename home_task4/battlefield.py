import sched
import time
from modules.army import Army
from config import *
from random import choice


class BattleField:
    def __init__(self):
        self.armies = [Army() for _ in range(CONFIG['num_armies'])]
        self.s = None
        self.list_for_remove = []

    def remove_dead_army(self):
        for army in self.list_for_remove:
            self.armies.remove(army)
        self.list_for_remove.clear()

    def update(self, sc):
        if len(self.armies) == 1:
            print(self.armies[0].name, " WIN!!!")
            return

        for army in self.armies:
            army.update(100)
            if not army.isAlive:
                self.list_for_remove.append(army)
                continue
            enemy_armies = list([army for army in self.armies if army.isAlive])
            enemy_armies.remove(army)
            if not enemy_armies:
                continue
            victim: Army = choice(enemy_armies)
            army.start_attack(victim.choice_squad())
            victim.update(0)

        if self.list_for_remove:
            self.remove_dead_army()

        self.s.enter(0.1, 1, self.update, (sc,))

    def start(self):
        self.s = sched.scheduler(time.time, time.sleep)
        self.s.enter(0.1, 1, self.update, (self.s,))
        self.s.run()
