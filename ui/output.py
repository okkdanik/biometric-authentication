import datetime


colors = {
    'green': '\033[92m',
    'red': '\033[91m',
    'yellow': '\033[93m',
    'end': '\033[0m'
}


def print_main_menu():
    menu_items = [
        ' Select the mode ',
        '1 - Registration',
        '2 - Log in',
        '3 - Exit'
    ]

    max_content_length = max(len(item) for item in menu_items)
    border_length = max_content_length + 4
    color = colors['yellow']

    print(f"\n{color}{'=' * border_length}{colors['end']}")
    print(f"{color}|{colors['end']}"
          f"{color}{menu_items[0].center(max_content_length + 2)}{colors['end']}"
          f"{color}|{colors['end']}")
    print(f"{color}{'=' * border_length}{colors['end']}")

    for item in menu_items[1:]:
        print(f"{color}|{colors['end']} "
              f"{color}{item.ljust(max_content_length)}{colors['end']} "
              f"{color}|{colors['end']}")

    print(f"{color}q{'=' * border_length}{colors['end']}\n")

def print_login_success(username: str, confidence: float, elapsed_time: float):
    header = ' LOGIN SUCCESSFUL '
    welcome_msg = f' Welcome, {username}! '
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    stats = [
        f' Recognition time: {elapsed_time:.3f} seconds',
        f' Confidence level: {min(100.0, confidence * 100):.1f}%',
        f' Login time: {current_time}'
    ]

    max_length = max(len(header), len(welcome_msg), *[len(s) for s in stats])
    separator = '=' * (max_length + 4)

    color = colors['green']
    print(f"\n{color}{separator}{colors['end']}")
    print(f"{color}=={header.center(max_length)}=={colors['end']}")
    print(f"{color}=={welcome_msg.center(max_length)}=={colors['end']}")
    print(f"{color}{separator}{colors['end']}")
    for stat in stats:
        print(f"{color}| {stat.ljust(max_length + 1)}|{colors['end']}")
    print(f"{color}{separator}{colors['end']}\n")


def print_access_denied(elapsed_time: float, error_reason: str = None):
    error_header = ' ACCESS DENIED '
    reasons = [
        'Possible reasons:',
        '- Face not recognized',
        '- Low confidence level',
        '- System error'
    ]

    if error_reason:
        custom_reason = f"- {error_reason}"
        reasons.insert(1, custom_reason)

    max_length = max(len(error_header), *[len(r) for r in reasons])
    separator = '#' * (max_length + 4)

    color = colors['red']
    print(f"\n{color}{separator}{colors['end']}")
    print(f"{color}##{error_header.center(max_length)}##{colors['end']}")
    print(f"{color}{separator}{colors['end']}")
    for reason in reasons:
        print(f"{color}# {reason.ljust(max_length + 1)}#{colors['end']}")
    print(f"{color}{separator}{colors['end']}")
    print(f"{colors['yellow']}Processing time: {elapsed_time:.3f} seconds{colors['end']}\n")