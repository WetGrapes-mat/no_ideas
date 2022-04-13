from __future__ import annotations
import random
import json
import time


class Player:

    def __init__(self, nickname: str, won_battles: int, battles: int, credits: int, tank: list[Tank]) -> None:
        self.__nickname = nickname
        self.__won_battles = won_battles
        self.__battles = battles
        self.__credits = credits
        self.__tanks = tank
        self.__win_rate: float = (self.__won_battles / self.__battles) * 100

    def get_nickname(self) -> str:
        return self.__nickname

    def get_winrate(self) -> float:
        return self.__win_rate

    def get_won_battles(self) -> int:
        return self.__won_battles

    def get_battle(self) -> int:
        return self.__battles

    def get_credits(self) -> int:
        return self.__credits

    def get_tanks(self) -> list:
        return self.__tanks

    def lets_battle(self, server: Server) -> None:
        print('Choose the tank:')
        tanks: list[Tank] = self.__tanks
        for i in range(len(tanks)):
            print(tanks[i].get_name())
        print('exit')
        choice: str = input()
        for i in range(len(tanks)):
            if choice == 'exit':
                return
            elif choice == tanks[i].get_name():
                my_tank: Tank = tanks[i]
                earned_credits, battle_won = server.start_battle(my_tank, self)
                self.__credits += earned_credits
                print(f'Earned {earned_credits} credits per battle')
                self.__won_battles += battle_won
                self.__battles += 1
                self.__win_rate = (self.__won_battles / self.__battles) * 100
                Server.set_players_in_file(server.get_player_list())
                break
        else:
            print('WRONG INPUT!')
            self.lets_battle(server)

    def buy_tank(self, server: Server) -> None:
        tanks: list[Tank] = server.get_tank_list()
        available_to_purchase: list[Tank] = []
        for c in tanks:
            if c not in self.__tanks:
                available_to_purchase.append(c)
            else:
                continue
        print('Available to purchase tanks:')
        for i in range(len(available_to_purchase)):
            print(f'{available_to_purchase[i].get_name()} - {available_to_purchase[i].get_price()}')
        if available_to_purchase == []:
            print('You have all tanks!')
        else:
            print('exit')

        if available_to_purchase != []:
            choice: str = input()
            for i in range(len(available_to_purchase)):
                if choice == 'exit':
                    return
                elif choice == available_to_purchase[i].get_name():
                    new_tank: Tank = available_to_purchase[i]
                    if self.__credits >= new_tank.get_price():
                        self.__credits -= new_tank.get_price()
                        self.__tanks.append(new_tank)
                        Server.set_players_in_file(server.get_player_list())
                    else:
                        print('Not enough credits :(')
                        self.buy_tank(server)
                    break
            else:
                print('WRONG INPUT!')
                self.buy_tank(server)

    def change_nickname(self, server) -> None:
        new_nickname: str = input('Enter new nickname: ')
        print('Are you sure? Changing your nickname costs 50_000 credits')
        print('yes\nno')
        choice: str = input()
        if choice == 'yes':
            self.__nickname = new_nickname
            self.__credits -= 50_000
            Server.set_players_in_file(server.get_player_list())
        elif choice == 'no':
            return
        else:
            print('WRONG INPUT!')
            self.change_nickname(server)


class Tank:
    def __init__(self, name: str, id: int, price: int, hp: int, force: int) -> None:
        self.__name = name
        self.__id = id
        self.__price = price
        self.__heal_points = hp
        self.__force = force

    def __str__(self):
        return self.__name

    def get_name(self) -> str:
        return self.__name

    def get_id(self) -> int:
        return self.__id

    def get_price(self) -> int:
        return self.__price

    def get_heal_points(self) -> int:
        return self.__heal_points

    def get_force(self) -> int:
        return self.__force


class Bot:
    __nickname: str = ''
    __tank: Tank = None    # ???
    __win_rate: float = 0    # float

    def __init__(self, server: Server) -> None:
        self.generate_nickname()
        self.generate_tank(server)
        self.generate_win_rate()

    def get_win_rate(self) -> float:
        return self.__win_rate

    def get_nickname(self) -> str:
        return self.__nickname

    def get_tank(self) -> Tank:
        return self.__tank

    def generate_win_rate(self) -> None:
        choice: int = random.randint(0, 100)
        if 0 <= choice < 10:
            i: int = random.randint(0, 1)
            if i == 0:
                self.__win_rate = random.randint(30, 40)
            elif i == 1:
                self.__win_rate = random.randint(60, 70)
        elif 10 <= choice < 30:
            i: int = random.randint(0, 1)
            if i == 0:
                self.__win_rate = random.randint(40, 43)
            elif i == 1:
                self.__win_rate = random.randint(57, 60)
        elif 30 <= choice < 55:
            i: int = random.randint(0, 1)
            if i == 0:
                self.__win_rate = random.randint(43, 47)
            elif i == 1:
                self.__win_rate = random.randint(53, 57)
        elif 55 <= choice <= 100:
            self.__win_rate = random.randint(47, 53)

    def generate_nickname(self) -> None:
        with open('nickname.txt', 'r', encoding="utf-8") as file_nickname:
            self.__nickname = random.choice(file_nickname.readlines())

    def generate_tank(self, server: Server) -> None:
        self.__tank = random.choice(server.get_tank_list())


