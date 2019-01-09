from random import randint


class UnitMixin:
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
                elif self.unit_type == 'soldier':
                    self.recharge = randint(100, 2000)
                self.can_attack = True
