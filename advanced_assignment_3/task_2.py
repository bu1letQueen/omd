import sys
from datetime import datetime


def timed_output(function):
    def wrapper(*args, **kwargs):
        original_write = sys.stdout.write

        def my_write(string_text):
            time = str(datetime.now())
            if string_text == "\n":
                return original_write(string_text)
            return original_write('[' + time + ']' + ': ' + string_text)

        sys.stdout.write = my_write

        try:
            function(*args, **kwargs)
        finally:
            sys.stdout.write = original_write

    return wrapper


@timed_output
def print_greeting(name):
    print(f'Hello, {name}!')

print_greeting("Nikita")
