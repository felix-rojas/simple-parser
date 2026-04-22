from Lexer import *
from Parser import *
import sys

if __name__ == '__main__':
    parser = Parser("test_cases/good/input01.txt")
    parser.analize()