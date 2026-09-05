"""Extra built-in answers — common Python/general topics not in main ai_answers.py"""

EXTRA_ANSWERS = {
    # ── Basics ──────────────────────────────────────────────────
    ('what is python', 'python intro', 'about python', 'python kya hai'): """**Python — Introduction**
```python
# Python ek high-level, interpreted programming language hai
# Easy syntax, powerful features

# Hello World
print("Hello, World!")          # Output: Hello, World!

# Variables — no type declaration needed
name   = "QueryNest"            # string
age    = 20                     # integer
marks  = 92.5                   # float
active = True                   # boolean

# Multiple assignment
x, y, z = 10, 20, 30
print(x, y, z)                  # 10 20 30

# Type check
print(type(name))               # <class 'str'>
print(type(age))                # <class 'int'>
```
Python — simple, readable, aur beginner-friendly! 🐍""",

    ('hello world', 'first program', 'print hello'): """**Hello World — Python**
```python
# Basic output
print("Hello, World!")          # Hello, World!

# With variable
message = "Hello, QueryNest!"
print(message)                  # Hello, QueryNest!

# f-string
name = "Student"
print(f"Hello, {name}! Welcome to Python 🐍")
# Hello, Student! Welcome to Python 🐍

# Multiple values
print("Name:", name, "| Age:", 20)
```""",

    ('if else', 'if elif', 'conditional', 'condition'): """**If-Else — Python**
```python
marks = 75

# Basic if-else
if marks >= 90:
    grade = "A+"
elif marks >= 80:
    grade = "A"
elif marks >= 70:
    grade = "B"
elif marks >= 60:
    grade = "C"
else:
    grade = "F"

print(f"Marks: {marks} → Grade: {grade}")   # Marks: 75 → Grade: B

# One-liner (ternary)
status = "Pass" if marks >= 33 else "Fail"
print("Status:", status)         # Pass

# Nested if
age = 20
has_id = True
if age >= 18:
    if has_id:
        print("Entry allowed ✅")
    else:
        print("Need ID card ❌")
else:
    print("Too young ❌")
```""",

    ('list', 'list in python', 'python list', 'lists'): """**Lists — Python**
```python
# Create list
fruits = ["apple", "banana", "cherry", "date"]
nums   = [10, 20, 30, 40, 50]
mixed  = [1, "hello", 3.14, True]       # any type

# Access
print(fruits[0])                # apple  (first)
print(fruits[-1])               # date   (last)
print(fruits[1:3])              # ['banana', 'cherry'] (slice)

# Modify
fruits.append("mango")          # add at end
fruits.insert(1, "kiwi")        # add at index 1
fruits.remove("banana")         # remove by value
popped = fruits.pop()           # remove last → returns it

# Useful methods
nums.sort()                     # sort ascending
nums.reverse()                  # reverse list
print(len(nums))                # 5 — length
print(sum(nums))                # 150 — total
print(max(nums), min(nums))     # 50  10

# List comprehension
squares = [x**2 for x in range(1, 6)]
print(squares)                  # [1, 4, 9, 16, 25]
```""",

    ('function', 'functions', 'def', 'python function', 'function in python'): """**Functions — Python**
```python
# Basic function
def greet(name):
    return f"Hello, {name}! 👋"

print(greet("Alice"))           # Hello, Alice! 👋

# Default parameter
def power(base, exp=2):         # exp ka default = 2
    return base ** exp

print(power(3))                 # 9   (3²)
print(power(2, 10))             # 1024 (2¹⁰)

# Multiple return values
def min_max(lst):
    return min(lst), max(lst)   # tuple return karta hai

lo, hi = min_max([4, 1, 9, 2, 7])
print(f"Min={lo}, Max={hi}")    # Min=1, Max=9

# *args — variable arguments
def total(*nums):
    return sum(nums)

print(total(1, 2, 3, 4, 5))    # 15

# Lambda (anonymous function)
square = lambda x: x * x
print(square(5))                # 25
```""",

    ('print', 'how to print', 'print function', 'output'): """**Print Function — Python**
```python
# Basic print
print("Hello!")                 # Hello!

# Multiple values
print("Name:", "Alice", "Age:", 20)     # Name: Alice Age: 20

# Separator
print("2024", "01", "15", sep="-")     # 2024-01-15

# End character (default is newline)
print("Loading", end="...")     # Loading...
print(" Done!")                 # Done!

# f-string (best way)
name, marks = "Alice", 92.5
print(f"Student: {name}, Marks: {marks:.1f}")  # Alice, Marks: 92.5

# Format numbers
pi = 3.14159265
print(f"Pi = {pi:.2f}")        # Pi = 3.14
print(f"Pi = {pi:10.4f}")      # Pi =     3.1416 (width=10)

# Print list nicely
data = [1, 2, 3, 4, 5]
print(*data)                    # 1 2 3 4 5  (unpacked)
print(*data, sep=", ")          # 1, 2, 3, 4, 5
```""",

    ('variable', 'variables', 'what is variable', 'variable in python'): """**Variables — Python**
```python
# Variable declare karo — type likhna zaroori nahi
name   = "Alice"                # str
age    = 20                     # int
marks  = 92.5                   # float
passed = True                   # bool

# Multiple assignment
x = y = z = 0                  # all = 0
a, b, c = 10, 20, 30           # unpack

# Type check & conversion
print(type(name))               # <class 'str'>
age_str = str(age)              # int → str
num     = int("123")            # str → int
flt     = float("3.14")        # str → float

# Swap variables
a, b = 10, 20
a, b = b, a                     # pythonic swap
print(a, b)                     # 20 10

# Constants (convention: UPPERCASE)
MAX_SIZE = 100
PI       = 3.14159

# Delete variable
temp = 42
del temp                        # memory free
```""",

    ('data types', 'data type', 'types in python', 'int float str bool'): """**Data Types — Python**
```python
# 1. Numeric
i = 42                          # int
f = 3.14                        # float
c = 2 + 3j                      # complex

# 2. String
s = "Hello"
s2 = 'World'
ml = \"\"\"Multi
line string\"\"\"

# 3. Boolean
t, fa = True, False
print(True + True)              # 2 (True = 1)

# 4. List — mutable, ordered
lst = [1, 2, 3]
lst[0] = 99                     # can change ✅

# 5. Tuple — immutable, ordered
tpl = (1, 2, 3)
# tpl[0] = 99  ← ERROR ❌

# 6. Set — unordered, unique
st = {1, 2, 2, 3, 3}
print(st)                       # {1, 2, 3}

# 7. Dictionary — key:value
d = {"name": "Alice", "age": 20}
print(d["name"])                # Alice

# Type check
for val in [42, 3.14, "hi", True, [1,2], (1,), {1}, {"k":"v"}]:
    print(type(val).__name__, "→", val)
```""",

    ('tuple', 'tuples', 'tuple in python'): """**Tuples — Python**
```python
# Create tuple — immutable (change nahi hoti)
coords  = (10, 20)
colors  = ("red", "green", "blue")
single  = (42,)                 # single item — comma zaroori!
empty   = ()

# Access
print(colors[0])                # red
print(colors[-1])               # blue
print(colors[1:])               # ('green', 'blue')

# Unpack
x, y = coords
print(f"x={x}, y={y}")         # x=10, y=20

r, g, b = colors
print(r, g, b)                  # red green blue

# Tuple vs List
lst = [1, 2, 3]
lst[0] = 99                     # OK — list mutable hai
tpl = (1, 2, 3)
# tpl[0] = 99  ← TypeError!    # tuple immutable hai

# Useful when
point    = (3, 4)               # coordinates
rgb      = (255, 128, 0)        # color value
db_row   = ("Alice", 20, 92.5) # database record

# Methods
print(colors.count("red"))      # 1
print(colors.index("green"))    # 1
print(len(colors))              # 3
```""",

    ('set', 'sets', 'set in python', 'set operations'): """**Sets — Python**
```python
# Set — unordered, unique elements
fruits = {"apple", "banana", "cherry", "apple"}  # duplicate remove!
print(fruits)                   # {'banana', 'cherry', 'apple'}

nums = {1, 2, 3, 4, 5}

# Add / Remove
fruits.add("mango")             # add element
fruits.discard("banana")        # remove (no error if missing)
fruits.remove("cherry")         # remove (error if missing)

# Set operations (like math)
A = {1, 2, 3, 4}
B = {3, 4, 5, 6}

print(A | B)                    # Union:        {1,2,3,4,5,6}
print(A & B)                    # Intersection: {3,4}
print(A - B)                    # Difference:   {1,2}
print(A ^ B)                    # Symmetric:    {1,2,5,6}

# Check membership — O(1) — very fast!
print("apple" in fruits)        # True
print(3 in A)                   # True

# Remove duplicates from list
lst = [1, 2, 2, 3, 3, 3, 4]
unique = list(set(lst))
print(unique)                   # [1, 2, 3, 4]
```""",

    ('lambda', 'lambda function', 'anonymous function'): """**Lambda Functions — Python**
```python
# Lambda — ek line ka anonymous function
square  = lambda x: x * x
add     = lambda a, b: a + b
greet   = lambda name: f"Hello, {name}!"

print(square(5))                # 25
print(add(3, 4))                # 7
print(greet("Alice"))           # Hello, Alice!

# Lambda with built-in functions
nums   = [3, 1, 4, 1, 5, 9, 2, 6]
words  = ["banana", "apple", "cherry", "date"]
people = [("Alice", 92), ("Bob", 78), ("Charlie", 85)]

print(sorted(nums))                          # [1,1,2,3,4,5,6,9]
print(sorted(words, key=lambda w: len(w)))   # sort by length
print(sorted(people, key=lambda p: p[1], reverse=True))  # sort by marks desc

# map — apply to all
squared = list(map(lambda x: x**2, [1,2,3,4,5]))
print(squared)                  # [1, 4, 9, 16, 25]

# filter — keep matching
evens   = list(filter(lambda x: x%2==0, range(1,11)))
print(evens)                    # [2, 4, 6, 8, 10]
```""",

    ('slice', 'slicing', 'list slicing', 'string slicing'): """**Slicing — Python**
```python
# Slice syntax: lst[start:stop:step]
lst = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

print(lst[2:6])                 # [2, 3, 4, 5]
print(lst[:4])                  # [0, 1, 2, 3]     — start se
print(lst[6:])                  # [6, 7, 8, 9]     — end tak
print(lst[::2])                 # [0, 2, 4, 6, 8]  — step=2
print(lst[::-1])                # [9,8,7,6,5,4,3,2,1,0] — reverse!
print(lst[1:8:2])               # [1, 3, 5, 7]

# String slicing (same rules)
s = "QueryNest"
print(s[0:5])                   # Query
print(s[5:])                    # Nest
print(s[::-1])                  # tseNyreuQ  — reverse!
print(s[::2])                   # ueyNs

# Negative indices
print(lst[-3:])                 # [7, 8, 9]  — last 3
print(lst[-5:-2])               # [5, 6, 7]
```""",

    ('enumerate', 'enumerate function'): """**Enumerate — Python**
```python
fruits = ["apple", "banana", "cherry", "date"]

# Without enumerate — manual index
for i in range(len(fruits)):
    print(i, fruits[i])

# With enumerate — clean & pythonic ✅
for i, fruit in enumerate(fruits):
    print(f"{i}: {fruit}")
# 0: apple
# 1: banana
# 2: cherry
# 3: date

# Custom start index
for i, fruit in enumerate(fruits, start=1):
    print(f"{i}. {fruit}")
# 1. apple  2. banana  3. cherry  4. date

# Use case — add serial numbers
students = ["Alice", "Bob", "Charlie"]
numbered = {i: name for i, name in enumerate(students, 1)}
print(numbered)         # {1: 'Alice', 2: 'Bob', 3: 'Charlie'}
```""",

    ('zip', 'zip function', 'zip in python'): """**Zip Function — Python**
```python
names  = ["Alice", "Bob",   "Charlie"]
marks  = [92,      78,      85]
grades = ["A+",    "B",     "A"]

# zip — parallel lists ko combine karo
for name, mark, grade in zip(names, marks, grades):
    print(f"{name}: {mark} ({grade})")
# Alice: 92 (A+)
# Bob: 78 (B)
# Charlie: 85 (A)

# Create dictionary from two lists
mapping = dict(zip(names, marks))
print(mapping)          # {'Alice': 92, 'Bob': 78, 'Charlie': 85}

# Unzip — inverse of zip
pairs = [(1, 'a'), (2, 'b'), (3, 'c')]
nums, letters = zip(*pairs)
print(nums)             # (1, 2, 3)
print(letters)          # ('a', 'b', 'c')

# zip_longest — missing values fill karo
from itertools import zip_longest
a = [1, 2, 3]
b = ["x", "y"]
for pair in zip_longest(a, b, fillvalue=0):
    print(pair)         # (1,'x') (2,'y') (3,0)
```""",

    ('map filter reduce', 'map function', 'filter function', 'reduce'): """**Map, Filter, Reduce — Python**
```python
from functools import reduce

nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# map — every element pe function apply karo
squares = list(map(lambda x: x**2, nums))
print("Squares:", squares)      # [1,4,9,16,25,36,49,64,81,100]

doubled = list(map(lambda x: x*2, nums))
print("Doubled:", doubled)      # [2,4,6,8,10,12,14,16,18,20]

# filter — condition match karne wale rakhho
evens   = list(filter(lambda x: x%2==0, nums))
print("Evens:",   evens)        # [2, 4, 6, 8, 10]

big     = list(filter(lambda x: x>5, nums))
print("Big (>5):", big)         # [6, 7, 8, 9, 10]

# reduce — accumulate into single value
total   = reduce(lambda a, b: a+b, nums)
product = reduce(lambda a, b: a*b, [1,2,3,4,5])
maximum = reduce(lambda a, b: a if a>b else b, nums)

print("Sum:",     total)        # 55
print("Product:", product)      # 120
print("Max:",     maximum)      # 10
```""",

    ('generator', 'generators', 'yield', 'generator function'): """**Generators — Python**
```python
# Generator — lazy evaluation, memory efficient

# Generator function — yield use karta hai
def count_up(n):
    for i in range(1, n+1):
        yield i                 # ek value deta hai, pause karta hai

gen = count_up(5)
print(next(gen))                # 1
print(next(gen))                # 2
for val in gen:
    print(val)                  # 3, 4, 5

# Generator expression (like list comp but lazy)
sq_gen = (x**2 for x in range(1, 6))   # no brackets = generator
print(list(sq_gen))             # [1, 4, 9, 16, 25]

# Fibonacci generator — infinite sequence!
def fib_gen():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a+b

fib = fib_gen()
print([next(fib) for _ in range(10)])   # [0,1,1,2,3,5,8,13,21,34]

# Memory advantage
import sys
lst = [x**2 for x in range(1000)]      # list — stores ALL
gen = (x**2 for x in range(1000))      # generator — one at a time
print("List:", sys.getsizeof(lst))      # ~8700 bytes
print("Gen: ", sys.getsizeof(gen))      # ~112 bytes ✅
```""",

    ('decorator', 'decorators', 'python decorator'): """**Decorators — Python**
```python
import time

# Decorator — function ko wrap karna
def timer(func):
    def wrapper(*args, **kwargs):
        start  = time.time()
        result = func(*args, **kwargs)         # original function call
        end    = time.time()
        print(f"⏱ {func.__name__} took {end-start:.4f}s")
        return result
    return wrapper

@timer                          # = greet = timer(greet)
def greet(name):
    return f"Hello, {name}!"

print(greet("Alice"))           # Hello, Alice! + time

# Logger decorator
def logger(func):
    def wrapper(*args, **kwargs):
        print(f"▶ Calling {func.__name__}({args}, {kwargs})")
        result = func(*args, **kwargs)
        print(f"◀ {func.__name__} returned {result}")
        return result
    return wrapper

@logger
def add(a, b):
    return a + b

add(3, 5)
# ▶ Calling add((3, 5), {})
# ◀ add returned 8

# Built-in decorators
class MyClass:
    count = 0

    @classmethod
    def get_count(cls):         # class method
        return cls.count

    @staticmethod
    def utility():              # no self/cls needed
        return "utility function"
```""",

    ('comprehension', 'list comprehension', 'dict comprehension', 'set comprehension'): """**Comprehensions — Python**
```python
nums = range(1, 11)

# List comprehension
squares  = [x**2       for x in nums]
evens    = [x          for x in nums if x%2==0]
filtered = [x**2       for x in nums if x%2==0]    # filter + transform

print(squares)   # [1,4,9,16,25,36,49,64,81,100]
print(evens)     # [2,4,6,8,10]
print(filtered)  # [4,16,36,64,100]

# Dictionary comprehension
sq_dict  = {x: x**2 for x in range(1,6)}
even_d   = {x: x**2 for x in range(1,11) if x%2==0}
print(sq_dict)   # {1:1, 2:4, 3:9, 4:16, 5:25}

# Set comprehension (unique values)
chars    = {c.lower() for c in "Hello World" if c != ' '}
print(chars)     # {'h','e','l','o','w','r','d'}

# Nested comprehension — matrix
matrix   = [[i*j for j in range(1,4)] for i in range(1,4)]
print(matrix)    # [[1,2,3],[2,4,6],[3,6,9]]

# Flatten nested list
nested   = [[1,2],[3,4],[5,6]]
flat     = [x for row in nested for x in row]
print(flat)      # [1,2,3,4,5,6]
```""",

    ('static method', 'classmethod', 'class method'): """**Static & Class Methods — Python**
```python
class MathHelper:
    pi = 3.14159                # class variable

    def __init__(self, value):
        self.value = value      # instance variable

    def double(self):           # instance method — needs self
        return self.value * 2

    @classmethod
    def from_string(cls, s):    # class method — gets class itself
        return cls(int(s))      # alternative constructor

    @staticmethod
    def add(a, b):              # static method — no self/cls
        return a + b            # just a regular utility function

    @staticmethod
    def is_prime(n):
        if n < 2: return False
        for i in range(2, int(n**0.5)+1):
            if n%i==0: return False
        return True


# Instance method
m = MathHelper(10)
print(m.double())               # 20

# Class method — create from string
m2 = MathHelper.from_string("42")
print(m2.value)                 # 42

# Static method — called on class directly (no instance needed)
print(MathHelper.add(5, 3))     # 8
print(MathHelper.is_prime(17))  # True
print(MathHelper.pi)            # 3.14159
```""",

    ('numpy', 'numpy array', 'np array', 'import numpy'): """**NumPy Basics — Python**
```python
import numpy as np

# Array create karo
a = np.array([1, 2, 3, 4, 5])
b = np.array([10, 20, 30, 40, 50])

print(a + b)        # [11 22 33 44 55]  — element-wise
print(a * 2)        # [ 2  4  6  8 10]  — broadcast
print(a ** 2)       # [ 1  4  9 16 25]  — power

# Shape & info
print(a.shape)      # (5,)
print(a.dtype)      # int64

# 2D array (matrix)
matrix = np.array([[1,2,3],[4,5,6],[7,8,9]])
print(matrix.shape)         # (3, 3)
print(matrix[1][2])         # 6 — row 1, col 2
print(matrix[:, 1])         # [2 5 8] — column 1

# Useful functions
print(np.zeros((3,3)))      # 3x3 zeros
print(np.ones((2,4)))       # 2x4 ones
print(np.arange(0,10,2))    # [0 2 4 6 8]
print(np.linspace(0,1,5))   # [0. .25 .5 .75 1.]

# Stats
data = np.array([4,7,2,9,1,5,8,3,6])
print("Mean:", np.mean(data))       # 5.0
print("Std:",  np.std(data))        # 2.58
print("Max:",  np.max(data))        # 9
print("Sort:", np.sort(data))       # [1 2 3 4 5 6 7 8 9]
```""",
}


def lookup_extra(query: str, lang: str = 'python') -> str | None:
    """Look up extra built-in answers. Returns answer string or None."""
    q = query.lower().strip()
    for keywords, answer in EXTRA_ANSWERS.items():
        if any(kw in q for kw in keywords):
            return answer
    return None
