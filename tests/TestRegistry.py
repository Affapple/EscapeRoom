import os
import sys
from typing import Callable

tests: dict[str, list[Callable[[], bool]]] = {}


def Test(function: Callable[[], bool]):
    def redirect_stdout():
        f = open(os.devnull, 'w')
        sys.stdout = f
        sys.stderr = f
        return f

    def restore_stdout(f):
        f.close()
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__

    def wrapper():
        print(f"Running test: {function.__name__}", end="")

        f = redirect_stdout() # Redirect stdout to suppress output during test execution
        result = function()
        restore_stdout(f)  # Restore original stdout

        green = "\033[92m"
        red = "\033[91m"
        bold = "\033[1m"
        endc = "\033[0m"

        resultStr = (green + "Passed") if result else (red + "Failed")
        print(" | " + bold + resultStr + endc)
        return result

    if function.__module__ not in tests:
        tests[function.__module__] = []

    tests[function.__module__].append(wrapper)
    return wrapper
