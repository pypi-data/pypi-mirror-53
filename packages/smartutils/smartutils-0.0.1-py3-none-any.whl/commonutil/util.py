import time
import math

def get_exec_time(func):
    def wrapper(*args, **kwargs):
        t1 = time.time()
        func(*args, **kwargs)
        t2 = time.time()
        print("{}(Function) took {}".format(func.__name__, round(t2-t1, 4)))
    return wrapper