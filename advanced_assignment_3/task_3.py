import sys


def redirect_output(filepath):
    def redirector(function):
        def wrapper(*args, **kwargs):
            original_stdout = sys.stdout
            file = open(filepath, 'w', encoding='utf-8')
            sys.stdout = file

            try:
                return function(*args, **kwargs)
            finally:
                file.close()
                sys.stdout = original_stdout

        return wrapper
    return redirector


@redirect_output('./function_output.txt')
def calculate():
    for power in range(1, 5):
        for num in range(1, 20):
            print(num ** power, end=' ')
        print()

calculate()