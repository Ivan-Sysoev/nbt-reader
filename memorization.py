import time

def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        ret = func(*args, **kwargs)
        end_time = time.time()
        print(f'Function {func.__name__} executed in {round(end_time - start_time, 2)} sec.')
        return ret
    return wrapper

# def memorization(func):
#     def wrapper(*args, **kwargs):
#         if args in memory_calls:
#             return memory_calls[args]
#         ret = func(*args, **kwargs)
#         memory_calls[args] = ret
#         return ret
#     return wrapper

class Memorization:
    def __init__(self, func):
        self._memory_calls = {}
        self._func = func
    
    def __call__(self, *args, **kwargs):
        if args in self._memory_calls:
            return self._memory_calls[args]

        ret = self._func(*args, **kwargs)
        self._memory_calls[args] = ret
        return ret

@Memorization
def foo(name, **kwargs):
    time.sleep(0.5)
    return kwargs.values()

@timer
def main():
    foo('ivans')
    foo('ivans')
    foo('nigga')
    foo('nigga')
    foo('nigga')
    foo('nigga')
    foo('nigga')
    foo('nigga')

if __name__ == "__main__":
    main()
