import random
import time

WAIT_TIME = 0.5

# my coworker be losing his fucking mind bro LMAOQOOO what is this

class Weapon:
    # класс для создания оружия

    def __init__(self, name, damage, special_damage, mana_cost):
        self.name = name
        self.damage = damage  # базовый урон
        self.special_damage = special_damage  # урон спец атаки
        self.mana_cost = mana_cost  # стоимость маны


class Character:
    # класс для создания врагов
    # сами враги если что в конце кода
    def __init__(self, name, health, mana, weapon):
        self.name = name
        self.health = health  # здоровье
        self.mana = mana  # количество маны
        self.weapon = weapon  # оружие из класса Weapon

    def is_alive(self):
        # проверка жив ли персонаж
        return self.health > 0

    def basic_attack(self, target):
        # физическая атака
        target.health -= self.weapon.damage
        time.sleep(WAIT_TIME)
        print(f"{self.name} атакует {target.name} на {self.weapon.damage} урона!")

    def special_attack(self, target):
        # магическая атака
        if self.mana >= self.weapon.mana_cost:
            self.mana -= self.weapon.mana_cost
            target.health -= self.weapon.special_damage
            time.sleep(WAIT_TIME)
            print(
                f"{self.name} использует специальную атаку! "
                f"{target.name} получает {self.weapon.special_damage} урона!"
            )
            return True
        print("Недостаточно маны!")
        return False

    def heal_attack(self):
        # лечение
        if self.mana >= self.weapon.mana_cost:
            self.mana -= self.weapon.mana_cost
            heal_amount = random.randint(5, 10)  # рандомные криты тф2 момент
            self.health += heal_amount
            time.sleep(WAIT_TIME)
            print(f"{self.name} лечится на {heal_amount} очков!")
            return True
        print("Недостаточно маны!")
        return False


class Player(Character):
    # класс игрока

    def __init__(self, name, health, mana, weapon, character_class):
        super().__init__(name, health, mana, weapon)
        self.level = 1  # начальный уровень
        self.exp = 0  # текущий опыт
        self.exp_to_next_level = 100  # опыт для следующего уровня
        self.character_class = character_class  # класс персонажа

    def gain_exp(self, amount):
        # добавление опыта и проверка уровня
        self.exp += amount
        print(f"\n{self.name} получает {amount} опыта!")
        if self.exp >= self.exp_to_next_level:
            self.level_up()

    def level_up(self):
        # повышение уровня и характеристик
        self.level += 1
        self.exp -= self.exp_to_next_level
        self.exp_to_next_level = int(self.exp_to_next_level * 1.5)  # увеличение планки опыта

        # определение прироста характеристик в зависимости от класса
        if self.character_class == "Воин":
            health_gain = 10
            mana_gain = 5
        elif self.character_class == "Маг":
            health_gain = 5
            mana_gain = 15
        elif self.character_class == "Разбойник":
            health_gain = 8
            mana_gain = 8
        else:
            health_gain = 0
            mana_gain = 0

        self.health += health_gain
        self.mana += mana_gain
        print(f"{self.name} достиг уровня {self.level}!")
        print(f"Здоровье: +{health_gain}, Мана: +{mana_gain}")
        print(f"Требуется опыта для следующего уровня: {self.exp_to_next_level}")

        # повторная проверка, если опыт остался после повышения
        if self.exp >= self.exp_to_next_level:
            self.level_up()

    def choose_action(self, target):
        # выбор действия игроком
        time.sleep(WAIT_TIME)
        print("\nДоступные действия:")
        print("1. Обычная атака")
        print(f"2. Магическая атака, стоимость {self.weapon.mana_cost} маны")
        print(f"3. Лечение, стоимость {self.weapon.mana_cost + random.randint(3, 5)} маны")

        while True:
            choice = input("Выберите действие (1-3): ")
            if choice == '1':
                self.basic_attack(target)
                return
            if choice == '2':
                if self.special_attack(target):
                    return
            if choice == '3':
                if self.heal_attack():
                    return
            print("Неверный ввод!")