class Server:
    __player_list: list[Player] = []
    __tank_list: list[Tank] = []

    def __init__(self) -> None:
        self.get_tanks_from_file()
        self.get_players_from_file()

    def get_tanks_from_file(self) -> None:
        with open('tank_list.json', 'r', encoding="utf-8") as file_tank:
            tank_list = json.load(file_tank)
            for tank in tank_list['tanks']:
                self.__tank_list.append(Tank(
                    name=tank['tank_name'],
                    id=tank['tank_id'],
                    price=tank['tank_price'],
                    hp=tank['tank_hp'],
                    force=tank['tank_force']
                ))

    def get_players_from_file(self) -> None:
        with open('player_list.json', 'r', encoding="utf-8") as file_player:
            temp_tank: list[Tank] = []
            player_list = json.load(file_player)
            for player in player_list['player']:
                for tank in self.__tank_list:
                    if tank.get_id() in player['tanks']:
                        temp_tank.append(tank)
                self.__player_list.append(Player(
                    nickname=player['nickname'],
                    won_battles=player['won_battles'],
                    battles=player['battles'],
                    credits=player['credits'],
                    tank=temp_tank
                ))
                temp_tank = []

    @staticmethod
    def set_players_in_file(list_all_players: list) -> None:
        with open('player_list.json', 'r', encoding="utf-8") as file:
            counter: int = 0
            player_list = json.load(file)
            temp: list[int] = []
            for i_item in player_list['player']:
                i_item['nickname'] = list_all_players[counter].get_nickname()
                i_item['won_battles'] = list_all_players[counter].get_won_battles()
                i_item['battles'] = list_all_players[counter].get_battle()
                i_item['credits'] = list_all_players[counter].get_credits()
                for i in list_all_players[counter].get_tanks():
                    temp.append(i.get_id())
                i_item['tanks'] = temp
                temp = []
                counter += 1
            with open('player_list.json', 'w', encoding="utf-8") as w:
                json.dump(player_list, w, indent=2)

    def get_player_list(self) -> list[Player]:
        return self.__player_list

    def get_tank_list(self) -> list[Tank]:
        return self.__tank_list

    def start_battle(self, tank: Tank, player: Player) -> tuple:
        team_one: list[BattlePlayer] = []
        team_two: list[BattlePlayer] = []
        active_player: BattlePlayer = BattlePlayer(player, tank)
        team_one.append(active_player)
        for i in range(4):
            team_one.append(BattlePlayer(Bot(self)))
        for i in range(5):
            team_two.append(BattlePlayer(Bot(self)))

        battle: Battle = Battle(team_one, team_two, self.choose_map())
        team_one, team_two = battle.simulate_battle()
        hp: int = 0
          
        for p in team_one:
            hp += p.get_heal_points()
        if hp > 0:
            battle_won: int = 1
        else:
            battle_won: int = 0
        earned_credits: int = self.count_prizes(team_one[0])
        return earned_credits, battle_won

    def choose_map(self) -> str:
        maps: list[str] = ['Prohorovka', 'Malinovka', 'Himelsdorf', 'Ruinberg', 'Minsk', 'Berlin']
        mapname: str = random.choice(maps)
        return mapname

    def count_prizes(self, battle_player: BattlePlayer) -> int:
        earned_credits: int = 20_000 * battle_player.get_frags() +\
                         100 * battle_player.get_damage() - battle_player.repair_tank()
        return earned_credits


