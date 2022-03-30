import sys

def read_crosslinks():
    for line in sys.stdin:
        values = line.strip().split('\t')
        values[2] = float(values[2])    # score
        values[5] = int(values[5])      # position 1
        values[6] = int(values[6])      # position 2
        yield values

def read_library():
    pass

if __name__ == '__main__':
    print('Reading crosslinks from stdin...')
    crosslinks = list(read_crosslinks())
    print('{} crosslinks read.'.format(len(crosslinks)))