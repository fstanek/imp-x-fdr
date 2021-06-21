#Test
import sys, os
from time import sleep

def log_info(text):
    print(text)
    sys.stdout.flush()

def log_error(text):
    print(text, file=sys.stderr)
    sys.stderr.flush()

try:
    input_filename = sys.argv[1]
    library_filename = sys.argv[2]
    output_filename = sys.argv[3]

    #log_info(os.environ['PYTHONHOME'])
    log_info('prefix')
    log_info(sys.prefix)
    log_info('exec_prefix')
    log_info(sys.exec_prefix)

    #sys.path.insert(0, r'C:\Users\stanek\source\repos\FDRCheck\FDRCheck\Resources\python\lib\site-packages')
    log_info(sys.path)

    import numpy
    import xlsxwriter

    log_info('This is a message.')
    sleep(3)

    log_error('This is an error.')

except Exception as e:
    log_error(e)
    sys.exit(1)