class Monster(Character):
    # класс монстра

    def __init__(self, name, health, mana, weapon, exp_reward):
        super().__init__(name, health, mana, weapon)
        self.exp_reward = exp_reward  # опыт за победу над монстром
        self.initial_health = health  # начальное здоровье
        self.initial_mana = mana  # начальная мана

    def reset_stats(self):
        # сброс здоровья и маны к начальным значениям
        self.health = self.initial_health
        self.mana = self.initial_mana

    def choose_action(self, target):
        # случайный выбор атаки или лечения для монстра
        if self.health <= 10:  # если меньше 10 хп, хилимся
            self.heal_attack()
        elif self.mana >= self.weapon.mana_cost and random.random() < 0.5:  # если больше 10 хп, рандомная атака
            self.special_attack(target)
        else:
            self.basic_attack(target)


class BattleSystem:
    # система управления боем

    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy

    def print_stats(self):
        # вывод статистики
        print("\n=== Текущая статистика ===")
        print(f"{self.player.name}: Ур. {self.player.level}, Опыт: {self.player.exp}/{self.player.exp_to_next_level}")
        print(f"Здоровье: {self.player.health}, Мана: {self.player.mana}")
        print(f"{self.enemy.name}: Здоровье - {self.enemy.health}, Мана - {self.enemy.mana}")
        print("=========================")

    def start_battle(self):
        # запуск боя
        time.sleep(WAIT_TIME)

        # сброс статистики врага перед началом боя
        self.enemy.reset_stats()

        print(f"\n{self.player.name} проходит дальше в лес... И встречает в нем {self.enemy.name}!")

        while self.player.is_alive() and self.enemy.is_alive():
            self.print_stats()
            self.player.choose_action(self.enemy)
            if not self.enemy.is_alive():
                break

            self.enemy.choose_action(self.player)

        if self.player.is_alive():
            print(f"\n{self.enemy.name} повержен! {self.player.name} побеждает!")
            self.player.gain_exp(self.enemy.exp_reward)  # начисление опыта
            return True
        print(f"\n{self.player.name} пал в бою...")
        return False


def choose_class():
    # выбор класса персонажа
    classes = {
        # словарь с классами
        '1': {
            'name': 'Воин',  # имя
            'health': 65,  # здоровье
            'mana': 20,  # мана
            'weapon': Weapon("Меч", damage=16, special_damage=6, mana_cost=15)  # оружие
        },
        '2': {
            'name': 'Маг',
            'health': 45,
            'mana': 60,
            'weapon': Weapon("Посох", damage=8, special_damage=30, mana_cost=18)
        },
        '3': {
            'name': 'Разбойник',
            'health': 55,
            'mana': 40,
            'weapon': Weapon("Дубина", damage=10, special_damage=13, mana_cost=12)
        }
    }

    print("\nВыберите класс персонажа:")
    print("1. Воин (высокое здоровье, физический урон)")
    print("2. Маг (низкое здоровье, магический урон)")
    print("3. Разбойник (сбалансированные характеристики)")

    while True:
        choice = input("Введите номер класса (1-3): ")
        if choice in classes:
            return classes[choice]
        print("Неверный ввод!")


if __name__ == "__main__":
    print("=== НАЧАЛО ИГРЫ ===")

    username = input('Введите ваше имя:\n')

    # сюжет
    time.sleep(WAIT_TIME)
    print(f'{username} находит старую карту, которая указывает на местонахождение древнего артефакта.')
    time.sleep(WAIT_TIME * 6)
    print('Артефакт обладает огромной силой, но его использование может быть опасным.')
    time.sleep(WAIT_TIME * 6)
    print(f'Но {username} все таки решает забрать его. Путь проходит через опасный лес, к которому он уже подходил...')
    time.sleep(WAIT_TIME * 6)

    class_info = choose_class()

    # описание статистики игрока

    player = Player(
        name=username,  # имя
        health=class_info['health'],  # здоровье
        mana=class_info['mana'],  # мана
        weapon=class_info['weapon'],  # оружие
        character_class=class_info['name']  # класс игрока
    )

    enemies = [
        # список врагов. хотите добавить больше, вписывайте сюда
        Monster(name="Гоблин", health=50, mana=20, weapon=Weapon("Дубина", 8, 12, 10), exp_reward=50),
        Monster(name="Темный маг", health=70, mana=50, weapon=Weapon("Посох", 8, 25, 20), exp_reward=100)
    ]

    for _ in range(2):
        enemy = random.choice(enemies)  # рандомный выбор игроков
        battle = BattleSystem(player, enemy)
        if not battle.start_battle():
            break
