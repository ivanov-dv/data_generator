import os

from config import INPUT_DIR, OUTPUT_DIR, LOG_DIR
from engine import terminal


def main():
    # сделай списком
    if not os.path.exists(INPUT_DIR):
        os.mkdir(INPUT_DIR)
    if not os.path.exists(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)
    if not os.path.exists(LOG_DIR):
        os.mkdir(LOG_DIR)
    terminal.start()


if __name__ == '__main__':
    main()
