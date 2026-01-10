import sys
from datetime import datetime


original_write = sys.stdout.write


def my_write(string_text):
    timestamp = str(datetime.now())
    return original_write('[' + timestamp + ']' + ': ' + string_text)


sys.stdout.write = my_write

if sys.stdout.write is my_write:
    sys.stdout.write("TEST")
else:
    print('failed')

sys.stdout.write = original_write
