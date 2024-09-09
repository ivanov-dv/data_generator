import os

from config import DIR_NAMES
from engine import terminal


def main():
    for dir_name in DIR_NAMES:
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
    terminal.start()


if __name__ == '__main__':
    main()
