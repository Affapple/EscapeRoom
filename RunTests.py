import importlib
import os

from tests.TestRegistry import tests


def discover_tests():
    """Dynamically discover and import all test modules in the tests/ directory."""
    test_files: int = 0
    for file in os.listdir("./tests"):
        if file.startswith("test_") and file.endswith(".py"):
            file_name: str = file[:-3]
            importlib.import_module("tests." + file_name)
            test_files += 1
    print(f"Discovered {len(tests)} tests on {test_files} test files.")


if __name__ == "__main__":
    discover_tests()

    for module_name, test_functions in tests.items():
        print("Running tests from module:", module_name)
        for test_func in test_functions:
            test_func()
        print()
