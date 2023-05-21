import random
import time
from functools import wraps


def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f"Function {func.__name__} Took {total_time:.4f} seconds")
        return result

    return timeit_wrapper


def get_random_list(list_length=200000, min_value=0, max_value=1000000000):
    randomlist = []
    for i in range(0, list_length):
        n = random.randint(min_value, max_value)
        randomlist.append(n)

    return randomlist
