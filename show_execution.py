import time


def show_execution(desc: str = "function", func=None, *args, **kwargs):
    if func is None:
        return
    print(f'{desc}: ', end='')
    start = time.time()
    res = func(*args, **kwargs)
    end = time.time()
    print(f'complete. in {end - start:.3f} seconds.')
    return res



