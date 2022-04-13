from server_wot import*


s = Server()


def choose_account(s: Server) -> Player:
    print('Choose an account: ')
    for i in range(len(s.get_player_list())):
        print('Number', i)
        print(s.get_player_list()[i].get_nickname())
        print(f'Won Battles: {s.get_player_list()[i].get_won_battles()}')
        print(f'Battles: {s.get_player_list()[i].get_battle()}')
        print(f'Credits: {s.get_player_list()[i].get_credits()}')
        print('Tanks')
        for tank in s.get_player_list()[i].get_tanks():
            print(tank)
        print('*'*20)
    choice: int = int(input())
    player = s.get_player_list()[choice]
    return player

command_list = ['start battle', 'buy a tank', 'change nickname', 'choose account', 'help', 'exit' ]
player = choose_account(s)
print(*command_list, sep='\n')
while True:
    choice: str = input()
    if choice == command_list[0]:
        player.lets_battle(s)
    elif choice == command_list[1]:
        player.buy_tank(s)
    elif choice == command_list[2]:
        player.change_nickname(s)
    elif choice == command_list[3]:
        player = choose_account(s)
    elif choice == command_list[4]:
        print(*command_list, sep='\n')
    elif choice == command_list[5]:
        break
    else:
        print('To see the list of available commands print help')
