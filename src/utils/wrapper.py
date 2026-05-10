import time


def execution_time_wrapper(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print({f"Время выполнения функции {func.__name__}: {execution_time:.8f}"})
        return result
    return wrapper

