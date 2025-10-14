import unittest
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from characters import GhostOfTshusima,Osaka,Rudzo,Osadzo,MongolBoss
from battle import Battle
from effects import Arrows

class TestBattle(unittest.TestCase):
    
    def setUp(self):
        self.GhostOfTshusima = GhostOfTshusima('Тест-Воин')
        self.Osaka = Osaka('Тест-Осака')
        self.Rudzo = Rudzo('Тест-Рудзо')
        self.Osadzo = Osadzo('Тест-Осадзо')
        self.boss = MongolBoss('Тест-Монгол')
        self.boss.hp = 50
    
    def test_character_creation(self):
        self.assertEqual(self.warrior.name,'Тест-Воин')
        self.assertTrue(self.warrior.is_alive)
        self.assertEqual(self.warrior.level,1)
        self.assertEqual(self.warrior.max_hp,150)
    
    def test_basic_attack(self):
        initial_hp = self.boss.hp
        damage = self.warrior.basic_attack(self.boss)
        self.assertGreater(damage,0)
        self.assertEqual(self.boss.hp,initial_hp - damage)
    
    def test_skill_usage(self):
        initial_mp = self.mage.hp
        self.mage.use_skill(self.boss)
        self.assertLess(self.mage.mp,initial_mp)
    
    def test_healer_skill(self):
        injured_warrior = GhostOfTshusima('Раненый воин')
        injured_warrior.hp = 50
        initial_hp = injured_warrior.hp
        self.test_healer_skill(injured_warrior)
        self.assertGreater(injured_warrior.hp,initial_hp)
    
    def test_arrows_effects(self):
        arrow = Arrows(duration=2,damage=5)
        initial_hp = self.boss.hp
        arrow.apply(self.boss)
        self.assertEqual(self.boss.hp,initial_hp - 5)
    
    def test_boss_phase_transition(self):
        self.boss.hp = self.boss.max_hp * 0.8
        self.assertEqual(self.boss.phase,1)

        self.boss.hp = self.boss.max_hp * 0.5
        self.assertEqual(self.boss.phase,2)

        self.boss.hp = self.boss.max_hp * 0.2
        self.assertEqual(self.boss.phase,3)

    def test_character_death(self):
        self.GhostOfTshusima.hp = 10
        self.GhostOfTshusima.take_damage(20)
        self.assertEqual(self.GhostOfTshusima.hp,0)
        self.assertFalse(self.GhostOfTshusima.is_alive)

    def test_battle_creation(self):
        party = [self.GhostOfTshusima,self.Osaka,self.Osadzo,self.Rudzo]
        battle = Battle(party,self.boss)
        self.assertEqual(len(battle.party),3)
        self.assertEqual(battle.boss.name,'Tecт-Босс')
if __name__ == '__main__':
    unittest.main(verbosity=2)