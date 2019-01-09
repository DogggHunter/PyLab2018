from modules.units import *
from config import *
from itertools import count


class Squad:
    def __init__(self):
        self.isAlive = True
        self.units = [Factory.create(unit) for unit in Factory.random_unit_gen(CONFIG['num_unit_per_squad'])]
        self.list_for_remove = []

    def attack(self, enemy_squad):
        for unit in self.units:
            if unit.attack() and enemy_squad.isAlive:
                enemy_squad.deal_damage(unit.damage()*CONFIG['multiple_damage'])
                unit.mod_experience()
                unit.can_attack = False

    def attack_chance(self):
        return reduce(lambda x, y: x * y, [unit.attack_chance() for unit in self.units]) ** (1.0 / len(self.units))

    def damage(self):
        return sum([unit.damage() for unit in self.units])

    def deal_damage(self, dmg):
        dmg_per_unit = dmg / len(self.units)
        for unit in self.units:
            unit.deal_damage(dmg_per_unit)
            if not unit.isAlive:
                self.list_for_remove.append(unit)
        if self.list_for_remove:
            self.remove_dead_unit()
        if not self.units:
            self.isAlive = False

    def update(self, tick):
        for unit in self.units:
            unit.update(tick)

    def remove_dead_unit(self):
        for unit in self.list_for_remove:
            self.units.remove(unit)
        self.list_for_remove.clear()


class Army:
    _count = count(0)

    def __init__(self):
        self.squads = [Squad() for _ in range(CONFIG['num_squads_per_army'])]
        self.isAlive = True
        self.name = f"Army {next(self._count)+1}"
        self.list_for_remove = []
        self.max_health = self.get_army_health()
        self.health75 = True
        self.health50 = True
        self.health25 = True
        self.health0 = True

    def get_army_health(self):
        health = 0.0
        for squad in self.squads:
            for unit in squad.units:
                health += unit.health
        return health

    def remove_dead_squads(self):
        for squad in self.list_for_remove:
            self.squads.remove(squad)
        self.list_for_remove.clear()

    def update(self, tick):
        for squad in self.squads:
            if not squad.isAlive:
                self.list_for_remove.append(squad)
            else:
                squad.update(tick)

        health = self.get_army_health()
        if health <= 0 and self.health0:
            print(self.name, " suffered a defeat")
            self.health0 = False
        elif health <= self.max_health * 0.25 and self.health25:
            print(self.name, " has 25% hp")
            self.health25 = False
        elif health <= self.max_health * 0.5 and self.health50:
            print(self.name, " has 50% hp")
            self.health50 = False
        elif health <= self.max_health * 0.75 and self.health75:
            print(self.name, " has 75% hp")
            self.health75 = False

        if self.list_for_remove:
            self.remove_dead_squads()

        if not self.squads:
            self.isAlive = False

    def choice_squad(self):
        if CONFIG['attack_strategy'] == 'random':
            return choice(self.squads)
        elif CONFIG['attack_strategy'] == 'weakest':
            return min(self.squads, key=lambda squad: squad.damage())
        elif CONFIG['attack_strategy'] == 'strongest':
            return max(self.squads, key=lambda squad: squad.damage())

    def start_attack(self, enemy_squad: Squad):
        for squad in self.squads:
            if enemy_squad.isAlive and squad.attack_chance() >= enemy_squad.attack_chance():
                squad.attack(enemy_squad)

