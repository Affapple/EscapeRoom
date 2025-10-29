tests: list = []

def Test(function):
    def wrapper():
        print(f"Running test: {function.__name__}", end="")
        result = function()
        print(f" | {'Passed' if result else 'Failed'}")
        return result
    tests.append(wrapper)
    return wrapper