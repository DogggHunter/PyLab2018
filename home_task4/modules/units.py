from abc import ABC, abstractmethod
from random import choice, random
from functools import reduce
from modules.UnitMixin import *


class Factory:
    @staticmethod
    def create(_type):
        if _type == "Soldier":
            return Soldier()
        if _type == "Vehicle":
            return Vehicle()
        assert 0, "Bad unit creation: " + _type

    @staticmethod
    def random_unit_gen(count):
        types = Unit.__subclasses__()
        for i in range(count):
            yield choice(types).__name__


class Unit(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def attack(self):
        pass

    @abstractmethod
    def attack_chance(self):
        pass

    @abstractmethod
    def damage(self):
        pass

    @abstractmethod
    def deal_damage(self, dmg):
        pass

    @abstractmethod
    def mod_experience(self):
        pass


class Soldier(UnitMixin, Unit):
    def __init__(self):
        super().__init__()
        self.experience = 0
        self.unit_type = 'soldier'

    def attack(self):
        if random() < self.attack_chance() and self.can_attack:
            return True
        return False

    def attack_chance(self):
        return 0.5 * (1 + self.health / 100) * randint(50 + self.experience, 100) / 100

    def damage(self):
        return 0.05 + self.experience / 100

    def deal_damage(self, dmg):
        self.health -= dmg
        if self.health <= 0:
            self.isAlive = False

    def mod_experience(self):
        if self.experience < 50:
            self.experience += 1

    def update(self, tick):
        super().update(tick)


class Vehicle(UnitMixin, Unit):
    def __init__(self):
        super().__init__()
        self.operators = [Factory.create("Soldier") for _ in range(randint(1, 3))]
        self.recharge = randint(1000, 2000)
        self.list_for_remove = []
        self.unit_type = 'vehicle'

    def attack(self):
        if random() < self.attack_chance() and self.can_attack:
            return True
        return False

    def attack_chance(self):
        return 0.5 * (1 + self.health / 100) * \
               reduce(lambda x, y: x*y, [soldier.attack_chance() for soldier in self.operators])**(1.0/len(self.operators))

    def damage(self):
        return 0.1 + sum([soldier.experience / 100 for soldier in self.operators])

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

    def update(self, tick):
        super().update(tick)

    def remove_dead_soldier(self):
        for soldier in self.list_for_remove:
            self.operators.remove(soldier)
        self.list_for_remove.clear()
