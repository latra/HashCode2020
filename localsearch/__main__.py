import sys

from .currentint import main

if __name__ == '__main__':
    if len(sys.argv) == 1:
        main()
    else:
        main(int(sys.argv[1]), sys.argv[2])