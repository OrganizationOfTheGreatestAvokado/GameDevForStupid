from characters import GhostOfTshusima, Osadzo,Rudzo,Osaka,MongolBoss
from battle import Battle

def create_party():
    party = [
        GhostOfTshusima('Призрак Цусимы', 5),
        Osadzo('Осадзо',5),
        Rudzo('Рудзо',5),
        Osaka('Осака',5)
    ]
    return party
def main():
    print("МИНИ-ИГРА 'ЯПОНЦЫ ПРОТИВ УСКОГЛАЗЫХ' ")
    print("=" * 50)
    party = create_party()
    boss = MongolBoss('Монгол-ускаглазых',10)
    print("\n Отряд хороших ускоглазых:")
    for i, GhostOfTshusima in enumerate(party,1):
        print(f"{i}.{GhostOfTshusima}")
    print(f"\n Босс-молокосос: {MongolBoss}")
    print(f"Фаза босса: {boss.phase}")

    input('\n Нажмите Enter чтобы начать бой...')

    battle = Battle(party,boss,seed=42)
    try:
        battle.start_battle()
        
        battle.save_battle('battle_result.json')
        print(f'\n Результаты боя сохранены в battle_result.json')
    except KeyboardInterrupt:
        print("\n\nБой прерван пользователем")
        battle.save_state("battle_unterrupted.json")
if __name__ == "__main__":
    main()
