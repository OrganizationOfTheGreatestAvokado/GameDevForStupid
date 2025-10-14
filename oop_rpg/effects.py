from abc import ABC, abstractmethod

class Effect(ABC):
    def __init__(self,name,duration):
        self.name = name
        self.duration = duration
    @abstractmethod
    def apply(self,target):
        pass

class Arrows(Effect):
    def __init__(self,duration = 3, damage = 5):
        super().__init__("Стрела", duration)
        self.damage = damage

    def apply(self, target):
        target.take_damage(self.damage)
        target.add_log(f'{target.name} получает {self.damage} урона от стрелы')
class Shield(Effect):
    def __init__(self,duration = 2, shield_amount = 20):
        super().__init__('Щит', duration)
        self.shield_amount = shield_amount
        self.remaining_shield = shield_amount
    def apply(self,target):
        pass
    