class Battle:

    def __init__(self,  teamone, teamtwo, mapname):
        self.__team_one = teamone
        self.__team_two = teamtwo
        self.__map_name = mapname
        self.__team_one_frags = [0] * 5
        self.__team_two_frags = [0] * 5
        self.__team_one_damage = [0] * 5
        self.__team_two_damage = [0] * 5

    def simulate_battle(self) -> tuple:
        print('team_one')
        print('-'*30)
        for i_1 in self.__team_one:
            print('{} -- {}'.format(i_1.get_nickname().rstrip(), i_1.get_tank().get_name()))
        print('='*30)
        print('team_two')
        print('-'*30)
        for i_2 in self.__team_two:
            print('{} -- {}'.format(i_2.get_nickname().rstrip(), i_2.get_tank().get_name()))
        print('+=' * 25)
        print('{:^46}'.format('Lets Battle'))
        print('+=' * 25)
        while True:
            hp_1: int = 0
            hp_2: int = 0
            for _1 in self.__team_one:
                hp_1 += _1.get_heal_points()
            for _2 in self.__team_two:
                hp_2 += _2.get_heal_points()

            if hp_1 == 0 or hp_2 == 0:
                if hp_1 == 0:
                    print('{:^46}'.format('TEAM TWO WIN'))
                elif hp_2 == 0:
                    print('{:^46}'.format('TEAM ONE WIN'))
                break

            curr_dmg_1: dict = {}
            curr_dmg_2: dict = {}
            curr_dmg: dict = {}

            for attacking_1 in self.__team_one:
                if attacking_1.get_heal_points() > 0:
                    while True:
                        protection_1: BattlePlayer = random.choice(self.__team_two)
                        if protection_1.get_heal_points() > 0:
                            break
                    temp: int = random.randint(1, 100)
                    if temp >= 40:
                        luck = True
                    else:
                        luck = False
                    if luck:
                        a1: float = attacking_1.get_tank().get_force() + \
                                    (attacking_1.get_tank().get_force() * (random.randint(-25, 25)/100))
                        a2: float = (1 - (attacking_1.get_winrate() / 100))
                        a3: float = (protection_1.get_winrate() / 100)
                        dmg: int = round(a1 * 4 * a2 * a3)
                        curr_dmg_1[dmg] = [attacking_1, protection_1]

            for attacking_2 in self.__team_two:
                if attacking_2.get_heal_points() > 0:
                    while True:
                        protection_2: BattlePlayer = random.choice(self.__team_one)
                        if protection_2.get_heal_points() > 0:
                            break
                    temp: int = random.randint(1, 100)
                    if temp >= 40:
                        luck = True
                    else:
                        luck = False
                    if luck:
                        a1: float = (attacking_2.get_tank().get_force() +
                                     (attacking_2.get_tank().get_force() * (random.randint(-25, 25)/100)))
                        a2: float = (1 - (attacking_2.get_winrate() / 100))
                        a3: float = (protection_2.get_winrate() / 100)
                        dmg: int = round(a1 * 4 * a2 * a3)
                        curr_dmg_2[dmg] = [attacking_2, protection_2]

            curr_dmg.update(curr_dmg_1)
            curr_dmg.update(curr_dmg_2)

            for i in range(len(curr_dmg)):
                damage = random.choice(list(curr_dmg.keys()))
                pair = curr_dmg[damage]
                if pair[0].get_heal_points() > 0 and pair[1].get_heal_points() > 0:
                    if pair[1].get_heal_points() > damage:
                        pair[1].take_self_damage(damage)
                        pair[0].take_damage(damage)
                        print('{:^15} dmg done {:^5} {:^15}'.format(pair[0].get_nickname().rstrip(), damage,
                                                                    pair[1].get_nickname().rstrip()))
                    elif pair[1].get_heal_points() < damage:
                        pair[1].take_self_damage(pair[1].get_heal_points())
                        pair[0].take_damage(pair[1].get_heal_points())
                        pair[0].take_frags()
                        print('{:^15}  {:^11}  {:^15}'.format(pair[0].get_nickname().rstrip(), 'Killed',
                                                              pair[1].get_nickname().rstrip()))
                del curr_dmg[damage]
            else:
                print('+='*25)

            time.sleep(1)
        return self.__team_one, self.__team_two


class BattlePlayer:
    # arg (Bot) or (Player, Tank)
    def __init__(self, *args) -> None:    # ???
        if len(args) == 1:
            self.__tank: Tank = args[0].get_tank()
            self.__heal_points: int = self.__tank.get_heal_points()
            self.__win_rate: float = args[0].get_win_rate()
            self.__nickname: str = args[0].get_nickname()
            self.__damage: int = 0
            self.__frags: int = 0
        elif len(args) == 2:
            self.__tank = args[1]
            self.__heal_points = args[1].get_heal_points()
            self.__win_rate = args[0].get_winrate()
            self.__nickname = args[0].get_nickname()
            self.__damage = 0
            self.__frags = 0

    def repair_tank(self) -> int:
        payment: int = (self.get_heal_points() - self.__heal_points) * 33

        return payment

    def take_self_damage(self, damage: int) -> None:
        self.__heal_points -= damage

    def take_frags(self) -> None:
        self.__frags += 1

    def take_damage(self, more_damage: int) -> None:
        self.__damage += more_damage

    def get_winrate(self) -> float:
        return self.__win_rate

    def get_heal_points(self) -> int:
        return self.__heal_points

    def get_tank(self) -> Tank:
        return self.__tank

    def get_nickname(self) -> str:
        return self.__nickname

    def get_damage(self) -> int:
        return self.__damage

    def get_frags(self) -> int:
        return self.__frags
