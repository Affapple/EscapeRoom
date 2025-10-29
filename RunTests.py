import importlib
import os

from tests.TestRegistry import tests


def discover_tests():
    test_files = 0
    for file in os.listdir("./tests"):
        if file.startswith("test_") and file.endswith(".py"):
            module_name = file[:-3]
            importlib.import_module("tests." + module_name)
            test_files += 1
    print(f"Discovered {len(tests)} tests on {test_files} test files.")


if __name__ == "__main__":
    discover_tests()

    for module in tests.keys():
        print("Running tests from module:", module)
        for test_func in tests[module]:
            test_func()
        print()
