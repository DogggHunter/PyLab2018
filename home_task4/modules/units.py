from abc import ABC, abstractmethod
from random import randint, choice, random
from functools import reduce


class Unit(ABC):
    def __init__(self):
        self.health = 100.0
        self.recharge = randint(100, 2000)
        self.isAlive = True
        self.can_attack = True
        self.unit_type = None

    def update(self, tick):
        if not self.can_attack:
            self.recharge -= tick
            if self.recharge <= 0:
                if self.unit_type == 'vehicle':
                    self.recharge = randint(1000, 2000)
                else:
                    self.recharge = randint(100, 2000)
                self.can_attack = True

    @abstractmethod
    def attack(self):
        pass

    @abstractmethod
    def damage(self, strategy):
        pass

    @abstractmethod
    def deal_damage(self, dmg):
        pass

    @abstractmethod
    def mod_experience(self):
        pass


class Soldier(Unit):
    def __init__(self):
        super().__init__()
        self.experience = 0
        self.unit_type = 'soldier'

    def update(self, tick):
        super().update(tick)

    def attack(self):
        return 0.5 * (1 + self.health / 100) * randint(50 + self.experience, 100) / 100

    def damage(self, strategy=False):
        if strategy:
            return 0.05 + self.experience / 100
        else:
            if random() < self.attack() and self.can_attack:
                self.mod_experience()
                self.can_attack = False
                return 0.05 + self.experience / 100
            else:
                return 0

    def deal_damage(self, dmg):
        self.health -= dmg
        if self.health <= 0:
            self.isAlive = False

    def mod_experience(self):
        if self.experience < 50:
            self.experience += 1


class Vehicle(Unit):
    def __init__(self):
        super().__init__()
        self.operators = [Soldier() for _ in range(randint(1, 3))]
        self.recharge = randint(1000, 2000)
        self.list_for_remove = []
        self.unit_type = 'vehicle'

    def update(self, tick):
        super().update(tick)

    def remove_dead_soldier(self):
        for soldier in self.list_for_remove:
            self.operators.remove(soldier)
        self.list_for_remove.clear()

    def attack(self):
        return 0.5 * (1 + self.health / 100) * \
               reduce(lambda x, y: x*y, [soldier.attack() for soldier in self.operators])**(1.0/len(self.operators))

    def damage(self, strategy=False):
        if strategy:
            return 0.1 + sum([soldier.experience / 100 for soldier in self.operators])
        else:
            if random() < self.attack() and self.can_attack:
                self.mod_experience()
                self.can_attack = False
                return 0.1 + sum([soldier.experience / 100 for soldier in self.operators])
            else:
                return 0

    def deal_damage(self, dmg):
        self.health -= dmg * 0.6
        if self.health <= 0:
            for soldier in self.operators:
                soldier.isAlive = False
            self.isAlive = False
            return
        rand_soldier = choice(self.operators)
        for soldier in self.operators:
            if soldier != rand_soldier:
                soldier.deal_damage(dmg * 0.1)
            else:
                soldier.deal_damage(dmg * 0.2)
            if not soldier.isAlive:
                self.list_for_remove.append(soldier)

        if self.list_for_remove:
            self.remove_dead_soldier()

        if not self.operators:
            self.isAlive = False

    def mod_experience(self):
        for soldier in self.operators:
            soldier.mod_experience()

