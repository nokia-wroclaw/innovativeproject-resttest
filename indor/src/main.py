import sys
from src import read_from_file

__author__ = 'slawomir'

args = sys.argv

if len(args) != 2:
    print("Usage: python main.py file.ind")
    sys.exit()

read_from_file(args[1])