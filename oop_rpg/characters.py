from abc import ABC, abstractmethod

from mixins import LoggerMixin, CritMixin, SilenceMixin
from effects import Effect, Arrows

class BoundedStat:
    def __init__(self, min_val=0, max_val=100):
        self.min_val = min_val
        self.max_val = max_val
    def __set_name__(self,owner,name):
        self.private_name = f"_{name}"
    def __get__(self,obj, objtype=None):
        return getattr(obj,self.private_nameself.min_val)
    def __set(self,obj,value):
        if not (self.min_val <= value <= self.mmax_val):
            raise ValueError(f'Значение должно быть между {self.min_val} и {self.max_val}')
        setattr(obj, self.private_name, value)

class GhostOfTshusima(LoggerMixin):
    hp = BoundedStat(0,1000)
    mp = BoundedStat(0,500)
    strength = BoundedStat(1,100)
    agility = BoundedStat(1,100)
    intelligence = BoundedStat(1,100)

    def __init__(self,name,level = 1):
        self.name = name
        self.level = level
        self._hp = 100
        self._mp = 50
        self._strength = 10
        self._agility = 10
        self._intelligence = 10
        self.max_hp = 100
        self.max_mp = 50
        super().__init__()

        @property
        def is_alive(self):
            return self.hp > 0

        def take_damage(self,damage):
            self.hp = max(0,self.hp - damage)
            self.add_log(f"{self.name} получает {damage} урона! HP: {self.hp}")
        
        def heal(self, amount):
            old_hp = self.hp
            self.hp = min(self.max_hp,self.hp + amount)
            actual_heal = self.hp - old_hp
            self.add_log(f"{self.name} восстанавливает {actual_heal} HP!")
            return actual_heal
        
        def __str__(self):
            return f"{self.name} (Yp. {self.level}) - HP:{self.hp}/{self.max_hp} MP: {self.mp}/{self.max_mp}"

        def __repr__(self):
            return f"{self.__clas__.__name__}('{self.name}',{self.level})"
        
        def to_dict(self):
            return {
                'name': self.name,
                'level': self.level,
                'hp':self.hp,
                'max_hp':self.max_hp,
                'mp':self.mp,
                'max_mp':self.max_mp,
                'strength':self.strength,
                'agility':self.agility,
                'intelligence':self.intelligence
            }

class Character(GhostOfTshusima,ABC):
    def __init__(self, name, level=1):
        super().__init__(name, level)
        self.effects = []
        self.cooldowns = {}
        self.skills_used = 0
    @abstractmethod
    def basic_attack(self,target):
        pass

    @abstractmethod
    def use_skill(self,target):
        pass

    def update_effects(self):
        new_effects = []
        for effect in self.effects:
            effect.duration -= 1
            if effect.duration > 0:
                new_effects.append(effect)
                effect.apply(self)
        self.effects = new_effects

    def add_effect(self,effect):
        self.effects.append(effect)
        self.add_log(f"{self.name} получает эффект: {effect.name}")

class Osaka(Character, CritMixin):
    def __init__(self, name, level=1):
        super().__init__(name, level)
        self._strength = 20
        self._agility = 15
        self._intelligence = 5
        self.max_hp = 150
        self.hp = 150
        self.max_mp = 30
        self.mp = 30
    
    def basic_attack(self, target):
        if hasattr(self,'is_silenced') and self.is_silenced:
            self.add_log(f"{self.name} кушает няма-няма и не хочет атаковать!")
            return 0
        damage = self.strength + self.level * 2
        crit_damage = self.calculate_crit(damage,0.2)
        target.take_damage(crit_damage)
        return crit_damage
    
    def use_skill(self, target):
        if hasattr(self,'is_silenced') and self.is_silenced:
            self.add_log(f"{self.name} только что поел и ему лень использовать навык, может чуть позже..?")
            return 0
        
        if self.mp < 15:
            self.add_log(f'Кому-то недостаточно MP для использования навыка')
            return 0
        self.mp -= 15
        damage = self.strength * 2 + self.level * 3
        self.add_log(f"{self.name} использует супершанс!")
        target.take_damage(damage)

        import random
        if random.random() < 0.3:
            target.add_log(f"{target.name} оглушен на 1 ход!")
        return damage

