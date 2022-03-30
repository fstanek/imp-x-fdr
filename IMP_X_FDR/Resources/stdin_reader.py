from os import sep
from sys import stdin

def read(separator = '\t'):
    #headers = stdin.readline().strip().split(separator)
    items = []

    for line in stdin:
        yield line.strip().split(separator)
        yield data