import random
import time
from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key):
        if key not in self.cache:
            return None
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key, value):
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)

    def invalidate_ranges(self, index):
        keys_to_remove = [key for key in self.cache if key[0] <= index <= key[1]]
        for key in keys_to_remove:
            del self.cache[key]

    def clear(self):
        self.cache.clear()

def update_no_cache(array, index, value):
    array[index] = value

def range_sum_with_cache(array, L, R, cache):
    key = (L, R)
    cached = cache.get(key)
    if cached is not None:
        return cached
    result = sum(array[L:R+1])
    cache.put(key, result)
    return result

def update_with_cache(array, index, value, cache):
    array[index] = value
    cache.invalidate_ranges(index)

N = 100_000
Q = 50_000
K = 1000

random.seed(42)
array = [random.randint(1, 1000) for _ in range(N)]

queries = []
for _ in range(Q):
    if random.random() < 0.7:
        L = random.randint(0, N-1)
        R = random.randint(L, N-1)
        queries.append(('Range', L, R))
    else:
        idx = random.randint(0, N-1)
        val = random.randint(1, 1000)
        queries.append(('Update', idx, val))

array_no_cache = list(array)
start = time.time()
for q in queries:
    if q[0] == 'Range':
        sum(array_no_cache[q[1]:1+q[2]])
    else:
        update_no_cache(array_no_cache, q[1], q[2])
no_cache_time = time.time() - start

array_with_cache = list(array)
lru_cache = LRUCache(K)
start = time.time()
for q in queries:
    if q[0] == 'Range':
        range_sum_with_cache(array_with_cache, q[1], q[2], lru_cache)
    else:
        update_with_cache(array_with_cache, q[1], q[2], lru_cache)
cache_time = time.time() - start

print(f"Час виконання без кешування: {no_cache_time:.2f} секунд")
print(f"Час виконання з LRU-кешем: {cache_time:.2f} секунд")