import detect.camera as cam
import detect.face_recogn as recogn
import database.db as db

def register():
    while True:
        username = input('Enter your name: ')
        check = db.check_username(username)
        if check is True:
            break
        print('That name is already taken. Try something else\n')

    frame = cam.video_capture()

    if frame is not None:
        encoding = recogn.face_handling(frame)
        if encoding is not None:
            db.add_user(username, encoding)

def login():
    frame = cam.video_capture()
    if frame is not None:
        username = recogn.face_compare(frame)
        if username:
            print(f'Login successful! Welcome, {username}')
        else:
            print('Face not recognized')

def exit_prog():
    print('Exiting the program...')
    exit()


def incorrect_input():
    print('Incorrect input. Try it (1 - 3)')


def menu():
    welcome_list = ['=' * 25, 'Select the mode:', '1 - Registration', '2 - Log in', '3 - Exit', '=' * 25]
    print(*welcome_list, sep='\n')


def main():
    db.create_db()

    funcs_menu = {'1': register, '2': login, '3': exit_prog}

    menu()

    while True:
        choice = input('Enter the mode number: ')

        funcs_menu.get(choice, incorrect_input)()

if __name__ == '__main__':
    main()
