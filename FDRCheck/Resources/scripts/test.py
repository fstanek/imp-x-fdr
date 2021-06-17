import sys
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

    log_info('This is a message.')
    sleep(3)

    log_error('This is an error.')


except Exception as e:
    log_error(e)
    sys.exit(1)