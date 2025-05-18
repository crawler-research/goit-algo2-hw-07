import timeit
from functools import lru_cache
import matplotlib.pyplot as plt

class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None

class SplayTree:
    def __init__(self):
        self.root = None

    def _right_rotate(self, x):
        y = x.left
        x.left = y.right
        y.right = x
        return y

    def _left_rotate(self, x):
        y = x.right
        x.right = y.left
        y.left = x
        return y

    def _splay(self, root, key):
        if root is None or root.key == key:
            return root

        if key < root.key:
            if root.left is None:
                return root
            if key < root.left.key:
                root.left.left = self._splay(root.left.left, key)
                root = self._right_rotate(root)
            elif key > root.left.key:
                root.left.right = self._splay(root.left.right, key)
                if root.left.right:
                    root.left = self._left_rotate(root.left)
            return root if root.left is None else self._right_rotate(root)
        else:
            if root.right is None:
                return root
            if key > root.right.key:
                root.right.right = self._splay(root.right.right, key)
                root = self._left_rotate(root)
            elif key < root.right.key:
                root.right.left = self._splay(root.right.left, key)
                if root.right.left:
                    root.right = self._right_rotate(root.right)
            return root if root.right is None else self._left_rotate(root)

    def insert(self, key, value):
        if self.root is None:
            self.root = Node(key, value)
            return
        self.root = self._splay(self.root, key)
        if self.root.key == key:
            self.root.value = value
            return
        new_node = Node(key, value)
        if key < self.root.key:
            new_node.right = self.root
            new_node.left = self.root.left
            self.root.left = None
        else:
            new_node.left = self.root
            new_node.right = self.root.right
            self.root.right = None
        self.root = new_node

    def search(self, key):
        self.root = self._splay(self.root, key)
        if self.root and self.root.key == key:
            return self.root.value
        return None

@lru_cache(maxsize=None)
def fibonacci_lru(n):
    if n < 2:
        return n
    return fibonacci_lru(n-1) + fibonacci_lru(n-2)

def fibonacci_splay(n, tree):
    cached = tree.search(n)
    if cached is not None:
        return cached
    if n < 2:
        tree.insert(n, n)
        return n
    value = fibonacci_splay(n-1, tree) + fibonacci_splay(n-2, tree)
    tree.insert(n, value)
    return value

n_values = list(range(0, 1000, 50))
lru_times = []
splay_times = []

for n in n_values:
    # LRU Cache
    stmt_lru = f"fibonacci_lru({n})"
    setup_lru = (
        "from __main__ import fibonacci_lru"
    )
    lru_time = timeit.timeit(stmt=stmt_lru, setup=setup_lru, number=5) / 5
    lru_times.append(lru_time)

    def run_splay():
        tree = SplayTree()
        return fibonacci_splay(n, tree)
    splay_time = timeit.timeit(run_splay, number=5) / 5
    splay_times.append(splay_time)

print(f"{'n':<10}{'LRU Cache Time (s)':<22}{'Splay Tree Time (s)':<22}")
print("-" * 54)
for n, lru, splay in zip(n_values, lru_times, splay_times):
    print(f"{n}{lru}{splay}")

plt.figure(figsize=(10, 6))
plt.plot(n_values, lru_times, label='LRU Cache')
plt.plot(n_values, splay_times,  label='Splay Tree')
plt.title('lru vs splay tree')
plt.ylabel("секунди)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
