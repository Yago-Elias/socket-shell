ERROR = 1
DEBUG = 2
WARNING = 3
INFO = 4

COL_ERROR = '\033[0;31m [ ERROR ] \033[m'
COL_DEBUG = '\033[32m [ DEBUG ] \033[m'
COL_WARNING = '\033[0;33m [ WARNING ] \033[m '
COL_INFO = '\033[0;34m [ INFO ] \033[m'


def log(message_log: str, level: int = INFO) -> None:
    if level == ERROR:
        print(f'{COL_ERROR}', end='')
    elif level == DEBUG:
        print(f'{COL_DEBUG} ', end='')
    elif level == WARNING:
        print(f'{COL_WARNING}', end='')
    elif level == INFO:
        print(f'{COL_INFO}', end='')

    print(message_log)


__all__ = [
    # funções
    'log',

    # constantes
    ERROR,
    DEBUG,
    WARNING,
    INFO,
]
