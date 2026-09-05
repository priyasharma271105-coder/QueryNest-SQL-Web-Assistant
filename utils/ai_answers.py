"""QueryNest — Built-in code answer generator. No API key needed."""
import re as _re
try:
    from utils.ai_answers_extra import lookup_extra as _lookup_extra
except ImportError:
    _lookup_extra = None

def generate_smart_answer(query, lang=None):
    """Generate proper working code for ANY query — 50+ topics, all 7 languages."""
    import re as _re
    q = query.lower().strip()
    L = lang or 'python'

    def has(*kws):
        return any(k in q for k in kws)

    # ══════════════════════════════════════════════════════════════
    # PYTHON
    # ══════════════════════════════════════════════════════════════
    if L == 'python':

        if has('whole number','whole numbers','natural number','natural numbers',
                'print natural','print whole','1 to n','1 to 100','1 to 50',
                'positive number','positive integer','counting number'):
            m = _re.search(r'(?:till|upto|up to|1 to|to)\s*(\d+)', q)
            limit = int(m.group(1)) if m else 10
            return f"""**Natural / Whole Numbers (1 to {limit}) — Python**
```python
n = {limit}                          # tak print karna hai

# Method 1 — for loop
print("Natural numbers:", end=" ")
for i in range(1, n + 1):           # 1 se n tak
    print(i, end=" ")
# Output: 1 2 3 4 5 ... {limit}

# Method 2 — list
nums = list(range(1, n + 1))        # [1, 2, 3, ..., {limit}]
print("\\nList:", nums)

# Sum formula
total = n * (n + 1) // 2            # n*(n+1)/2
print("Sum 1 to {limit}:", total)   # {limit*(limit+1)//2}
```"""

        if has('digit','digits','count digit','sum of digit','digit sum',
                'reverse digit','reverse number'):
            return """**Digit Operations — Python**
```python
n = 12345

# Count digits
count = len(str(n))                  # digits ki sankhya
print("Digits:", count)             # 5

# Sum of digits
digit_sum = sum(int(d) for d in str(n))
print("Digit sum:", digit_sum)      # 15

# Reverse number
rev = int(str(n)[::-1])             # string reverse trick
print("Reversed:", rev)             # 54321

# Check palindrome number
print("Palindrome:", n == rev)      # False (12345 ≠ 54321)
```"""

        if has('vowel','vowels','count vowel','count vowels','vowels in string','vowels in','consonant'):
            return """**Count Vowels & Consonants — Python**
```python
s = "Hello QueryNest"         # input string
vowels = "aeiouAEIOU"         # sabhi vowels

v_count = sum(1 for c in s if c in vowels)                      # vowels count
c_count = sum(1 for c in s if c.isalpha() and c not in vowels)  # consonants

print(f"String: '{s}'")
print(f"Vowels:     {v_count}")     # 5
print(f"Consonants: {c_count}")     # 9
```"""


        if has('even number','even numbers','print even','even upto','even till'):
            m = _re.search(r'(?:till|upto|up to|<=?|to)\s*(\d+)', q)
            limit = int(m.group(1)) if m else 50
            last_even = limit if limit % 2 == 0 else limit - 1
            return f"""**Even Numbers Till {limit} — Python**
```python
n = {limit}                         # tak print karna hai
for i in range(2, n+1, 2):          # 2 se shuru, step=2
    print(i, end=' ')               # even number print karo
# Output: 2 4 6 8 ... {last_even}
```"""

        if has('odd number','odd numbers','print odd','odd upto','odd till'):
            m = _re.search(r'(?:till|upto|up to|<=?|to)\s*(\d+)', q)
            limit = int(m.group(1)) if m else 50
            last_odd = limit if limit % 2 != 0 else limit - 1
            return f"""**Odd Numbers Till {limit} — Python**
```python
n = {limit}
for i in range(1, n+1, 2):          # 1 se shuru, step=2
    print(i, end=' ')               # odd number print karo
# Output: 1 3 5 7 9 ... {last_odd}
```"""

        if has('armstrong'):
            return """**Armstrong Number — Python**
```python
# Armstrong: digits^n ka sum == number (e.g. 153 = 1³+5³+3³)
def is_armstrong(n):
    digits = str(n)
    power  = len(digits)                        # kitne digits hain
    return sum(int(d)**power for d in digits) == n

print("Armstrong numbers (1–500):")
print([n for n in range(1, 501) if is_armstrong(n)])
# Output: [1, 2, 3, 4, 5, 6, 7, 8, 9, 153, 370, 371, 407]
```"""

        if has('swap','exchange two','interchange two'):
            return """**Swap Two Numbers — Python**
```python
a, b = 10, 20
print(f"Before: a={a}, b={b}")

# Method 1 — third variable
temp = a;  a = b;  b = temp
print(f"After (temp): a={a}, b={b}")   # a=20, b=10

# Method 2 — Python one-liner
x, y = 5, 15
x, y = y, x
print(f"After (one-liner): x={x}, y={y}")  # x=15, y=5
```"""

        if has('fibonacci','fibo series','fib series'):
            return """**Fibonacci Series — Python**
```python
n = 10                          # kitne terms chahiye
a, b = 0, 1
print(f"Fibonacci ({n} terms):", end=' ')
for _ in range(n):
    print(a, end=' ')           # current term print
    a, b = b, a + b             # next term calculate
# Output: 0 1 1 2 3 5 8 13 21 34
```"""

        if has('factorial'):
            return """**Factorial — Python**
```python
def factorial(n):
    if n <= 1: return 1          # base case
    return n * factorial(n-1)   # recursive call

for i in range(1, 8):
    print(f"{i}! = {factorial(i)}")
# Output: 1!=1, 2!=2, 3!=6, 4!=24, 5!=120, 6!=720, 7!=5040
```"""

        # ── "prime numbers till N" — specific N extract karke dynamic code do ──
        if has('prime numbers till','prime till','primes till','prime upto','primes upto',
               'prime up to','primes up to','print prime till','print primes till',
               'prime number till','prime number upto'):
            m = _re.search(r'(\d+)', q)
            n = int(m.group(1)) if m else 50
            primes_list = [i for i in range(2, n+1) if all(i % d != 0 for d in range(2, int(i**0.5)+1))]
            return f"""**Prime Numbers Till {n} — Python**

Prime number wo hota hai jo sirf 1 aur khud se divide ho — jaise 2, 3, 5, 7 ...

```python
# ── Step 1: Helper function — check karo koi number prime hai ya nahi ──
def is_prime(n):
    if n < 2:
        return False               # 0 aur 1 prime nahi hote
    for i in range(2, int(n**0.5) + 1):   # sirf sqrt(n) tak check karo
        if n % i == 0:
            return False           # koi divisor mila — prime nahi
    return True                    # koi divisor nahi mila — prime hai!

# ── Step 2: 2 se {n} tak saare prime numbers nikalo ──
limit = {n}
primes = [num for num in range(2, limit + 1) if is_prime(num)]

# ── Step 3: Result print karo ──
print(f"Prime numbers till {{limit}}:")
print(primes)
print(f"Total count: {{len(primes)}}")
```

**Output:**
```
Prime numbers till {n}:
{primes_list}
Total count: {len(primes_list)}
```

**Logic samjho:**
- `range(2, sqrt(n)+1)` — puri range tak nahi, sirf square root tak check karna kaafi hai
- Agar `n % i == 0` — matlab i ek divisor hai, to prime nahi
- List comprehension se ek line mein saari primes nikali"""

        # ── General prime — check karna hai ya concept samajhna hai ──
        if has('prime number','prime numbers','print prime','check prime'):
            return """**Prime Number — Python**

Prime number = sirf 1 aur khud se divisible ho (e.g. 2, 3, 5, 7, 11 ...)

```python
# ── Part 1: Ek number check karo ──────────────────────────────
def is_prime(n):
    if n < 2:
        return False               # 0, 1 — prime nahi hote
    if n == 2:
        return True                # 2 — sabse chhota prime
    if n % 2 == 0:
        return False               # baaki even numbers — prime nahi
    for i in range(3, int(n**0.5) + 1, 2):  # sirf odd numbers check karo
        if n % i == 0:
            return False           # divisor mila — prime nahi
    return True                    # koi divisor nahi — prime hai!

# Test karo
num = 37
result = "PRIME ✓" if is_prime(num) else "NOT prime ✗"
print(f"{num} is {result}")        # 37 is PRIME ✓

# ── Part 2: Range mein saare primes nikalo ─────────────────────
primes = [n for n in range(2, 51) if is_prime(n)]
print("Primes (2 to 50):", primes)
print("Total primes:", len(primes))
# Output: [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
# Total: 15

# ── Part 3: Sieve of Eratosthenes — bada range fast nikalo ────
def sieve(limit):
    is_p = [True] * (limit + 1)   # pehle sab prime maan lo
    is_p[0] = is_p[1] = False     # 0 aur 1 prime nahi
    for i in range(2, int(limit**0.5) + 1):
        if is_p[i]:
            for j in range(i*i, limit + 1, i):
                is_p[j] = False   # multiples ko cross karo
    return [i for i in range(2, limit + 1) if is_p[i]]

print("Sieve (1-100):", sieve(100))
```"""

        if has('palindrome'):
            return """**Palindrome Check — Python**
```python
def is_palindrome(s):
    s = s.lower().replace(" ", "")
    return s == s[::-1]         # reverse se compare

words = ["madam", "hello", "racecar", "level", "python"]
for w in words:
    print(f"{w}: {'Palindrome ✓' if is_palindrome(w) else 'Not Palindrome ✗'}")
# madam: Palindrome ✓
# hello: Not Palindrome ✗
# racecar: Palindrome ✓
```"""

        if has('bubble sort','bubblesort'):
            return """**Bubble Sort — Python**
```python
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(n-i-1):
            if arr[j] > arr[j+1]:           # bada pehle hai?
                arr[j], arr[j+1] = arr[j+1], arr[j]  # swap
    return arr

nums = [64, 34, 25, 12, 22, 11, 90]
print("Before:", nums)
print("After: ", bubble_sort(nums[:]))
# Before: [64, 34, 25, 12, 22, 11, 90]
# After:  [11, 12, 22, 25, 34, 64, 90]
```"""

        if has('selection sort','selectionsort'):
            return """**Selection Sort — Python**
```python
def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            if arr[j] < arr[min_idx]:   # chota element dhundo
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]  # swap
    return arr

arr = [64, 25, 12, 22, 11]
print("Sorted:", selection_sort(arr))
# Output: [11, 12, 22, 25, 64]
```"""

        if has('insertion sort','insertionsort'):
            return """**Insertion Sort — Python**
```python
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]            # current element
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j+1] = arr[j]  # shift right
            j -= 1
        arr[j+1] = key         # sahi jagah daalo
    return arr

arr = [12, 11, 13, 5, 6]
print("Sorted:", insertion_sort(arr))
# Output: [5, 6, 11, 12, 13]
```"""

        if has('binary search','binarysearch'):
            return """**Binary Search — Python**
```python
def binary_search(arr, target):
    low, high = 0, len(arr)-1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:  return mid   # found!
        elif arr[mid] < target: low = mid+1  # right half
        else:                   high = mid-1 # left half
    return -1  # not found

arr = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
print("Index of 23:", binary_search(arr, 23))   # 5
print("Index of 99:", binary_search(arr, 99))   # -1
```"""

        if has('linear search','linearsearch'):
            return """**Linear Search — Python**
```python
def linear_search(arr, target):
    for i, val in enumerate(arr):   # har element check karo
        if val == target:
            return i                # mila! index return karo
    return -1                       # nahi mila

arr = [10, 25, 38, 42, 57, 63]
print("Index of 42:", linear_search(arr, 42))   # 3
print("Index of 99:", linear_search(arr, 99))   # -1
```"""

        if has('reverse string','reverse a string','string reverse'):
            return """**Reverse String — Python**
```python
s = "QueryNest"
print("Original:", s)
print("Reversed:", s[::-1])         # slicing se reverse
print("Reversed:", ''.join(reversed(s)))  # reversed() se

# Number reverse
num = 12345
print("Reversed num:", int(str(num)[::-1]))  # 54321
```"""

        if has('pattern','star pattern','triangle','pyramid','diamond',
                'isosceles','equilateral','scalene'):
            return r"""**Star Patterns — Python**
```python
n = 5

# 1. Right Triangle (Scalene)
print("Right Triangle:")
for i in range(1, n+1):
    print("* " * i)

# 2. Isosceles Triangle (centered pyramid)
print("\nIsosceles Triangle:")
for i in range(1, n+1):
    print(" "*(n-i) + "* "*i)

# Output:
#     *
#    * *
#   * * *
#  * * * *
# * * * * *

# 3. Equilateral-style (solid pyramid with odd stars)
print("\nEquilateral Triangle:")
for i in range(1, n+1):
    print(" "*(n-i) + "*"*(2*i-1))

# Output:
#     *
#    ***
#   *****
#  *******
# *********

# 4. Diamond
print("\nDiamond:")
for i in range(1, n+1): print(" "*(n-i)+"* "*i)
for i in range(n-1, 0, -1): print(" "*(n-i)+"* "*i)

# 5. Number Triangle
print("\nNumber Triangle:")
for i in range(1, n+1):
    print(*range(1, i+1))
```"""

        if has('calculator','simple calculator'):
            return """**Calculator — Python**
```python
def calc(a, b, op):
    if op == '+': return a + b
    if op == '-': return a - b
    if op == '*': return a * b
    if op == '/': return a/b if b!=0 else "Error: div by zero"

a, b = 10, 5
for op in ['+', '-', '*', '/']:
    print(f"{a} {op} {b} = {calc(a, b, op)}")
# 10 + 5 = 15
# 10 - 5 = 5
# 10 * 5 = 50
# 10 / 5 = 2.0
```"""

        if has('matrix','matrix multiplication','2d array'):
            return """**Matrix Multiplication — Python**
```python
A = [[1,2],[3,4]]
B = [[5,6],[7,8]]
n = len(A)
C = [[0]*n for _ in range(n)]       # result matrix

for i in range(n):
    for j in range(n):
        for k in range(n):
            C[i][j] += A[i][k] * B[k][j]  # dot product

print("Matrix A:", A)
print("Matrix B:", B)
print("Result C:", C)
# Result: [[19, 22], [43, 50]]
```"""

        if has('linked list','linkedlist'):
            return """**Linked List — Python**
```python
class Node:
    def __init__(self, data):
        self.data = data        # value store karo
        self.next = None        # next node pointer

class LinkedList:
    def __init__(self): self.head = None

    def append(self, data):
        new = Node(data)
        if not self.head:
            self.head = new; return
        cur = self.head
        while cur.next: cur = cur.next  # end tak jao
        cur.next = new

    def display(self):
        cur = self.head
        while cur:
            print(cur.data, end=' -> ')
            cur = cur.next
        print("None")

ll = LinkedList()
for v in [10, 20, 30, 40]:
    ll.append(v)
ll.display()   # 10 -> 20 -> 30 -> 40 -> None
```"""

        if has('stack'):
            return """**Stack — Python**
```python
stack = []                      # list as stack

# Push
stack.append(10)
stack.append(20)
stack.append(30)
print("Stack:", stack)          # [10, 20, 30]

# Pop
print("Popped:", stack.pop())   # 30
print("Top:",    stack[-1])     # 20
print("Empty?:", len(stack)==0) # False
```"""

        if has('queue'):
            return """**Queue — Python**
```python
from collections import deque
queue = deque()                 # deque as queue

# Enqueue
queue.append(10)
queue.append(20)
queue.append(30)
print("Queue:", list(queue))    # [10, 20, 30]

# Dequeue
print("Dequeued:", queue.popleft())  # 10
print("Front:",    queue[0])         # 20
```"""

        if has('class','oop','object oriented','inheritance','encapsulation'):
            return """**OOP / Class — Python**
```python
class Animal:
    def __init__(self, name, sound):
        self.name  = name       # instance variable
        self.sound = sound

    def speak(self):
        print(f"{self.name} says {self.sound}!")

class Dog(Animal):              # inheritance
    def __init__(self, name):
        super().__init__(name, "Woof")  # parent constructor

    def fetch(self):
        print(f"{self.name} fetches the ball!")

d = Dog("Tommy")
d.speak()    # Tommy says Woof!
d.fetch()    # Tommy fetches the ball!
```"""

        if has('file','read file','write file','file handling'):
            return """**File Handling — Python**
```python
# Write to file
with open("data.txt", "w") as f:
    f.write("Alice,20,92\\n")
    f.write("Bob,21,78\\n")
print("File written!")

# Read from file
with open("data.txt", "r") as f:
    for line in f:
        name, age, marks = line.strip().split(",")
        print(f"Name:{name}  Age:{age}  Marks:{marks}")
# Name:Alice  Age:20  Marks:92
# Name:Bob    Age:21  Marks:78
```"""

        if has('recursion','recursive'):
            return """**Recursion — Python**
```python
# 1. Factorial
def factorial(n):
    if n <= 1: return 1
    return n * factorial(n-1)

# 2. Fibonacci
def fib(n):
    if n <= 1: return n
    return fib(n-1) + fib(n-2)

# 3. Sum of digits
def sum_digits(n):
    if n < 10: return n
    return n%10 + sum_digits(n//10)

# 4. Power
def power(b, e):
    if e == 0: return 1
    return b * power(b, e-1)

print("5! =", factorial(5))         # 120
print("fib(8) =", fib(8))           # 21
print("digits(1234) =", sum_digits(1234))  # 10
print("2^10 =", power(2, 10))       # 1024
```"""

        if has('exception','try except','error handling'):
            return """**Exception Handling — Python**
```python
# Basic try-except
try:
    x = int(input("Enter number: "))
    result = 100 / x
    print("Result:", result)
except ValueError:
    print("Error: Valid number daalo!")
except ZeroDivisionError:
    print("Error: 0 se divide nahi ho sakta!")
except Exception as e:
    print("Unknown error:", e)
finally:
    print("Program khatam.")    # hamesha chalega

# Custom exception
class AgeError(Exception): pass

def set_age(age):
    if age < 0 or age > 150:
        raise AgeError(f"Invalid age: {age}")
    print("Age set:", age)

try: set_age(200)
except AgeError as e: print(e)
```"""

        if has('dictionary','dict'):
            return """**Dictionary — Python**
```python
student = {"name":"Alice","age":20,"marks":92.5,"city":"Delhi"}

print(student["name"])                      # Alice
print(student.get("phone","Not found"))     # Not found (safe)

student["email"] = "alice@test.com"        # add new key
student["marks"] = 95                      # update value
del student["city"]                         # delete key

for key, val in student.items():
    print(f"  {key}: {val}")

# Dict comprehension
squared = {x: x**2 for x in range(1,6)}
print(squared)   # {1:1, 2:4, 3:9, 4:16, 5:25}
```"""

        if has('list comprehension','listcomp'):
            return """**List Comprehension — Python**
```python
nums = [1,2,3,4,5,6,7,8,9,10]

squares  = [x**2 for x in nums]            # squares
evens    = [x for x in nums if x%2==0]     # filter evens
doubled  = [x*2 for x in nums if x>5]      # filter + transform

print("Squares:", squares)
print("Evens:  ", evens)
print("Doubled:", doubled)

# Nested list comprehension
matrix = [[i*j for j in range(1,4)] for i in range(1,4)]
print("Matrix:", matrix)
```"""

        if has('string','string method','string function','string operation'):
            return """**String Methods — Python**
```python
s = "Hello QueryNest"

print(s.upper())                    # HELLO QUERYNEST
print(s.lower())                    # hello querynest
print(s.replace("Hello","Hi"))      # Hi QueryNest
print(s.split(" "))                 # ['Hello', 'QueryNest']
print(len(s))                       # 15
print(s[6:])                        # QueryNest
print(s[::-1])                      # reverse
print("nest" in s.lower())          # True
print(s.startswith("Hello"))        # True
print(s.count("l"))                 # 2
print(s.strip())                    # trim spaces
print(", ".join(["a","b","c"]))     # a, b, c
```"""

        if has('number pattern','number triangle','floyd','multiplication table'):
            return """**Number Patterns — Python**
```python
n = 5

print("Floyd's Triangle:")
num = 1
for i in range(1, n+1):
    for j in range(i):
        print(num, end=' ')
        num += 1
    print()

print("\\nMultiplication Table (5):")
for i in range(1, 11):
    print(f"5 x {i:2} = {5*i}")

print("\\nPascal's Triangle:")
row = [1]
for i in range(n):
    print(row)
    row = [1]+[row[j]+row[j+1] for j in range(len(row)-1)]+[1]
```"""

        if has('happy number','happy num'):
            return """**Happy Number — Python**
```python
def is_happy(n):
    seen = set()
    while n != 1:
        if n in seen: return False   # cycle = not happy
        seen.add(n)
        n = sum(int(d)**2 for d in str(n))  # digits ke squares ka sum
    return True

print("Happy numbers (1-50):")
print([n for n in range(1,51) if is_happy(n)])
# Output: [1, 7, 10, 13, 19, 23, 28, 31, 32, 44, 49]
```"""

        if has('perfect number','perfect num'):
            return """**Perfect Number — Python**
```python
def is_perfect(n):
    if n < 2: return False
    return sum(i for i in range(1,n) if n%i==0) == n

print("Perfect numbers (1–1000):")
print([n for n in range(1,1001) if is_perfect(n)])
# Output: [6, 28, 496]
# 6 = 1+2+3, 28 = 1+2+4+7+14
```"""

        if has('gcd','lcm','hcf'):
            return """**GCD and LCM — Python**
```python
import math

a, b = 48, 18

# GCD / HCF
gcd = math.gcd(a, b)
print(f"GCD({a},{b}) = {gcd}")       # 6

# LCM
lcm = (a * b) // gcd
print(f"LCM({a},{b}) = {lcm}")       # 144

# Without library
def my_gcd(a, b):
    while b: a, b = b, a%b
    return a

print("GCD (manual):", my_gcd(48, 18))  # 6
```"""

        if has('anagram'):
            return """**Anagram Check — Python**
```python
def is_anagram(s1, s2):
    s1 = s1.lower().replace(" ","")
    s2 = s2.lower().replace(" ","")
    return sorted(s1) == sorted(s2)   # sort karke compare

pairs = [("listen","silent"),("hello","world"),("triangle","integral")]
for a, b in pairs:
    print(f"{a} & {b}: {'Anagram ✓' if is_anagram(a,b) else 'Not Anagram ✗'}")
# listen & silent: Anagram ✓
# triangle & integral: Anagram ✓
```"""

        if has('harshad','niven number'):
            return """**Harshad Number — Python**
```python
def is_harshad(n):
    return n % sum(int(d) for d in str(n)) == 0

print("Harshad numbers (1–50):")
print([n for n in range(1,51) if is_harshad(n)])
# Output: [1,2,3,4,5,6,7,8,9,10,12,18,20,21,24,27,30,36,40,42,45,48,50]
```"""

        if has('count vowel','count consonant','vowel','vowels in string','vowels in','count vowels','vowels'):
            return """**Count Vowels & Consonants — Python**
```python
s = "Hello QueryNest"
vowels = "aeiouAEIOU"

v_count = sum(1 for c in s if c in vowels)
c_count = sum(1 for c in s if c.isalpha() and c not in vowels)

print(f"String: '{s}'")
print(f"Vowels:     {v_count}")     # 5
print(f"Consonants: {c_count}")     # 9
```"""

        # ── Extra built-in answers (variables, if-else, list, etc.) ─
        if _lookup_extra:
            _ex = _lookup_extra(query, 'python')
            if _ex and len(_ex.strip()) > 80:
                return _ex
        return None

    # ══════════════════════════════════════════════════════════════
    # C
    # ══════════════════════════════════════════════════════════════
    elif L == 'c':

        if has('vowel','vowels','count vowel','count vowels','vowels in string','vowels in','consonant'):
            return r"""**Count Vowels in String — C**
```c
#include <stdio.h>
#include <ctype.h>
int isVowel(char c){c=tolower(c);return c=='a'||c=='e'||c=='i'||c=='o'||c=='u';}
int main() {
    char s[] = "Hello QueryNest";
    int v=0, con=0;
    for (int i=0; s[i]; i++) {
        if (isalpha(s[i])) {
            if (isVowel(s[i])) v++;
            else               con++;
        }
    }
    printf("Vowels:     %d\n", v);    // 5
    printf("Consonants: %d\n", con);  // 9
    return 0;
}
// Output: Vowels: 5, Consonants: 9
```"""


        if has('even number','even numbers','print even','even upto','even till'):
            m = _re.search(r'(?:till|upto|up to|<=?|to)\s*(\d+)', q)
            limit = int(m.group(1)) if m else 50
            last_even = limit if limit % 2 == 0 else limit - 1
            return f"""**Even Numbers Till {limit} — C**
```c
#include <stdio.h>
int main() {{
    int n = {limit};
    printf("Even numbers 1 to %d:\\n", n);
    for (int i = 2; i <= n; i += 2)     // 2 se shuru, 2-2 jump
        printf("%d ", i);               // even number print karo
    printf("\\n");
    return 0;
}}
// Output: 2 4 6 8 ... {last_even}
```"""

        if has('odd number','odd numbers','print odd'):
            m = _re.search(r'(?:till|upto|up to|<=?|to)\s*(\d+)', q)
            limit = int(m.group(1)) if m else 50
            last_odd = limit if limit % 2 != 0 else limit - 1
            return f"""**Odd Numbers Till {limit} — C**
```c
#include <stdio.h>
int main() {{
    int n = {limit};
    printf("Odd numbers 1 to %d:\\n", n);
    for (int i = 1; i <= n; i += 2)     // 1 se shuru, 2-2 jump
        printf("%d ", i);
    printf("\\n");
    return 0;
}}
// Output: 1 3 5 7 9 ... {last_odd}
```"""

        if has('armstrong'):
            return r"""**Armstrong Number — C**
```c
#include <stdio.h>
#include <math.h>

int isArmstrong(int n) {
    int original = n, sum = 0, digits = 0, temp = n;
    while (temp > 0) { digits++; temp /= 10; }  // count digits
    temp = n;
    while (temp > 0) {
        int d = temp % 10;                        // last digit
        sum += (int)pow(d, digits);               // d^digits
        temp /= 10;
    }
    return sum == original;
}
int main() {
    printf("Armstrong (1-500): ");
    for (int i = 1; i <= 500; i++)
        if (isArmstrong(i)) printf("%d ", i);
    printf("\n");
    return 0;
}
// Output: 1 2 3 4 5 6 7 8 9 153 370 371 407
```"""

        if has('swap','exchange two','interchange'):
            return r"""**Swap Two Numbers — C**
```c
#include <stdio.h>
int main() {
    int a = 10, b = 20, temp;
    printf("Before: a=%d, b=%d\n", a, b);
    temp = a;  a = b;  b = temp;           // third variable swap
    printf("After:  a=%d, b=%d\n", a, b);

    // Without third variable
    int x = 5, y = 15;
    x = x + y;  y = x - y;  x = x - y;   // arithmetic swap
    printf("x=%d, y=%d\n", x, y);
    return 0;
}
// Before: a=10, b=20
// After:  a=20, b=10
// x=15, y=5
```"""

        if has('fibonacci','fibo'):
            return r"""**Fibonacci Series — C**
```c
#include <stdio.h>
int main() {
    int n=10, a=0, b=1, next;
    printf("Fibonacci: ");
    for (int i=0; i<n; i++) {
        printf("%d ", a);
        next = a+b;  a = b;  b = next;
    }
    printf("\n");
    return 0;
}
// Output: 0 1 1 2 3 5 8 13 21 34
```"""

        if has('factorial'):
            return r"""**Factorial — C**
```c
#include <stdio.h>
long long factorial(int n) {
    if (n <= 1) return 1;
    return n * factorial(n-1);
}
int main() {
    for (int i=1; i<=7; i++)
        printf("%d! = %lld\n", i, factorial(i));
    return 0;
}
// 1!=1, 2!=2, 3!=6, 4!=24, 5!=120, 6!=720, 7!=5040
```"""

        if has('prime numbers till','prime till','primes till','prime upto','primes upto',
               'prime up to','primes up to','print prime till','print primes till',
               'prime number till','prime number upto'):
            m = _re.search(r'(\d+)', q)
            n = int(m.group(1)) if m else 50
            return rf"""**Prime Numbers Till {n} — C**

Prime = sirf 1 aur khud se divisible (2, 3, 5, 7 ...)

```c
#include <stdio.h>
#include <math.h>

/* ── Check function: prime hai ya nahi ── */
int isPrime(int n) {{
    if (n < 2) return 0;                    /* 0,1 prime nahi */
    for (int i = 2; i <= (int)sqrt(n); i++) /* sqrt tak check */
        if (n % i == 0) return 0;           /* divisor mila — not prime */
    return 1;                               /* prime hai */
}}

int main() {{
    int limit = {n};
    printf("Prime numbers till %d:\n", limit);
    int count = 0;
    for (int i = 2; i <= limit; i++) {{
        if (isPrime(i)) {{
            printf("%d ", i);               /* prime print karo */
            count++;
        }}
    }}
    printf("\nTotal: %d\n", count);
    return 0;
}}
```"""

        if has('prime number','prime numbers','print prime','check prime'):
            return r"""**Prime Number — C**

Prime = sirf 1 aur khud se divisible (2, 3, 5, 7 ...)

```c
#include <stdio.h>
#include <math.h>

/* ── Part 1: Check karo ek number prime hai ya nahi ── */
int isPrime(int n) {
    if (n < 2) return 0;                    /* 0,1 prime nahi hote */
    if (n == 2) return 1;                   /* 2 prime hai */
    if (n % 2 == 0) return 0;              /* even = not prime */
    for (int i = 3; i <= (int)sqrt(n); i += 2)  /* sirf odd check */
        if (n % i == 0) return 0;           /* divisor mila */
    return 1;                               /* prime hai! */
}

int main() {
    /* ── Part 2: Single number check ── */
    int num = 37;
    printf("%d is %s\n", num, isPrime(num) ? "PRIME" : "NOT prime");

    /* ── Part 3: 2 se 50 tak saare primes ── */
    printf("Primes (2-50): ");
    int count = 0;
    for (int i = 2; i <= 50; i++) {
        if (isPrime(i)) { printf("%d ", i); count++; }
    }
    printf("\nTotal: %d\n", count);
    /* Output: 2 3 5 7 11 13 17 19 23 29 31 37 41 43 47 — Total: 15 */
    return 0;
}
```"""

        if has('palindrome'):
            return r"""**Palindrome — C**
```c
#include <stdio.h>
#include <string.h>
int isPalin(char s[]) {
    int l=0, r=strlen(s)-1;
    while (l<r) { if(s[l]!=s[r]) return 0; l++; r--; }
    return 1;
}
int isNumPalin(int n) {
    int orig=n, rev=0;
    while (n>0) { rev=rev*10+n%10; n/=10; }
    return orig==rev;
}
int main() {
    printf("madam: %s\n",    isPalin("madam")   ?"Palindrome":"Not");
    printf("hello: %s\n",    isPalin("hello")   ?"Palindrome":"Not");
    printf("racecar: %s\n",  isPalin("racecar") ?"Palindrome":"Not");
    printf("121: %s\n",      isNumPalin(121)    ?"Palindrome":"Not");
    return 0;
}
```"""

        if has('bubble sort','bubblesort'):
            return r"""**Bubble Sort — C**
```c
#include <stdio.h>
void bubbleSort(int arr[], int n) {
    for (int i=0; i<n-1; i++)
        for (int j=0; j<n-i-1; j++)
            if (arr[j]>arr[j+1]) {
                int t=arr[j]; arr[j]=arr[j+1]; arr[j+1]=t;
            }
}
int main() {
    int arr[]={64,34,25,12,22,11,90}, n=7;
    printf("Before: "); for(int i=0;i<n;i++) printf("%d ",arr[i]);
    bubbleSort(arr, n);
    printf("\nAfter:  "); for(int i=0;i<n;i++) printf("%d ",arr[i]);
    printf("\n");
    return 0;
}
// Before: 64 34 25 12 22 11 90
// After:  11 12 22 25 34 64 90
```"""

        if has('binary search'):
            return r"""**Binary Search — C**
```c
#include <stdio.h>
int binarySearch(int arr[], int n, int target) {
    int low=0, high=n-1;
    while (low<=high) {
        int mid=(low+high)/2;
        if (arr[mid]==target) return mid;
        else if (arr[mid]<target) low=mid+1;
        else high=mid-1;
    }
    return -1;
}
int main() {
    int arr[]={2,5,8,12,16,23,38,56,72,91}, n=10;
    printf("Index of 23: %d\n", binarySearch(arr,n,23));  // 5
    printf("Index of 99: %d\n", binarySearch(arr,n,99));  // -1
    return 0;
}
```"""

        if has('selection sort'):
            return r"""**Selection Sort — C**
```c
#include <stdio.h>
void selectionSort(int arr[], int n) {
    for (int i=0; i<n-1; i++) {
        int min=i;
        for (int j=i+1; j<n; j++)
            if (arr[j]<arr[min]) min=j;
        int t=arr[i]; arr[i]=arr[min]; arr[min]=t;
    }
}
int main() {
    int arr[]={64,25,12,22,11}, n=5;
    selectionSort(arr,n);
    printf("Sorted: "); for(int i=0;i<n;i++) printf("%d ",arr[i]);
    return 0;
}
// Output: 11 12 22 25 64
```"""

        if has('pattern','star','triangle','pyramid','diamond'):
            return r"""**Patterns — C**
```c
#include <stdio.h>
int main() {
    int n=5;
    printf("Right Triangle:\n");
    for(int i=1;i<=n;i++){for(int j=0;j<i;j++)printf("* ");printf("\n");}

    printf("\nPyramid:\n");
    for(int i=1;i<=n;i++){
        for(int j=i;j<n;j++)printf(" ");
        for(int j=1;j<=2*i-1;j++)printf("*");
        printf("\n");
    }
    printf("\nNumber Triangle:\n");
    for(int i=1;i<=n;i++){for(int j=1;j<=i;j++)printf("%d ",j);printf("\n");}
    return 0;
}
```"""

        if has('recursion','recursive'):
            return r"""**Recursion — C**
```c
#include <stdio.h>
#include <math.h>
long factorial(int n){ return n<=1?1:n*factorial(n-1); }
long fib(int n){ return n<=1?n:fib(n-1)+fib(n-2); }
int sumDigits(int n){ return n<10?n:n%10+sumDigits(n/10); }
long power(int b,int e){ return e==0?1:b*power(b,e-1); }
int gcd(int a,int b){ return b==0?a:gcd(b,a%b); }

int main() {
    printf("5!=%ld  fib(8)=%ld  digits(1234)=%d  2^10=%ld  gcd(48,18)=%d\n",
        factorial(5), fib(8), sumDigits(1234), power(2,10), gcd(48,18));
    return 0;
}
// 5!=120  fib(8)=21  digits(1234)=10  2^10=1024  gcd(48,18)=6
```"""

        if has('pointer'):
            return r"""**Pointers — C**
```c
#include <stdio.h>
int main() {
    int x=42, *ptr=&x;
    printf("Value: %d\n", x);
    printf("Address: %p\n", ptr);
    printf("Via ptr: %d\n", *ptr);
    *ptr=100;
    printf("Changed: %d\n", x);       // 100

    // Pointer arithmetic
    int arr[]={10,20,30,40,50};
    int *p=arr;
    printf("Array: ");
    for(int i=0;i<5;i++) printf("%d ",*(p+i));
    printf("\n");
    return 0;
}
```"""

        if has('struct','structure'):
            return r"""**Structure — C**
```c
#include <stdio.h>
#include <string.h>
struct Student {
    int id;
    char name[50];
    float marks;
};
int main() {
    struct Student s1={1,"Alice",92.5};
    struct Student s2={2,"Bob",  78.0};
    struct Student arr[]={{1,"Alice",92.5},{2,"Bob",78.0},{3,"Charlie",85.0}};
    int n=3;
    printf("%-5s %-15s %s\n","ID","Name","Marks");
    for(int i=0;i<n;i++)
        printf("%-5d %-15s %.1f\n",arr[i].id,arr[i].name,arr[i].marks);
    return 0;
}
```"""

        if has('calculator'):
            return r"""**Calculator — C**
```c
#include <stdio.h>
int main() {
    float a=10,b=5;
    printf("Add:      %.1f\n", a+b);
    printf("Subtract: %.1f\n", a-b);
    printf("Multiply: %.1f\n", a*b);
    printf("Divide:   %.1f\n", b!=0?a/b:0);
    return 0;
}
// Add:10+5=15, Sub:5, Mul:50, Div:2
```"""

        if has('string','string function','strlen','strcpy','strcat'):
            return r"""**String Functions — C**
```c
#include <stdio.h>
#include <string.h>
int main() {
    char s1[50]="Hello", s2[]=" World";
    printf("Length: %lu\n",  strlen(s1));        // 5
    strcat(s1, s2);
    printf("Concat: %s\n",   s1);                // Hello World
    printf("Compare: %d\n",  strcmp("abc","abc")); // 0 = equal
    char dest[50]; strcpy(dest,"QueryNest");
    printf("Copy: %s\n",     dest);
    // Uppercase manual
    for(int i=0;s1[i];i++) if(s1[i]>='a'&&s1[i]<='z') s1[i]-=32;
    printf("Upper: %s\n",    s1);
    return 0;
}
```"""

        if has('matrix','2d array','matrix multiply'):
            return r"""**Matrix Multiplication — C**
```c
#include <stdio.h>
#define N 3
void multiply(int A[N][N], int B[N][N], int C[N][N]) {
    for(int i=0;i<N;i++) for(int j=0;j<N;j++) {
        C[i][j]=0;
        for(int k=0;k<N;k++) C[i][j]+=A[i][k]*B[k][j];
    }
}
void print(int M[N][N]){for(int i=0;i<N;i++){for(int j=0;j<N;j++)printf("%4d",M[i][j]);printf("\n");}}
int main() {
    int A[N][N]={{1,2,3},{4,5,6},{7,8,9}};
    int B[N][N]={{9,8,7},{6,5,4},{3,2,1}};
    int C[N][N]={};
    multiply(A,B,C);
    printf("Result:\n"); print(C);
    return 0;
}
```"""

        if has('linked list','linkedlist'):
            return r"""**Linked List — C**
```c
#include <stdio.h>
#include <stdlib.h>
struct Node { int data; struct Node* next; };

struct Node* insertFront(struct Node* head, int val) {
    struct Node* n=(struct Node*)malloc(sizeof(struct Node));
    n->data=val; n->next=head; return n;
}
void print(struct Node* h){while(h){printf("%d->",h->data);h=h->next;}printf("NULL\n");}

int main() {
    struct Node* head=NULL;
    head=insertFront(head,30);
    head=insertFront(head,20);
    head=insertFront(head,10);
    print(head);    // 10->20->30->NULL
    return 0;
}
```"""

        if has('gcd','lcm','hcf'):
            return r"""**GCD and LCM — C**
```c
#include <stdio.h>
int gcd(int a,int b){ return b==0?a:gcd(b,a%b); }
int main() {
    int a=48, b=18;
    int g=gcd(a,b);
    printf("GCD(%d,%d) = %d\n",a,b,g);       // 6
    printf("LCM(%d,%d) = %d\n",a,b,a*b/g);   // 144
    return 0;
}
```"""


        if has('harshad','niven'):
            return r"""**Harshad Number — C**
```c
#include <stdio.h>
int digitSum(int n) {
    int sum = 0;
    while (n > 0) { sum += n % 10; n /= 10; }
    return sum;
}
int isHarshad(int n) { return n % digitSum(n) == 0; }
int main() {
    printf("Harshad numbers (1-100):\n");
    for (int i = 1; i <= 100; i++)
        if (isHarshad(i)) printf("%d ", i);
    printf("\n\nCheck 18: digit sum=%d, Harshad=%s\n",
        digitSum(18), isHarshad(18)?"YES":"NO");
    return 0;
}
// Output:
// Harshad: 1 2 3 4 5 6 7 8 9 10 12 18 20 21 24 27 30 36 40 42 45...
// Check 18: digit sum=9, Harshad=YES
```"""

        if has('perfect number','perfect num'):
            return r"""**Perfect Number — C**
```c
#include <stdio.h>
int isPerfect(int n) {
    if (n<2) return 0;
    int sum=1;
    for (int i=2; i*i<=n; i++)
        if (n%i==0) { sum+=i; if(i!=n/i) sum+=n/i; }
    return sum==n;
}
int main() {
    printf("Perfect numbers (1-1000):\n");
    for (int i=1;i<=1000;i++) if(isPerfect(i)) printf("%d ",i);
    printf("\n");
    return 0;
}
// Output: 6 28 496
```"""

        if has('happy number','happy num'):
            return r"""**Happy Number — C**
```c
#include <stdio.h>
int sumSqDigits(int n){int s=0,d;while(n>0){d=n%10;s+=d*d;n/=10;}return s;}
int isHappy(int n){
    int slow=n,fast=sumSqDigits(n);
    while(fast!=1&&slow!=fast){slow=sumSqDigits(slow);fast=sumSqDigits(sumSqDigits(fast));}
    return fast==1;
}
int main() {
    printf("Happy numbers (1-50):\n");
    for(int i=1;i<=50;i++) if(isHappy(i)) printf("%d ",i);
    printf("\n");
    return 0;
}
// Output: 1 7 10 13 19 23 28 31 32 44 49
```"""

        if has('reverse number','reverse a number','reverse num','number reverse'):
            return r"""**Reverse Number — C**
```c
#include <stdio.h>
int reverseNum(int n) {
    int rev = 0;
    while (n > 0) { rev = rev*10 + n%10; n /= 10; }
    return rev;
}
int main() {
    printf("Reverse of 12345 = %d\n", reverseNum(12345));  // 54321
    printf("Reverse of  9087 = %d\n", reverseNum(9087));   // 7809
    return 0;
}
```"""

        if has('anagram'):
            return r"""**Anagram Check — C**
```c
#include <stdio.h>
#include <string.h>
#include <ctype.h>
int isAnagram(char s1[], char s2[]) {
    int f[26]={0};
    for(int i=0;s1[i];i++) f[tolower(s1[i])-'a']++;
    for(int i=0;s2[i];i++) f[tolower(s2[i])-'a']--;
    for(int i=0;i<26;i++) if(f[i]!=0) return 0;
    return 1;
}
int main() {
    printf("listen & silent: %s\n", isAnagram("listen","silent")?"Anagram":"Not");
    printf("hello  & world:  %s\n", isAnagram("hello","world") ?"Anagram":"Not");
    return 0;
}
// Output:
// listen & silent: Anagram
// hello  & world:  Not
```"""

        if has('harshad','niven'):
            return """**Harshad Number — Java**
```java
public class Harshad {
    static int digitSum(int n) {
        int sum = 0;
        while (n > 0) { sum += n % 10; n /= 10; }
        return sum;
    }
    static boolean isHarshad(int n) { return n % digitSum(n) == 0; }
    public static void main(String[] args) {
        System.out.print("Harshad numbers (1-100): ");
        for (int i = 1; i <= 100; i++)
            if (isHarshad(i)) System.out.print(i + " ");
        // Output: 1 2 3 4 5 6 7 8 9 10 12 18 20 21 24 27 30 36 40 42 45...
    }
}
```"""

        if has('vowel','count vowel','vowels in string','vowels in','count vowels','consonant','vowels'):
            return r"""**Count Vowels in String — C**
```c
#include <stdio.h>
#include <ctype.h>
int isVowel(char c){c=tolower(c);return c=='a'||c=='e'||c=='i'||c=='o'||c=='u';}
int main() {
    char s[] = "Hello QueryNest";
    int v=0, con=0;
    for(int i=0; s[i]; i++) {
        if(isalpha(s[i])) {
            if(isVowel(s[i])) v++;
            else               con++;
        }
    }
    printf("Vowels:     %d\n", v);    // 5
    printf("Consonants: %d\n", con);  // 9
    return 0;
}
// Output: Vowels: 5, Consonants: 9
```"""

        # ── Extra built-in answers (variables, if-else, list, etc.) ─
        if _lookup_extra:
            _ex = _lookup_extra(query, 'python')
            if _ex and len(_ex.strip()) > 80:
                return _ex
        return None

    # ══════════════════════════════════════════════════════════════
    # C++
    # ══════════════════════════════════════════════════════════════
    elif L == 'cpp':

        if has('even number','even numbers','print even'):
            m = _re.search(r'(?:till|upto|up to|<=?|to)\s*(\d+)', q)
            limit = int(m.group(1)) if m else 50
            last_even = limit if limit % 2 == 0 else limit - 1
            return f"""**Even Numbers Till {limit} — C++**
```cpp
#include <iostream>
using namespace std;
int main() {{
    int n = {limit};
    cout << "Even numbers 1 to " << n << ": ";
    for (int i=2; i<=n; i+=2) cout << i << " ";
    cout << endl;
    return 0;
}}
// Output: 2 4 6 8 ... {last_even}
```"""

        if has('odd number','odd numbers','print odd'):
            return """**Odd Numbers — C++**
```cpp
#include <iostream>
using namespace std;
int main() {
    cout << "Odd numbers 1 to 50: ";
    for (int i=1; i<=50; i+=2) cout << i << " ";
    cout << endl;
    return 0;
}
// Output: 1 3 5 7 9 ... 49
```"""

        if has('armstrong'):
            return """**Armstrong Number — C++**
```cpp
#include <iostream>
#include <cmath>
#include <string>
using namespace std;
bool isArmstrong(int n){
    int orig=n,sum=0,d=to_string(n).length();
    while(n>0){int r=n%10;sum+=pow(r,d);n/=10;}
    return sum==orig;
}
int main(){
    cout<<"Armstrong (1-500): ";
    for(int i=1;i<=500;i++) if(isArmstrong(i)) cout<<i<<" ";
    cout<<endl;
    return 0;
}
// Output: 1 2 3 4 5 6 7 8 9 153 370 371 407
```"""

        if has('swap','exchange two'):
            return """**Swap — C++**
```cpp
#include <iostream>
using namespace std;
int main(){
    int a=10,b=20;
    cout<<"Before: a="<<a<<", b="<<b<<endl;
    swap(a,b);                // STL swap
    cout<<"After:  a="<<a<<", b="<<b<<endl;
    return 0;
}
// Before: a=10, b=20
// After:  a=20, b=10
```"""

        if has('fibonacci'):
            return """**Fibonacci — C++**
```cpp
#include <iostream>
using namespace std;
int main(){
    int n=10,a=0,b=1,next;
    cout<<"Fibonacci: ";
    for(int i=0;i<n;i++){cout<<a<<" ";next=a+b;a=b;b=next;}
    cout<<endl; return 0;
}
// Output: 0 1 1 2 3 5 8 13 21 34
```"""

        if has('factorial'):
            return """**Factorial — C++**
```cpp
#include <iostream>
using namespace std;
long long factorial(int n){ return n<=1?1:n*factorial(n-1); }
int main(){
    for(int i=1;i<=7;i++) cout<<i<<"! = "<<factorial(i)<<endl;
    return 0;
}
// 1!=1, 2!=2, 3!=6, 4!=24, 5!=120, 6!=720, 7!=5040
```"""

        if has('prime numbers till','prime till','primes till','prime upto','primes upto',
               'prime up to','primes up to','print prime till','print primes till',
               'prime number till','prime number upto'):
            m = _re.search(r'(\d+)', q)
            n = int(m.group(1)) if m else 50
            return f"""**Prime Numbers Till {n} — C++**

Prime = sirf 1 aur khud se divisible (2, 3, 5, 7 ...)

```cpp
#include <iostream>
#include <cmath>
using namespace std;

// ── Check function ──────────────────────────────────────
bool isPrime(int n) {{
    if (n < 2) return false;               // 0,1 prime nahi
    for (int i = 2; i <= sqrt(n); i++)    // sqrt tak check
        if (n % i == 0) return false;      // divisor mila
    return true;                           // prime hai!
}}

int main() {{
    int limit = {n};
    cout << "Prime numbers till " << limit << ":" << endl;
    int count = 0;
    for (int i = 2; i <= limit; i++) {{
        if (isPrime(i)) {{
            cout << i << " ";              // prime print karo
            count++;
        }}
    }}
    cout << endl << "Total: " << count << endl;
    return 0;
}}
```"""

        if has('prime number','prime numbers','print prime'):
            return """**Prime Number — C++**

Prime = sirf 1 aur khud se divisible (2, 3, 5, 7 ...)

```cpp
#include <iostream>
#include <cmath>
using namespace std;

// ── Part 1: Check karo ek number prime hai ya nahi ──
bool isPrime(int n) {
    if (n < 2) return false;               // 0,1 prime nahi hote
    if (n == 2) return true;              // 2 prime hai
    if (n % 2 == 0) return false;         // even = not prime
    for (int i = 3; i <= sqrt(n); i += 2) // sirf odd check karo
        if (n % i == 0) return false;      // divisor mila
    return true;                           // prime hai!
}

int main() {
    // ── Part 2: Single number check ──
    int num = 37;
    cout << num << " is " << (isPrime(num) ? "PRIME" : "NOT prime") << endl;

    // ── Part 3: 2 se 50 tak saare primes nikalo ──
    cout << "Primes (2-50): ";
    int count = 0;
    for (int i = 2; i <= 50; i++) {
        if (isPrime(i)) { cout << i << " "; count++; }
    }
    cout << endl << "Total: " << count << endl;
    // Output: 2 3 5 7 11 13 17 19 23 29 31 37 41 43 47 — Total: 15
    return 0;
}
```"""

        if has('palindrome'):
            return """**Palindrome — C++**
```cpp
#include <iostream>
#include <string>
#include <algorithm>
using namespace std;
bool isPalin(string s){
    string r=s; reverse(r.begin(),r.end());
    return s==r;
}
int main(){
    vector<string> words={"madam","hello","racecar","level"};
    for(auto w:words)
        cout<<w<<": "<<(isPalin(w)?"Palindrome":"Not Palindrome")<<endl;
    return 0;
}
```"""

        if has('bubble sort','bubblesort'):
            return """**Bubble Sort — C++**
```cpp
#include <iostream>
#include <vector>
using namespace std;
void bubbleSort(vector<int>& arr){
    int n=arr.size();
    for(int i=0;i<n-1;i++)
        for(int j=0;j<n-i-1;j++)
            if(arr[j]>arr[j+1]) swap(arr[j],arr[j+1]);
}
int main(){
    vector<int> arr={64,34,25,12,22,11,90};
    cout<<"Before: "; for(int x:arr) cout<<x<<" ";
    bubbleSort(arr);
    cout<<"\nAfter:  "; for(int x:arr) cout<<x<<" ";
    cout<<endl; return 0;
}
// Before: 64 34 25 12 22 11 90
// After:  11 12 22 25 34 64 90
```"""

        if has('vector','stl','array list'):
            return """**Vector (STL) — C++**
```cpp
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;
int main(){
    vector<int> v={5,2,8,1,9,3};
    v.push_back(7);                      // add element
    sort(v.begin(),v.end());             // sort
    cout<<"Sorted: "; for(int x:v) cout<<x<<" ";
    cout<<"\nSize: "<<v.size()<<endl;
    cout<<"Max: "<<*max_element(v.begin(),v.end())<<endl;
    v.erase(v.begin());                  // remove first
    return 0;
}
// Sorted: 1 2 3 5 7 8 9
```"""

        if has('class','oop','object','inheritance'):
            return """**Class & OOP — C++**
```cpp
#include <iostream>
#include <string>
using namespace std;
class Animal {
protected: string name;
public:
    Animal(string n):name(n){}
    virtual void speak(){ cout<<name<<" makes a sound"<<endl; }
};
class Dog:public Animal {
public:
    Dog(string n):Animal(n){}
    void speak() override { cout<<name<<" says: Woof!"<<endl; }
};
int main(){
    Animal* a=new Dog("Tommy");
    a->speak();    // Tommy says: Woof!
    delete a;
    return 0;
}
```"""

        if has('pattern','star','triangle','pyramid'):
            return """**Patterns — C++**
```cpp
#include <iostream>
using namespace std;
int main(){
    int n=5;
    cout<<"Right Triangle:\n";
    for(int i=1;i<=n;i++){for(int j=0;j<i;j++)cout<<"* ";cout<<"\n";}
    cout<<"\nPyramid:\n";
    for(int i=1;i<=n;i++){
        for(int j=i;j<n;j++)cout<<" ";
        for(int j=1;j<=2*i-1;j++)cout<<"*";
        cout<<"\n";
    }
    return 0;
}
```"""

        if has('recursion','recursive'):
            return """**Recursion — C++**
```cpp
#include <iostream>
using namespace std;
long long fact(int n){ return n<=1?1:n*fact(n-1); }
long long fib(int n){ return n<=1?n:fib(n-1)+fib(n-2); }
long long pw(int b,int e){ return e==0?1:b*pw(b,e-1); }
int gcd(int a,int b){ return b==0?a:gcd(b,a%b); }
int main(){
    cout<<"5!="<<fact(5)<<" fib(8)="<<fib(8)
        <<" 2^10="<<pw(2,10)<<" gcd(48,18)="<<gcd(48,18)<<endl;
    return 0;
}
// 5!=120 fib(8)=21 2^10=1024 gcd(48,18)=6
```"""

        if has('happy number','happy num'):
            return """**Happy Number — C++**
```cpp
#include <iostream>
using namespace std;
int digitSqSum(int n){int s=0;while(n>0){int d=n%10;s+=d*d;n/=10;}return s;}
bool isHappy(int n){int slow=n,fast=n;do{slow=digitSqSum(slow);fast=digitSqSum(digitSqSum(fast));}while(slow!=fast);return slow==1;}
int main(){
    cout<<"Happy numbers (1-50): ";
    for(int i=1;i<=50;i++) if(isHappy(i)) cout<<i<<" ";
    cout<<endl;
    // Output: 1 7 10 13 19 23 28 31 32 44 49
    return 0;
}
```"""

        if has('perfect number','perfect num'):
            return """**Perfect Number — C++**
```cpp
#include <iostream>
using namespace std;
bool isPerfect(int n){
    if(n<2)return false;
    int sum=1;
    for(int i=2;i*i<=n;i++){if(n%i==0){sum+=i;if(i!=n/i)sum+=n/i;}}
    return sum==n;
}
int main(){
    cout<<"Perfect numbers (1-1000): ";
    for(int i=2;i<=1000;i++) if(isPerfect(i)) cout<<i<<" ";
    cout<<endl; // Output: 6 28 496
    return 0;
}
```"""

        if has('harshad','niven'):
            return """**Harshad Number — C++**
```cpp
#include <iostream>
using namespace std;
int digitSum(int n){int s=0;while(n>0){s+=n%10;n/=10;}return s;}
int main(){
    cout<<"Harshad numbers (1-100): ";
    for(int i=1;i<=100;i++) if(i%digitSum(i)==0) cout<<i<<" ";
    cout<<endl; return 0;
}
// Output: 1 2 3 4 5 6 7 8 9 10 12 18 20 21 24 27 30 36...
```"""

        if has('gcd','lcm','hcf'):
            return """**GCD & LCM — C++**
```cpp
#include <iostream>
using namespace std;
int gcd(int a,int b){return b==0?a:gcd(b,a%b);}
int lcm(int a,int b){return (a/gcd(a,b))*b;}
int main(){
    int a=48,b=18;
    cout<<"GCD: "<<gcd(a,b)<<endl;  // 6
    cout<<"LCM: "<<lcm(a,b)<<endl;  // 144
    return 0;
}
```"""

        if has('vowel','vowels','count vowel','count vowels','consonant','vowels in string'):
            return """**Count Vowels in String — C++**
```cpp
#include <iostream>
#include <string>
using namespace std;
int main(){
    string s = "Hello QueryNest";          // input string
    string vowels = "aeiouAEIOU";
    int v=0, con=0;
    for(char c:s){
        if(isalpha(c)){                    // only letters
            if(vowels.find(c)!=string::npos) v++;   // vowel
            else con++;                              // consonant
        }
    }
    cout<<"String:     "<<s<<endl;
    cout<<"Vowels:     "<<v<<endl;   // 5
    cout<<"Consonants: "<<con<<endl; // 9
    return 0;
}
```"""

        if has('whole number','whole numbers','natural number','natural numbers',
                'print natural','print whole','1 to n','positive number'):
            return """**Natural/Whole Numbers — C++**
```cpp
#include <iostream>
using namespace std;
int main(){
    int n=10;
    cout<<"Natural numbers 1 to "<<n<<": ";
    for(int i=1;i<=n;i++) cout<<i<<" ";  // 1 2 3 ... 10
    cout<<"\nSum = "<<n*(n+1)/2<<endl;   // 55
    return 0;
}
```"""

        if has('anagram'):
            return """**Anagram — C++**
```cpp
#include <iostream>
#include <string>
#include <algorithm>
using namespace std;
bool isAnagram(string a,string b){sort(a.begin(),a.end());sort(b.begin(),b.end());return a==b;}
int main(){
    cout<<boolalpha;
    cout<<"listen/silent: "<<isAnagram("listen","silent")<<endl; // true
    cout<<"hello/world:   "<<isAnagram("hello","world")<<endl;   // false
    return 0;
}
```"""

        if has('string','string function','string method','string operation',
                'string reverse','reverse string'):
            return """**String Operations — C++**
```cpp
#include <iostream>
#include <string>
#include <algorithm>
using namespace std;
int main(){
    string s="Hello QueryNest";
    cout<<"Length:  "<<s.length()<<endl;          // 15
    cout<<"Sub:     "<<s.substr(6,9)<<endl;       // QueryNest
    cout<<"Find:    "<<s.find("Query")<<endl;     // 6
    string rev=s; reverse(rev.begin(),rev.end());
    cout<<"Reverse: "<<rev<<endl;
    string w="madam";
    string rw=w; reverse(rw.begin(),rw.end());
    cout<<"Palindrome: "<<(w==rw?"Yes":"No")<<endl; // Yes
    return 0;
}
```"""

        if has('pointer','pointers','ptr'):
            return """**Pointers — C++**
```cpp
#include <iostream>
using namespace std;
int main(){
    int x=42;
    int* ptr=&x;                    // pointer to x
    cout<<"Value:   "<<x<<endl;     // 42
    cout<<"Address: "<<ptr<<endl;   // memory address
    cout<<"Via ptr: "<<*ptr<<endl;  // 42
    *ptr=100;
    cout<<"Changed: "<<x<<endl;     // 100
    int arr[]={10,20,30,40,50};
    int* p=arr;
    cout<<"Array: ";
    for(int i=0;i<5;i++) cout<<*(p+i)<<" ";
    cout<<endl; return 0;
}
```"""

        if has('linked list','linkedlist'):
            return """**Linked List — C++**
```cpp
#include <iostream>
using namespace std;
struct Node{int data;Node* next;Node(int d):data(d),next(nullptr){}};
class LinkedList{
    Node* head=nullptr;
public:
    void push(int d){Node* n=new Node(d);n->next=head;head=n;}
    void print(){for(Node* t=head;t;t=t->next)cout<<t->data<<" → ";cout<<"NULL"<<endl;}
};
int main(){
    LinkedList ll;
    ll.push(10);ll.push(20);ll.push(30);
    ll.print(); // 30 → 20 → 10 → NULL
    return 0;
}
```"""

        if has('map','hashmap','unordered_map'):
            return """**Map/HashMap — C++**
```cpp
#include <iostream>
#include <map>
using namespace std;
int main(){
    map<string,int> marks;
    marks["Alice"]=92; marks["Bob"]=78; marks["Charlie"]=85;
    cout<<"Alice: "<<marks["Alice"]<<endl;   // 92
    for(auto& [name,m]:marks)
        cout<<name<<" → "<<m<<endl;
    // Check key exists
    cout<<"Has Diana: "<<(marks.count("Diana")?"Yes":"No")<<endl; // No
    return 0;
}
```"""

        if has('exception','try catch','error handling'):
            return """**Exception Handling — C++**
```cpp
#include <iostream>
#include <stdexcept>
using namespace std;
double divide(int a,int b){
    if(b==0) throw runtime_error("Division by zero!");
    return (double)a/b;
}
int main(){
    try{
        cout<<divide(10,2)<<endl;  // 5.0
        cout<<divide(10,0)<<endl;  // throws!
    }catch(const runtime_error& e){
        cout<<"Error: "<<e.what()<<endl;
    }
    cout<<"Program continues..."<<endl;
    return 0;
}
```"""

        # ── Extra built-in answers (variables, if-else, list, etc.) ─
        if _lookup_extra:
            _ex = _lookup_extra(query, 'python')
            if _ex and len(_ex.strip()) > 80:
                return _ex
        return None

    # ══════════════════════════════════════════════════════════════
    # JAVA
    # ══════════════════════════════════════════════════════════════
    elif L == 'java':

        if has('whole number','whole numbers','natural number','natural numbers',
                'print natural','print whole','1 to n','1 to 100','1 to 50',
                'positive number','positive integer','counting number'):
            m = _re.search(r'(?:till|upto|up to|1 to|to)\s*(\d+)', q)
            limit = int(m.group(1)) if m else 10
            return f"""**Natural / Whole Numbers (1 to {limit}) — Java**
```java
public class NaturalNumbers {{
    public static void main(String[] args) {{
        int n = {limit};                          // print karna hai 1 se n tak
        System.out.print("Natural numbers 1 to " + n + ": ");
        for (int i = 1; i <= n; i++) {{           // 1 se start, n tak
            System.out.print(i + " ");            // har number print karo
        }}
        // Output: Natural numbers 1 to {limit}: {' '.join(str(i) for i in range(1, min(limit+1, 11)))}{'...' if limit > 10 else ''}

        // Sum of natural numbers 1 to n
        int sum = n * (n + 1) / 2;               // formula: n*(n+1)/2
        System.out.println("\\nSum = " + sum);    // Output: Sum = {limit*(limit+1)//2}
    }}
}}
```"""

        if has('digit','digits','count digit','sum of digit','digit sum',
                'reverse digit','reverse number','number of digit'):
            return """**Digit Operations — Java**
```java
public class DigitOps {
    public static void main(String[] args) {
        int n = 12345;

        // Count digits
        int count = String.valueOf(n).length();        // total digits
        System.out.println("Digits: " + count);       // 5

        // Sum of digits
        int temp = n, sum = 0;
        while (temp > 0) {
            sum += temp % 10;                          // last digit add karo
            temp /= 10;                                // number chota karo
        }
        System.out.println("Digit sum: " + sum);      // 15

        // Reverse number
        temp = n; int rev = 0;
        while (temp > 0) {
            rev = rev * 10 + temp % 10;               // reverse build karo
            temp /= 10;
        }
        System.out.println("Reversed: " + rev);       // 54321
    }
}
```"""

        if has('number pattern','number triangle','floyd','multiplication table','table of'):
            num = _re.search(r'table of (\d+)', q)
            t = int(num.group(1)) if num else 5
            return f"""**Number Patterns & Tables — Java**
```java
public class NumberPattern {{
    public static void main(String[] args) {{

        // Floyd's Triangle
        System.out.println("Floyd's Triangle:");
        int num = 1;
        for (int i = 1; i <= 5; i++) {{
            for (int j = 1; j <= i; j++)
                System.out.print(num++ + " ");        // sequential numbers
            System.out.println();
        }}
        // 1
        // 2 3
        // 4 5 6

        // Multiplication table of {t}
        System.out.println("\\nTable of {t}:");
        for (int i = 1; i <= 10; i++)
            System.out.println("{t} x " + i + " = " + ({t} * i));
    }}
}}
```"""

        if has('type cast','typecast','type conversion','int to string',
                'string to int','casting','data type','parse int','parseint'):
            return """**Type Casting & Conversion — Java**
```java
public class TypeCasting {
    public static void main(String[] args) {

        // Widening (automatic)
        int i = 42;
        double d = i;                              // int → double auto
        System.out.println("int→double: " + d);   // 42.0

        // Narrowing (manual cast)
        double pi = 3.14159;
        int truncated = (int) pi;                  // decimal part cut
        System.out.println("double→int: " + truncated); // 3

        // String ↔ int
        String s = "123";
        int parsed = Integer.parseInt(s);          // String → int
        String back = String.valueOf(parsed + 1);  // int → String
        System.out.println("Parsed+1: " + back);  // "124"

        // char ↔ int
        char ch = 'A';
        int ascii = ch;                            // char → ASCII value
        System.out.println("'A' ASCII: " + ascii); // 65
    }
}
```"""

        if has('scanner','user input','take input','read input','stdin',
                'bufferedreader','console input'):
            return """**User Input (Scanner) — Java**
```java
import java.util.Scanner;
public class UserInput {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);      // Scanner object banao

        System.out.print("Enter your name: ");
        String name = sc.nextLine();              // String input

        System.out.print("Enter your age: ");
        int age = sc.nextInt();                   // int input

        System.out.print("Enter your marks: ");
        double marks = sc.nextDouble();           // double input

        System.out.println("\\nHello " + name + "!");
        System.out.println("Age: " + age);
        System.out.println("Marks: " + marks);

        sc.close();                               // Scanner band karo
    }
}
// Run: Enter name → age → marks → output milega
```"""

        if has('interface','abstract class','abstract method','implement interface'):
            return """**Interface & Abstract Class — Java**
```java
// Interface — blueprint of methods
interface Shape {
    double area();           // abstract method (no body)
    default void show() {    // default method (has body)
        System.out.println("Area: " + area());
    }
}

// Abstract class
abstract class Animal {
    String name;
    Animal(String n) { this.name = n; }
    abstract void sound();   // must be overridden
    void breathe() { System.out.println(name + " breathes"); }
}

class Circle extends Animal implements Shape {
    double r;
    Circle(String n, double r) { super(n); this.r = r; }
    public double area() { return Math.PI * r * r; }  // interface method
    public void sound() { System.out.println(name + ": ..."); }
}

public class Main {
    public static void main(String[] args) {
        Circle c = new Circle("Circle", 5);
        c.show();       // Area: 78.53...
        c.breathe();    // Circle breathes
    }
}
```"""

        if has('even number','even numbers','print even'):

            m = _re.search(r'(?:till|upto|up to|<=?|to)\s*(\d+)', q)
            limit = int(m.group(1)) if m else 50
            last_even = limit if limit % 2 == 0 else limit - 1
            return f"""**Even Numbers Till {limit} — Java**
```java
public class EvenNumbers {{
    public static void main(String[] args) {{
        int n = {limit};
        System.out.print("Even numbers 1 to " + n + ": ");
        for (int i = 2; i <= n; i += 2)
            System.out.print(i + " ");
        // Output: 2 4 6 8 ... {last_even}
    }}
}}
```"""

        if has('odd number','odd numbers','print odd'):
            return """**Odd Numbers — Java**
```java
public class OddNumbers {
    public static void main(String[] args) {
        System.out.print("Odd numbers 1 to 50: ");
        for (int i = 1; i <= 50; i += 2)
            System.out.print(i + " ");
    }
}
// Output: 1 3 5 7 9 ... 49
```"""

        if has('armstrong'):
            return """**Armstrong Number — Java**
```java
public class Armstrong {
    static boolean isArmstrong(int n) {
        int orig=n, sum=0, d=String.valueOf(n).length();
        while (n>0) { int r=n%10; sum+=(int)Math.pow(r,d); n/=10; }
        return sum==orig;
    }
    public static void main(String[] args) {
        System.out.print("Armstrong (1-500): ");
        for (int i=1;i<=500;i++) if(isArmstrong(i)) System.out.print(i+" ");
    }
}
// Output: 1 2 3 4 5 6 7 8 9 153 370 371 407
```"""

        if has('swap','exchange two'):
            return """**Swap Two Numbers — Java**
```java
public class Swap {
    public static void main(String[] args) {
        int a=10, b=20, temp;
        System.out.println("Before: a="+a+", b="+b);
        temp=a; a=b; b=temp;
        System.out.println("After:  a="+a+", b="+b);
    }
}
// Before: a=10, b=20
// After:  a=20, b=10
```"""

        if has('fibonacci'):
            return """**Fibonacci — Java**
```java
public class Fibonacci {
    public static void main(String[] args) {
        int n=10, a=0, b=1;
        System.out.print("Fibonacci: ");
        for(int i=0;i<n;i++){System.out.print(a+" ");int t=a+b;a=b;b=t;}
    }
}
// Output: 0 1 1 2 3 5 8 13 21 34
```"""

        if has('factorial'):
            return """**Factorial — Java**
```java
public class Factorial {
    static long factorial(int n){ return n<=1?1:n*factorial(n-1); }
    public static void main(String[] args) {
        for(int i=1;i<=7;i++) System.out.println(i+"! = "+factorial(i));
    }
}
// 1!=1, 2!=2, 3!=6, 4!=24, 5!=120, 6!=720, 7!=5040
```"""

        if has('prime numbers till','prime till','primes till','prime upto','primes upto',
               'prime up to','primes up to','print prime till','print primes till',
               'prime number till','prime number upto'):
            m = _re.search(r'(\d+)', q)
            n = int(m.group(1)) if m else 50
            return f"""**Prime Numbers Till {n} — Java**

Prime = sirf 1 aur khud se divisible (2, 3, 5, 7 ...)

```java
public class PrimeTillN {{

    // ── Check karo: number prime hai ya nahi ──
    static boolean isPrime(int n) {{
        if (n < 2) return false;              // 0,1 prime nahi hote
        for (int i = 2; i <= Math.sqrt(n); i++) // sqrt tak check karo
            if (n % i == 0) return false;     // divisor mila — not prime
        return true;                          // prime hai!
    }}

    public static void main(String[] args) {{
        int limit = {n};
        System.out.println("Prime numbers till " + limit + ":");
        int count = 0;
        for (int i = 2; i <= limit; i++) {{
            if (isPrime(i)) {{
                System.out.print(i + " ");    // prime print karo
                count++;
            }}
        }}
        System.out.println();
        System.out.println("Total: " + count);
    }}
}}
```"""

        if has('prime number','prime numbers','print prime'):
            return """**Prime Number — Java**

Prime = sirf 1 aur khud se divisible (2, 3, 5, 7 ...)

```java
public class Prime {

    // ── Part 1: Check function ─────────────────────────────
    static boolean isPrime(int n) {
        if (n < 2) return false;              // 0,1 prime nahi hote
        if (n == 2) return true;             // 2 prime hai
        if (n % 2 == 0) return false;         // even = not prime
        for (int i = 3; i <= Math.sqrt(n); i += 2) // sirf odd check
            if (n % i == 0) return false;     // divisor mila
        return true;                          // prime hai!
    }

    public static void main(String[] args) {
        // ── Part 2: Single number check ──
        int num = 37;
        System.out.println(num + " is " + (isPrime(num) ? "PRIME" : "NOT prime"));

        // ── Part 3: 2 se 50 tak saare primes ──
        System.out.print("Primes (2-50): ");
        int count = 0;
        for (int i = 2; i <= 50; i++) {
            if (isPrime(i)) { System.out.print(i + " "); count++; }
        }
        System.out.println("\nTotal: " + count);
        // Output: 2 3 5 7 11 13 17 19 23 29 31 37 41 43 47 — Total: 15
    }
}
```"""

        if has('palindrome'):
            return """**Palindrome — Java**
```java
public class Palindrome {
    static boolean isPalin(String s){
        String r=new StringBuilder(s).reverse().toString();
        return s.equalsIgnoreCase(r);
    }
    static boolean isNumPalin(int n){
        int orig=n,rev=0;
        while(n>0){rev=rev*10+n%10;n/=10;}
        return orig==rev;
    }
    public static void main(String[] args) {
        System.out.println(isPalin("madam"));    // true
        System.out.println(isPalin("hello"));    // false
        System.out.println(isNumPalin(121));     // true
    }
}
```"""

        if has('bubble sort','bubblesort'):
            return """**Bubble Sort — Java**
```java
import java.util.Arrays;
public class BubbleSort {
    static void sort(int[] arr){
        int n=arr.length;
        for(int i=0;i<n-1;i++)
            for(int j=0;j<n-i-1;j++)
                if(arr[j]>arr[j+1]){int t=arr[j];arr[j]=arr[j+1];arr[j+1]=t;}
    }
    public static void main(String[] args){
        int[] arr={64,34,25,12,22,11,90};
        System.out.println("Before: "+Arrays.toString(arr));
        sort(arr);
        System.out.println("After:  "+Arrays.toString(arr));
    }
}
// Before: [64, 34, 25, 12, 22, 11, 90]
// After:  [11, 12, 22, 25, 34, 64, 90]
```"""

        if has('pattern','star','triangle','pyramid'):
            return """**Patterns — Java**
```java
public class Pattern {
    public static void main(String[] args) {
        int n=5;
        System.out.println("Right Triangle:");
        for(int i=1;i<=n;i++){for(int j=0;j<i;j++)System.out.print("* ");System.out.println();}
        System.out.println("\\nPyramid:");
        for(int i=1;i<=n;i++){
            for(int j=i;j<n;j++)System.out.print(" ");
            for(int j=1;j<=2*i-1;j++)System.out.print("*");
            System.out.println();
        }
    }
}
```"""

        if has('class','oop','object','inheritance','interface'):
            return """**OOP — Java**
```java
class Animal {
    String name;
    Animal(String name){ this.name=name; }
    void speak(){ System.out.println(name+" makes a sound"); }
}
class Dog extends Animal {
    Dog(String name){ super(name); }
    @Override
    void speak(){ System.out.println(name+" says: Woof!"); }
}
public class OOPDemo {
    public static void main(String[] args){
        Animal a=new Dog("Tommy");
        a.speak();    // Tommy says: Woof!
    }
}
```"""

        if has('arraylist','array list','collections'):
            return """**ArrayList — Java**
```java
import java.util.*;
public class ArrayListDemo {
    public static void main(String[] args){
        ArrayList<String> list=new ArrayList<>();
        list.add("Alice"); list.add("Bob"); list.add("Charlie");
        list.add(1,"Dave");                       // index pe insert
        System.out.println(list);                 // [Alice, Dave, Bob, Charlie]
        System.out.println("Size: "+list.size()); // 4
        list.remove("Bob");
        Collections.sort(list);
        System.out.println("Sorted: "+list);
    }
}
```"""

        if has('hashmap','hash map','map'):
            return """**HashMap — Java**
```java
import java.util.*;
public class HashMapDemo {
    public static void main(String[] args){
        HashMap<String,Integer> marks=new HashMap<>();
        marks.put("Alice",92); marks.put("Bob",78); marks.put("Charlie",85);
        System.out.println("Alice: "+marks.get("Alice"));  // 92
        marks.put("Alice",97);                              // update
        for(Map.Entry<String,Integer> e:marks.entrySet())
            System.out.println(e.getKey()+" -> "+e.getValue());
        marks.remove("Bob");
    }
}
```"""

        if has('recursion','recursive'):
            return """**Recursion — Java**
```java
public class Recursion {
    static long fact(int n){ return n<=1?1:n*fact(n-1); }
    static long fib(int n){ return n<=1?n:fib(n-1)+fib(n-2); }
    static long pw(int b,int e){ return e==0?1:b*pw(b,e-1); }
    static int gcd(int a,int b){ return b==0?a:gcd(b,a%b); }
    public static void main(String[] args){
        System.out.println("5!="   +fact(5));    // 120
        System.out.println("fib8=" +fib(8));     // 21
        System.out.println("2^10=" +pw(2,10));   // 1024
        System.out.println("gcd="  +gcd(48,18)); // 6
    }
}
```"""

        if has('exception','try catch','error handling'):
            return """**Exception Handling — Java**
```java
public class ExceptionDemo {
    static class AgeException extends Exception {
        AgeException(String m){ super(m); }
    }
    static void setAge(int age) throws AgeException {
        if(age<0||age>150) throw new AgeException("Invalid age: "+age);
        System.out.println("Age: "+age);
    }
    public static void main(String[] args){
        try{
            int[] arr={1,2,3};
            System.out.println(arr[5]);          // throws exception
        }catch(ArrayIndexOutOfBoundsException e){
            System.out.println("Array error: "+e.getMessage());
        }
        try{ setAge(200); }
        catch(AgeException e){ System.out.println(e.getMessage()); }
    }
}
```"""

        if has('vowel','count vowel','vowels in string','vowels in','count vowels','consonant','vowels'):
            return """**Count Vowels in String — Java**
```java
public class VowelCount {
    public static void main(String[] args) {
        String s = "Hello QueryNest";
        String vowels = "aeiouAEIOU";
        int v = 0, con = 0;
        for (char c : s.toCharArray()) {
            if (Character.isLetter(c)) {
                if (vowels.indexOf(c) != -1) v++;
                else con++;
            }
        }
        System.out.println("Vowels:     " + v);    // 5
        System.out.println("Consonants: " + con);  // 9
    }
}
```"""

        if has('reverse string','string reverse','reverse a string','reverse the string'):
            return """**Reverse String — Java**
```java
public class ReverseStr {
    public static void main(String[] args) {
        String s = "QueryNest";
        String rev = new StringBuilder(s).reverse().toString();
        System.out.println("Original: " + s);    // QueryNest
        System.out.println("Reversed: " + rev);  // tseNyreuQ
    }
}
```"""

        if has('string','string method','string function'):
            return """**String Methods — Java**
```java
public class StringDemo {
    public static void main(String[] args){
        String s="Hello QueryNest";
        System.out.println(s.length());           // 15
        System.out.println(s.toUpperCase());      // HELLO QUERYNEST
        System.out.println(s.replace("Hello","Hi")); // Hi QueryNest
        System.out.println(s.contains("Query")); // true
        System.out.println(s.substring(6));       // QueryNest
        System.out.println(s.indexOf("Q"));       // 6
        System.out.println(s.split(" ").length);  // 2
        System.out.println(s.trim());             // no spaces
    }
}
```"""

        if has('harshad','niven'):
            return """**Harshad Number — Java**
```java
public class Harshad {
    static int digitSum(int n) {
        int s = 0;
        while (n > 0) { s += n % 10; n /= 10; }
        return s;
    }
    static boolean isHarshad(int n) { return n % digitSum(n) == 0; }
    public static void main(String[] args) {
        System.out.print("Harshad numbers (1-100): ");
        for (int i = 1; i <= 100; i++)
            if (isHarshad(i)) System.out.print(i + " ");
        // Output: 1 2 3 4 5 6 7 8 9 10 12 18 20 21 24 27 30 36...
    }
}
```"""


        if has('harshad','niven'):
            return """**Harshad Number — Java**
```java
public class Harshad {
    static int digitSum(int n) {
        int s = 0;
        while (n > 0) { s += n % 10; n /= 10; }
        return s;
    }
    static boolean isHarshad(int n) { return n % digitSum(n) == 0; }
    public static void main(String[] args) {
        System.out.print("Harshad numbers (1-100): ");
        for (int i = 1; i <= 100; i++)
            if (isHarshad(i)) System.out.print(i + " ");
        // Output: 1 2 3 4 5 6 7 8 9 10 12 18 20 21 24 27 30 36...
    }
}
```"""

        if has('find integer','integer from list','integer in list','integers in list',
                'find int','int from list','extract integer','filter integer',
                'find number','number from list','numbers in list','find numbers',
                'integer list','list of number','list of integer'):
            return """**Find Integers From a List — Java**
```java
import java.util.*;
import java.util.stream.*;

public class FindIntegers {
    public static void main(String[] args) {

        // Method 1: Mixed Object list — filter only Integer values
        List<Object> mixedList = Arrays.asList(1, "hello", 3, "world", 5, 7, "foo", 9);
        System.out.print("Integers found: ");
        for (Object item : mixedList) {
            if (item instanceof Integer) {          // check if item is int
                System.out.print(item + " ");       // print it
            }
        }
        // Output: Integers found: 1 3 5 7 9

        System.out.println();

        // Method 2: Using Java Streams (Java 8+)
        List<Integer> onlyInts = mixedList.stream()
            .filter(o -> o instanceof Integer)      // keep only integers
            .map(o -> (Integer) o)                  // cast to Integer
            .collect(Collectors.toList());
        System.out.println("List of ints: " + onlyInts);
        // Output: List of ints: [1, 3, 5, 7, 9]

        // Method 3: Find integers in int array matching condition
        int[] nums = {4, 7, 2, 9, 11, 3, 8, 15, 6};
        System.out.print("Integers > 5: ");
        for (int n : nums) {
            if (n > 5) System.out.print(n + " "); // print if greater than 5
        }
        // Output: Integers > 5: 7 9 11 8 15
    }
}
```"""

        if has('array','arrays','int array','array of','sort array','array sort',
                'array search','array element','array program'):
            return """**Array Operations — Java**
```java
import java.util.Arrays;
public class ArrayDemo {
    public static void main(String[] args) {
        int[] arr = {5, 3, 8, 1, 9, 2, 7};         // array declare + initialize

        System.out.println("Original: " + Arrays.toString(arr));

        // Find max and min
        int max = arr[0], min = arr[0];
        for (int n : arr) {
            if (n > max) max = n;                    // update max
            if (n < min) min = n;                    // update min
        }
        System.out.println("Max: " + max);           // 9
        System.out.println("Min: " + min);           // 1

        // Sum and average
        int sum = 0;
        for (int n : arr) sum += n;
        System.out.println("Sum: " + sum);           // 35
        System.out.println("Avg: " + (double)sum/arr.length);  // 5.0

        // Sort the array
        Arrays.sort(arr);
        System.out.println("Sorted: " + Arrays.toString(arr)); // [1,2,3,5,7,8,9]
    }
}
```"""

        # ── Extra built-in answers (variables, if-else, list, etc.) ─
        if _lookup_extra:
            _ex = _lookup_extra(query, 'python')
            if _ex and len(_ex.strip()) > 80:
                return _ex
        return None

    # ══════════════════════════════════════════════════════════════
    # SQL
    # ══════════════════════════════════════════════════════════════
    elif L == 'sql':
        t = query.strip().title()

        if has('student table','students table','student database','create student'):
            return """**Student Table — SQL**
```sql
-- Create student table
CREATE TABLE students (
    id         INTEGER      PRIMARY KEY,
    name       VARCHAR(100) NOT NULL,
    email      VARCHAR(150) UNIQUE,
    age        INTEGER      CHECK (age > 0),
    class      VARCHAR(20),
    marks      DECIMAL(5,2) DEFAULT 0.00,
    created_at DATE         DEFAULT CURRENT_DATE
);

-- Insert sample data
INSERT INTO students (name, email, age, class, marks) VALUES
    ('Alice',   'alice@test.com',   20, '10th', 92.5),
    ('Bob',     'bob@test.com',     21, '11th', 78.0),
    ('Charlie', 'charlie@test.com', 19, '10th', 85.5),
    ('Diana',   'diana@test.com',   22, '12th', 91.0);

-- View all students
SELECT * FROM students;

-- Top students
SELECT name, marks FROM students WHERE marks > 80 ORDER BY marks DESC;

-- Count per class
SELECT class, COUNT(*) total, AVG(marks) avg_marks
FROM students GROUP BY class;
```"""

        if has('employee table','employees table','employee database','create employee'):
            return """**Employee Table — SQL**
```sql
CREATE TABLE employees (
    id         INTEGER      PRIMARY KEY,
    name       VARCHAR(100) NOT NULL,
    email      VARCHAR(150) UNIQUE,
    department VARCHAR(50),
    salary     DECIMAL(10,2),
    hire_date  DATE         DEFAULT CURRENT_DATE,
    is_active  BOOLEAN      DEFAULT TRUE
);

INSERT INTO employees (name, email, department, salary) VALUES
    ('Alice',   'alice@co.com',   'Engineering', 75000),
    ('Bob',     'bob@co.com',     'Marketing',   55000),
    ('Charlie', 'charlie@co.com', 'Engineering', 82000),
    ('Diana',   'diana@co.com',   'HR',          48000);

-- Queries
SELECT * FROM employees ORDER BY salary DESC;
SELECT department, COUNT(*) headcount, AVG(salary) avg_salary
FROM employees GROUP BY department;
SELECT name, salary FROM employees WHERE salary > 60000;
```"""

        if has('create table','create a table'):
            tbl = _re.search(r'create\s+(?:a\s+)?table\s+(?:for\s+)?(\w+)', q)
            tname = tbl.group(1) if tbl else 'students'
            return f"""**CREATE TABLE — SQL**
```sql
CREATE TABLE {tname} (
    id         INTEGER      PRIMARY KEY,
    name       VARCHAR(100) NOT NULL,
    email      VARCHAR(150) UNIQUE,
    age        INTEGER,
    created_at DATE         DEFAULT CURRENT_DATE
);
INSERT INTO {tname} (name,email,age) VALUES
    ('Alice','alice@test.com',20),
    ('Bob',  'bob@test.com',  21);
SELECT * FROM {tname};
```"""

        if has('select','fetch','retrieve','show all','display all'):
            return """**SELECT Queries — SQL**
```sql
-- All rows
SELECT * FROM students;

-- Specific columns with condition
SELECT name, marks FROM students WHERE marks > 80;

-- Sort and limit
SELECT * FROM students ORDER BY marks DESC LIMIT 5;

-- COUNT, AVG, MAX
SELECT COUNT(*) total, AVG(marks) avg, MAX(marks) highest FROM students;

-- GROUP BY
SELECT class, COUNT(*) students, ROUND(AVG(marks),2) avg
FROM students GROUP BY class HAVING AVG(marks) > 70;
```"""

        if has('insert','add data','insert into'):
            return """**INSERT — SQL**
```sql
-- Single row
INSERT INTO students (name, age, marks) VALUES ('Alice', 20, 92.5);

-- Multiple rows
INSERT INTO students (name, age, marks) VALUES
    ('Bob',     21, 78.0),
    ('Charlie', 19, 85.5),
    ('Diana',   20, 91.0);

SELECT * FROM students;
```"""

        if has('update','modify','change'):
            return """**UPDATE — SQL**
```sql
-- Single row update
UPDATE students SET marks = 95 WHERE name = 'Alice';

-- Multiple columns
UPDATE students SET marks = 98, class = '12th' WHERE id = 1;

-- Increment
UPDATE students SET marks = marks + 5 WHERE marks < 50;

-- Verify
SELECT * FROM students WHERE id = 1;
```"""

        if has('delete','remove','drop'):
            return """**DELETE — SQL**
```sql
-- Delete specific row
DELETE FROM students WHERE id = 1;

-- Delete with condition
DELETE FROM students WHERE marks < 33;

-- Delete all rows (table remains)
DELETE FROM students;

-- Drop entire table
DROP TABLE IF EXISTS students;
```"""

        if has('join','inner join','left join','right join','join query','select join','sql join','table join','with join'):
            return """**JOINs — SQL**
```sql
-- INNER JOIN: only matching rows
SELECT s.name, c.course_name
FROM students s
INNER JOIN courses c ON s.class = c.class;

-- LEFT JOIN: all students even unenrolled
SELECT s.name, c.course_name
FROM students s
LEFT JOIN courses c ON s.class = c.class;

-- Self JOIN: employee-manager
SELECT e.name employee, m.name manager
FROM employees e LEFT JOIN employees m ON e.manager_id = m.id;
```"""

        if has('group by','aggregate','count','sum','avg'):
            return """**GROUP BY & Aggregates — SQL**
```sql
-- Count per group
SELECT class, COUNT(*) total FROM students GROUP BY class;

-- Multiple aggregates
SELECT class,
    COUNT(*)          AS students,
    ROUND(AVG(marks),2) AS avg_marks,
    MAX(marks)        AS highest,
    MIN(marks)        AS lowest
FROM students
GROUP BY class
HAVING AVG(marks) > 70
ORDER BY avg_marks DESC;
```"""

        if has('subquery','sub query','nested query'):
            return """**Subquery — SQL**
```sql
-- WHERE subquery
SELECT name, marks FROM students
WHERE marks > (SELECT AVG(marks) FROM students);

-- IN subquery
SELECT name FROM students
WHERE id IN (SELECT student_id FROM enrollments WHERE course_id = 3);

-- EXISTS
SELECT name FROM students s
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.student_id = s.id);
```"""

        if has('index','create index'):
            return """**Indexes — SQL**
```sql
-- Single column index
CREATE INDEX idx_marks ON students(marks);

-- Unique index
CREATE UNIQUE INDEX idx_email ON students(email);

-- Composite index
CREATE INDEX idx_class_marks ON students(class, marks);

-- Check if used
EXPLAIN SELECT * FROM students WHERE marks > 80;

-- Remove index
DROP INDEX idx_marks;
```"""

        if has('view','create view'):
            return """**Views — SQL**
```sql
-- Create view
CREATE VIEW top_students AS
SELECT name, class, marks
FROM students
WHERE marks >= 85
ORDER BY marks DESC;

-- Use view
SELECT * FROM top_students;
SELECT * FROM top_students WHERE class = '10th';

-- Drop view
DROP VIEW IF EXISTS top_students;
```"""

        if has('transaction','commit','rollback'):
            return """**Transactions — SQL**
```sql
-- Transfer money example
BEGIN;
    UPDATE accounts SET balance = balance - 500 WHERE id = 1;
    UPDATE accounts SET balance = balance + 500 WHERE id = 2;
COMMIT;

-- Rollback on error
BEGIN;
    DELETE FROM orders WHERE id = 99;
ROLLBACK;  -- undo karo

-- Savepoint
BEGIN;
    INSERT INTO logs VALUES ('action1');
    SAVEPOINT sp1;
    INSERT INTO logs VALUES ('action2');  -- ye fail ho
    ROLLBACK TO sp1;                       -- sp1 pe wapas
COMMIT;
```"""


        # ── Programming/pattern questions → delegate to Python ──────
        # Users on this tab sometimes ask programming questions
        # (isosceles triangle, fibonacci, pattern, etc.)
        _PROG_KW = [
            'isosceles','equilateral','scalene','triangle','pattern','star',
            'pyramid','diamond','fibonacci','fibo','factorial','prime',
            'palindrome','armstrong','bubble sort','selection sort',
            'insertion sort','binary search','linear search','linked list',
            'stack','queue','recursion','swap','reverse','anagram',
            'happy number','perfect number','harshad','gcd','lcm',
            'even number','odd number','vowel','consonant','digit',
            'matrix','calculator','oop','inheritance','sorting','searching',
            'number series','whole number','natural number','number pattern',
            'print series','count','sum of',
        ]
        if any(kw in q for kw in _PROG_KW):
            _py = generate_smart_answer(query, 'python')
            if _py and len(_py.strip()) > 80:
                return _py
        # ── Extra built-in answers (variables, if-else, list, etc.) ─
        if _lookup_extra:
            _ex = _lookup_extra(query, 'python')
            if _ex and len(_ex.strip()) > 80:
                return _ex
        return None

    # ══════════════════════════════════════════════════════════════
    # MySQL
    # ══════════════════════════════════════════════════════════════
    elif L == 'mysql':
        t = query.strip().title()

        if has('student table','students table','student database','create student'):
            return """**Student Table — MySQL**
```sql
CREATE TABLE students (
    id         INT          AUTO_INCREMENT PRIMARY KEY,
    name       VARCHAR(100) NOT NULL,
    email      VARCHAR(150) UNIQUE,
    age        INT          CHECK (age > 0),
    class      VARCHAR(20),
    marks      DECIMAL(5,2) DEFAULT 0.00,
    created_at TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO students (name, email, age, class, marks) VALUES
    ('Alice',   'alice@test.com',   20, '10th', 92.5),
    ('Bob',     'bob@test.com',     21, '11th', 78.0),
    ('Charlie', 'charlie@test.com', 19, '10th', 85.5),
    ('Diana',   'diana@test.com',   22, '12th', 91.0);

SELECT * FROM students;
SELECT name, marks FROM students WHERE marks > 80 ORDER BY marks DESC;
SELECT class, COUNT(*) total, AVG(marks) avg_marks FROM students GROUP BY class;
DESCRIBE students;
```"""

        if has('employee table','employees table','employee database','create employee'):
            return """**Employee Table — MySQL**
```sql
CREATE TABLE employees (
    id         INT           AUTO_INCREMENT PRIMARY KEY,
    name       VARCHAR(100)  NOT NULL,
    email      VARCHAR(150)  UNIQUE,
    department VARCHAR(50),
    salary     DECIMAL(10,2),
    hire_date  TIMESTAMP     DEFAULT CURRENT_TIMESTAMP,
    is_active  TINYINT(1)    DEFAULT 1
);

INSERT INTO employees (name, email, department, salary) VALUES
    ('Alice',   'alice@co.com',   'Engineering', 75000),
    ('Bob',     'bob@co.com',     'Marketing',   55000),
    ('Charlie', 'charlie@co.com', 'Engineering', 82000);

SELECT * FROM employees ORDER BY salary DESC;
SELECT department, COUNT(*) headcount, AVG(salary) avg_salary
FROM employees GROUP BY department;
```"""

        if has('create table','create a table'):
            tbl = _re.search(r'create\s+(?:a\s+)?table\s+(?:for\s+)?(\w+)', q)
            tname = tbl.group(1) if tbl else 'students'
            return f"""**CREATE TABLE — MySQL**
```sql
CREATE TABLE {tname} (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    name       VARCHAR(100) NOT NULL,
    email      VARCHAR(150) UNIQUE,
    age        INT          CHECK (age >= 0),
    marks      DECIMAL(5,2) DEFAULT 0.00,
    status     ENUM('active','inactive') DEFAULT 'active',
    created_at TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
);
INSERT INTO {tname} (name,email,age,marks) VALUES
    ('Alice','alice@test.com',20,92.5),
    ('Bob',  'bob@test.com',  21,78.0);
SELECT * FROM {tname};
DESCRIBE {tname};
```"""

        if has('select','fetch','retrieve','show all','group by','aggregate','count','sum','avg'):
            return """**SELECT — MySQL**
```sql
SELECT * FROM students;
SELECT name, marks FROM students WHERE marks > 80;
SELECT * FROM students WHERE age BETWEEN 18 AND 25;
SELECT * FROM students WHERE name LIKE 'A%';
SELECT * FROM students ORDER BY marks DESC LIMIT 5;
SELECT DISTINCT class FROM students;

-- Aggregate
SELECT class, COUNT(*) n, ROUND(AVG(marks),2) avg
FROM students GROUP BY class HAVING avg > 70 ORDER BY avg DESC;
```"""

        if has('join','inner join','left join'):
            return """**JOINs — MySQL**
```sql
-- INNER JOIN
SELECT s.name, c.course_name
FROM students s INNER JOIN courses c ON s.class = c.class;

-- LEFT JOIN
SELECT s.name, c.course_name
FROM students s LEFT JOIN courses c ON s.class = c.class;

-- Self JOIN (manager-employee)
SELECT e.name employee, m.name manager
FROM employees e LEFT JOIN employees m ON e.manager_id = m.id;
```"""

        if has('stored procedure','procedure'):
            return """**Stored Procedure — MySQL**
```sql
DELIMITER //
CREATE PROCEDURE GetTopStudents(IN min_marks DECIMAL)
BEGIN
    SELECT name, class, marks
    FROM students
    WHERE marks >= min_marks
    ORDER BY marks DESC;
END //
DELIMITER ;

-- Call
CALL GetTopStudents(85);
```"""

        if has('trigger'):
            return """**Trigger — MySQL**
```sql
CREATE TABLE student_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_name VARCHAR(100),
    action VARCHAR(20),
    log_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

DELIMITER //
CREATE TRIGGER after_insert_student
AFTER INSERT ON students
FOR EACH ROW
BEGIN
    INSERT INTO student_log(student_name, action)
    VALUES (NEW.name, 'INSERTED');
END //
DELIMITER ;
```"""

        if has('index'):
            return """**Indexes — MySQL**
```sql
CREATE INDEX idx_marks ON students(marks);
CREATE UNIQUE INDEX idx_email ON students(email);
CREATE INDEX idx_composite ON students(class, marks);
CREATE FULLTEXT INDEX ft_name ON students(name);

SHOW INDEX FROM students;
EXPLAIN SELECT * FROM students WHERE marks > 80;
DROP INDEX idx_marks ON students;
```"""


        # ── Programming/pattern questions → delegate to Python ──────
        # Users on this tab sometimes ask programming questions
        # (isosceles triangle, fibonacci, pattern, etc.)
        _PROG_KW = [
            'isosceles','equilateral','scalene','triangle','pattern','star',
            'pyramid','diamond','fibonacci','fibo','factorial','prime',
            'palindrome','armstrong','bubble sort','selection sort',
            'insertion sort','binary search','linear search','linked list',
            'stack','queue','recursion','swap','reverse','anagram',
            'happy number','perfect number','harshad','gcd','lcm',
            'even number','odd number','vowel','consonant','digit',
            'matrix','calculator','oop','inheritance','sorting','searching',
            'number series','whole number','natural number','number pattern',
            'print series','count','sum of',
        ]
        if any(kw in q for kw in _PROG_KW):
            _py = generate_smart_answer(query, 'python')
            if _py and len(_py.strip()) > 80:
                return _py
        return None

    # ══════════════════════════════════════════════════════════════
    # MongoDB
    # ══════════════════════════════════════════════════════════════
    elif L == 'mongodb':
        t = query.strip().title()

        if has('insert','insertone','insertmany','add document','create document'):
            return """**Insert Documents — MongoDB**
```javascript
// insertOne
db.students.insertOne({
    name:      "Alice",
    age:       20,
    class:     "10th",
    marks:     92.5,
    subjects:  ["Math","Physics"],
    createdAt: new Date()
})

// insertMany
db.students.insertMany([
    { name:"Bob",     age:21, marks:78.0 },
    { name:"Charlie", age:19, marks:85.5 },
    { name:"Diana",   age:20, marks:91.0 }
])
// Returns: { acknowledged:true, insertedCount:3 }
```"""

        if has('find','select','query','fetch','retrieve','show all'):
            return """**Find / Query — MongoDB**
```javascript
db.students.find()                              // all documents
db.students.find({ class:"10th" })             // filter
db.students.find({ marks:{ $gt:80 } })         // marks > 80
db.students.find({ $or:[{marks:{$gt:90}},{age:{$lt:20}}] }) // OR

// Projection (show only name & marks)
db.students.find({ marks:{$gt:80} }, { name:1, marks:1, _id:0 })

// Sort, limit, skip
db.students.find().sort({ marks:-1 }).limit(5) // top 5
db.students.findOne({ name:"Alice" })           // single doc
db.students.countDocuments({ class:"10th" })    // count
```"""

        if has('update','updateone','updatemany','modify','change'):
            return """**Update — MongoDB**
```javascript
// updateOne
db.students.updateOne(
    { name:"Alice" },
    { $set:{ marks:97, grade:"A+" } }
)

// Increment
db.students.updateOne({ name:"Bob" }, { $inc:{ marks:5 } })

// updateMany
db.students.updateMany(
    { marks:{ $lt:50 } },
    { $set:{ status:"fail" } }
)

// Push to array
db.students.updateOne({ name:"Alice" }, { $push:{ subjects:"Chemistry" } })

// Upsert (insert if not found)
db.students.updateOne(
    { email:"new@test.com" },
    { $set:{ name:"New", age:25 } },
    { upsert:true }
)
```"""

        if has('delete','deleteone','deletemany','remove','drop'):
            return """**Delete — MongoDB**
```javascript
db.students.deleteOne({ name:"Alice" })         // single
db.students.deleteMany({ marks:{ $lt:33 } })    // condition
db.students.deleteMany({})                       // ALL docs
db.students.drop()                               // drop collection
db.dropDatabase()                                // drop database
```"""

        if has('aggregate','group','pipeline','count group','avg group'):
            return """**Aggregation Pipeline — MongoDB**
```javascript
// Group & count
db.students.aggregate([
    { $group:{
        _id:     "$class",
        count:   { $sum:1 },
        avg:     { $avg:"$marks" },
        highest: { $max:"$marks" }
    }},
    { $sort:{ avg:-1 } }
])

// Filter → Project → Sort
db.students.aggregate([
    { $match:  { marks:{ $gte:60 } } },
    { $project:{ name:1, marks:1,
        grade:{ $cond:[{ $gte:["$marks",90] },"A","B"] }
    }},
    { $sort:{ marks:-1 } },
    { $limit:10 }
])
```"""

        if has('lookup','join'):
            return """**$lookup (JOIN) — MongoDB**
```javascript
db.orders.aggregate([
    { $lookup:{
        from:         "users",
        localField:   "user_id",
        foreignField: "_id",
        as:           "user_info"
    }},
    { $unwind:"$user_info" },
    { $project:{
        order_id:1, amount:1,
        "user_info.name":1,
        "user_info.email":1
    }}
])
```"""

        if has('index','createindex','create index'):
            return """**Indexes — MongoDB**
```javascript
db.students.createIndex({ email:1 })                    // single
db.students.createIndex({ email:1 },{ unique:true })    // unique
db.students.createIndex({ class:1, marks:-1 })          // compound
db.students.createIndex({ name:"text" })                // text search

db.students.find({ $text:{ $search:"Alice" } })         // text search
db.students.getIndexes()                                 // list all
db.students.dropIndex({ email:1 })                      // remove
```"""

        if has('create collection','new collection'):
            return """**Create Collection — MongoDB**
```javascript
// Method 1: Explicit
db.createCollection("students")

// Method 2: With validation
db.createCollection("orders", {
    validator:{ $jsonSchema:{
        bsonType:"object",
        required:["name","amount"]
    }}
})

// Method 3: Auto-create on insert
db.students.insertOne({ name:"Alice", age:20 })

show collections    // verify
```"""

        # ── MySQL: programming/pattern topics — delegate to Python ──
        # Users on MySQL tab sometimes ask general programming questions
        # (isosceles triangle, fibonacci, pattern, etc.) — answer in Python
        PROG_TOPICS = [
            'isosceles','equilateral','scalene','triangle','pattern','star',
            'pyramid','diamond','fibonacci','factorial','prime','palindrome',
            'armstrong','bubble sort','selection sort','insertion sort',
            'binary search','linear search','linked list','stack','queue',
            'recursion','swap','reverse','anagram','happy number','perfect',
            'harshad','gcd','lcm','even','odd','vowel','consonant','digit',
            'matrix','calculator','class','oop','inheritance','array','string',
        ]
        if any(kw in q for kw in PROG_TOPICS):
            # Re-run with Python so the user gets a working answer
            result = generate_smart_answer(query, 'python')
            if result:
                return result
            # If Python doesn't cover it either, build a specific answer
            topic = query.strip().title()
            if has('isosceles'):
                return r"""**Isosceles Triangle Pattern — Python**
```python
n = 5                           # rows
for i in range(1, n + 1):
    spaces = ' ' * (n - i)      # left padding
    stars  = '* ' * i           # stars for this row
    print(spaces + stars)

# Output:
#     *
#    * *
#   * * *
#  * * * *
# * * * * *
```"""
            if has('equilateral'):
                return r"""**Equilateral Triangle Pattern — Python**
```python
n = 5                           # rows
for i in range(1, n + 1):
    spaces = ' ' * (n - i)
    stars  = '*' * (2 * i - 1)  # 1, 3, 5, 7, 9 stars
    print(spaces + stars)

# Output:
#     *
#    ***
#   *****
#  *******
# *********
```"""
            if has('scalene'):
                return r"""**Scalene / Right Triangle Pattern — Python**
```python
n = 5                           # rows
for i in range(1, n + 1):
    print('* ' * i)             # increasing stars

# Output:
# *
# * *
# * * *
# * * * *
# * * * * *
```"""


        # ── Programming/pattern questions → delegate to Python ──────
        # Users on this tab sometimes ask programming questions
        # (isosceles triangle, fibonacci, pattern, etc.)
        _PROG_KW = [
            'isosceles','equilateral','scalene','triangle','pattern','star',
            'pyramid','diamond','fibonacci','fibo','factorial','prime',
            'palindrome','armstrong','bubble sort','selection sort',
            'insertion sort','binary search','linear search','linked list',
            'stack','queue','recursion','swap','reverse','anagram',
            'happy number','perfect number','harshad','gcd','lcm',
            'even number','odd number','vowel','consonant','digit',
            'matrix','calculator','oop','inheritance','sorting','searching',
            'number series','whole number','natural number','number pattern',
            'print series','count','sum of',
        ]
        if any(kw in q for kw in _PROG_KW):
            _py = generate_smart_answer(query, 'python')
            if _py and len(_py.strip()) > 80:
                return _py
        # ── Extra built-in answers (variables, if-else, list, etc.) ─
        if _lookup_extra:
            _ex = _lookup_extra(query, 'python')
            if _ex and len(_ex.strip()) > 80:
                return _ex
        return None

    # ── Check extra answers (handles general Python topics) ────────
    if _lookup_extra:
        extra = _lookup_extra(query, L)
        if extra and len(extra.strip()) > 80:
            return extra

    # ── Last resort — return None so real AI gets called ─────────
    return None
