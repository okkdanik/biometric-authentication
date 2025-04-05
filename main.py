import detect.camera as cam
import detect.face_recogn as recogn
import database.redis_cli as redis
from ui.output import print_main_menu, print_login_success, print_access_denied
from logs.log_writer import log_successful_login


def register():
    while True:
        username = input('Enter your name: ')
        check = redis.check_username(username)
        if check is True:
            break
        print('That name is already taken. Try something else\n')

    frame = cam.video_capture()

    if frame is not None:
        encoding = recogn.face_handling(frame)
        if encoding is not None:
            redis.add_user(username, encoding)


def login():
    frame = cam.video_capture()
    if frame is not None:
        username, confidence, elapsed_time, error_reason = recogn.face_compare(frame)
        if username:
            print_login_success(username, confidence, elapsed_time)
            log_successful_login(username, elapsed_time, confidence)
            exit()
        else:
            print_access_denied(elapsed_time, error_reason)
            exit_prog()


def exit_prog():
    print('Exiting the program...')
    exit()


def incorrect_input():
    print('Incorrect input. Try it (1 - 3)')


def menu():
    print_main_menu()


def main():
    funcs_menu = {'1': register, '2': login, '3': exit_prog}
    menu()

    while True:
        choice = input('Enter the mode number: ')

        funcs_menu.get(choice, incorrect_input)()


if __name__ == '__main__':
    main()
