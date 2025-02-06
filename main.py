# Импорт opencv, face_rec..., ??database??

def register():
    username = input('Enter your name: ')

    # Функция включения камеры, захвата кадра, внесение данных в БД

def login():

    # Распознавание лица (сравнение с БД)
    pass

def exit_prog():
    print('Exiting the program...')
    exit()

def incorrect_input():
    print('Incorrect input. Try it (1 - 3)')

def menu():
    welcome_list = ['=' * 25, 'Select the mode:', '1 - Registration', '2 - Log in', '3 - Exit', '=' * 25]
    print(*welcome_list, sep='\n')

def main():

    funcs_menu = {'1': register, '2': login, '3': exit_prog}

    while True:
        menu()
        choice = input('Enter the mode number: ')

        funcs_menu.get(choice, incorrect_input)()

if __name__ == '__main__':
    main()
