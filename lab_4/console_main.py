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
        print('Choose the tank:')
        tanks = player.get_tanks()
        for c in tanks:
            print(f'{c.get_name()}')
        print('exit')
        tank_name = input()
        credits, text = player.lets_battle(s, tank_name)
        print(text)
        if credits != 0:
            print(f'You earned {credits} credits per battle')

    elif choice == command_list[1]:
        print('Available to purchase tanks:')
        available_to_purchase = player.find_available_to_purchase(s)
        if available_to_purchase:
            for c in available_to_purchase:
                print(f'{c.get_name()} - {c.get_price()}')
            print('Input tank name:')
            tank_name = input()
            was_bought = player.buy_tank(s, tank_name)
            if was_bought:
                print('The tank was bought successfully!')
            else:
                print('Smth went wrong ;(')

        print('Waiting for the next command...')
    elif choice == command_list[2]:
        print('Input name: ', end='')
        name = input()
        was_changed = player.change_nickname(s, name)
        if was_changed:
            print('The nickname was changed successfully!')
        else:
            print('Something went wrong ;(')
        print('Waiting for the next command...')
    elif choice == command_list[3]:
        player = choose_account(s)
    elif choice == command_list[4]:
        print(*command_list, sep='\n')
    elif choice == command_list[5]:
        break
    else:
        print('To see the list of available commands print help')