class Rudzo(Character, CritMixin, SilenceMixin):
    def __init__(self, name, level=1):
        super().__init__(name, level)
        self._strength = 5
        self._agility = 10
        self._intelligence = 25
        self.max_hp = 80
        self.hp = 80
        self.max_mp = 100
        self.mp = 100
        SilenceMixin.__init__(self)
    def basic_attack(self,target):
        if self.is_silenced:
            self.add_log(f"{self.name} смотрит на птичку и не может атаковать")
            return 0 

        damage = self.intelligence + self.level
        target.take_damage(damage)
        return damage

    def use_skill(self,target):
        if self.is_silenced:
            self.add_log(f"{self.name} задумался о смысле жизни, ему не до атаки")
            return 0
        if self.mp < 25:
            self.add_log(f'Недостаточно МР для использования навыка!')
            return 0
        self.mp -= 25
        self.add_log(f"{self.name} использует свою супер-пупер-мега-тактику!!!")
        damage = self.intelligence * 1.5
        crit_damage = self.calculate_crit(damage, 0.15)
        target.take_damage(crit_damage)
        arrow = Arrows(duration = 3, damage = 7)
        target.add_effect(arrow)
        return crit_damage
class Osadzo(Character, SilenceMixin):
    def __init__(self, name, level=1):
        super().__init__(name, level)
        self._strength = 8
        self._agility = 12
        self._intelligence = 20
        self.max_hp = 100
        self.hp = 100
        self.max_mp = 80
        self.mp = 80
        SilenceMixin.__init__(self)

    def basic_attack(self, target):
        if self.is_silenced:
            self.add_log(f"{self.name} не может атаковать (честно, вообще не знаю почему)")
            return 0
        damage = self.intelligence * 0.7
        target.take_damage(damage)
        return damage
    
    def use_skill(self,target):
        if self.is_silenced:
            self.add_log(f"{self.name} не может использовать навык ( no comments... )")
            return 0
        if self.mp < 20:
            self.add_log(f"Недостаточно МР для использования навыка")
            return 0 
        self.mp -= 20
        self.add_log(f"{self.name} использует целебный японский мат!")
        heal_amount = self.intelligence * 2 + self.level * 3
        actual_heal = target.heal(heal_amount)
        return -actual_heal

class MongolBoss(ABC):
    @abstractmethod
    def execute(self, boss, targets):
        pass

class ZloiMongol(MongolBoss):
    def execute(self,boss, targets):
        boss.add_log('Монгол какой-то злобный..Сейчас будет ж##a')
        weakest = min(targets, key=lambda x: x.hp)
        damage = boss.strength * 2
        weakest.take_damage(damage)
        return damage
class DefensiveMongol(MongolBoss):
    def execute(self,boss,targets):
        boss.add_log('Хааааа, туда этого жирного, смотри, он лечится!!!')
        heal_amount = boss.intelligence * 1.5
        actual_heal = boss.heal(heal_amount)
        return -actual_heal

class PlevokMongola(MongolBoss):
    def execute(self,boss,targets):
        boss.add_log('Монгол плюнул!!!')
        return 0 

class Mongol(Character,CritMixin):
    def __init__(self, name, level=1):
        super().__init__(name, level)
        self._strength = 30
        self._agility = 20
        self._intelligence = 25
        self.max_hp = 500
        self.hp = 500
        self.max_mp = 200
        self.mp = 200

        self.strategies = {
            'aggressive': ZloiMongol(),
            'defensive':  DefensiveMongol(),
            'debuff': PlevokMongola()
            }
        self.current_strategy = 'aggressive'
    def basic_attack(self, target):
        damage = self.strength + self.level
        crit_damage = self.calculate_crit(damage,0.25)
        target.take_damage(crit_damage)
        return crit_damage
    def use_skill(self, target):
        if self.hp < self.max_hp * 0.3:
            self.current_strategy = 'aggressive'
        elif self.hp < self.max_hp * 0.6:
            self.current_strategy = 'debuff'
        else:
            self.current_strategy = 'defensive'
        strategy = self.strategies[self.current_strategy]
        return strategy.execute(self, [target] if target else [])
    @property
    def phase(self):
        if self.hp > self.max_hp * 0.7:
            return 1
        elif self.hp > self.max_hp * 0.4:
            return 2
        else:
            return 3