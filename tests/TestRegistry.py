from typing import Callable

tests: dict[str, list[Callable[[], bool]]] = {}


def Test(function: Callable[[], bool]):
    def wrapper():
        print(f"Running test: {function.__name__}", end="")
        result = function()

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
