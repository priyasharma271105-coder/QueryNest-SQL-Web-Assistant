"""
QueryNest — MongoDB Seed Script
================================
Yeh script saari JSON saved queries MongoDB mein insert karti hai.

Run karo:
    python seed_mongodb.py

Conditions:
- Duplicate titles skip ho jaate hain (upsert)
- Existing data safe rehta hai
"""

import json, glob, os, sys
from pymongo import MongoClient

# ── Config ────────────────────────────────────────────────────────
MONGO_URI  = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/')
DB_NAME    = 'QueryNest'
COLLECTION = 'solutions'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_DIR = os.path.join(BASE_DIR, 'data', 'saved_queries')

# ── Extra topics not in JSON files ────────────────────────────────
EXTRA_ENTRIES = [
    # ── Python string operations ──────────────────────────────────
    {
        "title": "Python Vowels in String",
        "language": "python",
        "tags": ["vowels", "string", "count", "python", "characters"],
        "content": """# Count vowels in a string — Python
s = input("Enter a string: ")   # e.g. "Hello World"

vowels = "aeiouAEIOU"           # all vowels upper+lower

# Method 1 — for loop
count = 0
for ch in s:                    # iterate each character
    if ch in vowels:            # check if it's a vowel
        count += 1
print("Vowels:", count)         # Vowels: 3

# Method 2 — list comprehension (one line)
v_list = [ch for ch in s if ch in vowels]
print("Vowel chars:", v_list)   # ['e', 'o', 'o']

# Method 3 — count specific vowels
for v in "aeiou":
    print(f"'{v}' appears {s.lower().count(v)} times")

# Output (for "Hello World"):
# Vowels: 3
# Vowel chars: ['e', 'o', 'o']"""
    },
    {
        "title": "Python String Operations",
        "language": "python",
        "tags": ["string", "upper", "lower", "replace", "split", "python"],
        "content": """# String operations — Python
s = "Hello World"

print(s.upper())           # HELLO WORLD
print(s.lower())           # hello world
print(s.replace("World", "Python"))  # Hello Python
print(s.split(" "))        # ['Hello', 'World']
print(s.strip())           # removes leading/trailing spaces
print(len(s))              # 11
print(s[0])                # H  — first char
print(s[-1])               # d  — last char
print(s[0:5])              # Hello — slicing
print(s.count("l"))        # 3 — count occurrences
print(s.find("World"))     # 6 — index where found
print("World" in s)        # True — membership check
print(s.startswith("Hello"))  # True
print(s.endswith("World"))    # True
print(",".join(["a","b","c"]))  # a,b,c
print(s.title())           # Hello World (Title Case)"""
    },
    {
        "title": "Python Palindrome String",
        "language": "python",
        "tags": ["palindrome", "string", "reverse", "python"],
        "content": """# Check if string is palindrome — Python
s = input("Enter string: ").lower().strip()

# Method 1 — reverse compare
if s == s[::-1]:            # [::-1] reverses the string
    print(f"'{s}' is a Palindrome")
else:
    print(f"'{s}' is NOT a Palindrome")

# Method 2 — loop
def is_palindrome(st):
    st = st.lower()
    for i in range(len(st) // 2):
        if st[i] != st[-(i+1)]:    # compare from both ends
            return False
    return True

print(is_palindrome("madam"))   # True
print(is_palindrome("hello"))   # False
# Output: 'madam' is a Palindrome"""
    },
    {
        "title": "Python Count Characters in String",
        "language": "python",
        "tags": ["count", "characters", "string", "frequency", "python"],
        "content": """# Count characters / frequency in string — Python
s = "programming"

# Count each character
freq = {}
for ch in s:
    freq[ch] = freq.get(ch, 0) + 1   # increment count
print(freq)   # {'p':1, 'r':2, 'o':1, 'g':2, ...}

# Using collections.Counter (easier)
from collections import Counter
c = Counter(s)
print(c.most_common(3))   # top 3 most frequent chars

# Count only letters (ignore spaces/punctuation)
letters = [ch for ch in s if ch.isalpha()]
print("Letters:", len(letters))

# Count spaces
spaces = s.count(" ")
print("Spaces:", spaces)"""
    },
    # ── C programs ───────────────────────────────────────────────
    {
        "title": "C Vowels in String",
        "language": "c",
        "tags": ["vowels", "string", "count", "c", "characters"],
        "content": """/* Count vowels in string — C */
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int main() {
    char s[100];
    printf("Enter string: ");
    gets(s);                        /* read full line */

    int vowels = 0, consonants = 0;
    for (int i = 0; s[i] != '\\0'; i++) {
        char ch = tolower(s[i]);    /* convert to lowercase */
        if (ch >= 'a' && ch <= 'z') {
            if (ch=='a'||ch=='e'||ch=='i'||ch=='o'||ch=='u')
                vowels++;           /* it's a vowel */
            else
                consonants++;       /* it's a consonant */
        }
    }
    printf("Vowels: %d\\n", vowels);
    printf("Consonants: %d\\n", consonants);
    return 0;
    /* Output: Vowels: 3, Consonants: 7 (for "Hello World") */
}"""
    },
    {
        "title": "C String Reverse",
        "language": "c",
        "tags": ["reverse", "string", "c", "array"],
        "content": """/* Reverse a string — C */
#include <stdio.h>
#include <string.h>

int main() {
    char s[100], rev[100];
    printf("Enter string: ");
    gets(s);

    int n = strlen(s);              /* length of string */
    for (int i = 0; i < n; i++) {
        rev[i] = s[n - 1 - i];     /* copy in reverse order */
    }
    rev[n] = '\\0';                  /* null terminate */
    printf("Reversed: %s\\n", rev);  /* Output: dlroW olleH */

    /* Check palindrome */
    if (strcmp(s, rev) == 0)
        printf("Palindrome\\n");
    else
        printf("Not Palindrome\\n");
    return 0;
}"""
    },
    # ── Java programs ────────────────────────────────────────────
    {
        "title": "Java Vowels in String",
        "language": "java",
        "tags": ["vowels", "string", "count", "java", "characters"],
        "content": """// Count vowels in String — Java
import java.util.Scanner;

public class VowelCount {
    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        System.out.print("Enter string: ");
        String s = sc.nextLine().toLowerCase();   // convert to lowercase

        int vowels = 0, consonants = 0;
        String vowelChars = "aeiou";

        for (int i = 0; i < s.length(); i++) {
            char ch = s.charAt(i);                // get each character
            if (Character.isLetter(ch)) {         // only count letters
                if (vowelChars.indexOf(ch) != -1)
                    vowels++;                     // found in vowel list
                else
                    consonants++;
            }
        }
        System.out.println("Vowels: " + vowels);
        System.out.println("Consonants: " + consonants);
        // Output: Vowels: 3  Consonants: 7
    }
}"""
    },
    {
        "title": "Java String Reverse and Palindrome",
        "language": "java",
        "tags": ["reverse", "palindrome", "string", "java"],
        "content": """// Reverse string and check palindrome — Java
public class StringReverse {
    public static void main(String[] args) {
        String s = "madam";

        // Method 1 — StringBuilder
        String rev = new StringBuilder(s).reverse().toString();
        System.out.println("Reversed: " + rev);  // madam

        // Method 2 — manual loop
        String rev2 = "";
        for (int i = s.length()-1; i >= 0; i--)
            rev2 += s.charAt(i);
        System.out.println("Reversed: " + rev2);

        // Palindrome check
        if (s.equals(rev))
            System.out.println(s + " is Palindrome");
        else
            System.out.println(s + " is NOT Palindrome");
        // Output: Reversed: madam  →  madam is Palindrome
    }
}"""
    },
    # ── C++ programs ─────────────────────────────────────────────
    {
        "title": "C++ Vowels in String",
        "language": "cpp",
        "tags": ["vowels", "string", "count", "cpp", "c++", "characters"],
        "content": """// Count vowels in string — C++
#include <iostream>
#include <string>
#include <cctype>
using namespace std;

int main() {
    string s;
    cout << "Enter string: ";
    getline(cin, s);              // read full line

    int vowels = 0, consonants = 0;
    string v = "aeiouAEIOU";

    for (char ch : s) {           // range-based for loop
        if (isalpha(ch)) {        // only count letters
            if (v.find(ch) != string::npos)
                vowels++;         // found in vowels string
            else
                consonants++;
        }
    }
    cout << "Vowels: " << vowels << endl;
    cout << "Consonants: " << consonants << endl;
    // Output: Vowels: 3  Consonants: 7
    return 0;
}"""
    },
    {
        "title": "C++ String Reverse Palindrome",
        "language": "cpp",
        "tags": ["reverse", "palindrome", "string", "cpp", "c++"],
        "content": """// Reverse string and palindrome check — C++
#include <iostream>
#include <string>
#include <algorithm>
using namespace std;

int main() {
    string s;
    cout << "Enter string: ";
    cin >> s;

    string rev = s;
    reverse(rev.begin(), rev.end());  // STL reverse
    cout << "Reversed: " << rev << endl;

    if (s == rev)
        cout << s << " is Palindrome" << endl;
    else
        cout << s << " is NOT Palindrome" << endl;
    // Output: Reversed: madam → madam is Palindrome
    return 0;
}"""
    },
    # ── MySQL extra ───────────────────────────────────────────────
    {
        "title": "MySQL Create Table Library",
        "language": "mysql",
        "tags": ["create", "table", "library", "mysql", "books"],
        "content": """-- Library management table — MySQL
CREATE TABLE books (
    id          INT AUTO_INCREMENT PRIMARY KEY,  -- unique book id
    title       VARCHAR(200) NOT NULL,           -- book title
    author      VARCHAR(100) NOT NULL,           -- author name
    isbn        VARCHAR(20) UNIQUE,              -- unique isbn
    genre       VARCHAR(50),                     -- fiction/non-fiction etc
    price       DECIMAL(8,2) DEFAULT 0.00,       -- book price
    quantity    INT DEFAULT 0,                   -- copies available
    added_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE members (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    email       VARCHAR(150) UNIQUE NOT NULL,
    phone       VARCHAR(15),
    joined_at   DATE DEFAULT (CURRENT_DATE)
);

CREATE TABLE issues (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    book_id     INT,
    member_id   INT,
    issue_date  DATE NOT NULL,
    due_date    DATE NOT NULL,
    return_date DATE,
    FOREIGN KEY (book_id)   REFERENCES books(id),
    FOREIGN KEY (member_id) REFERENCES members(id)
);

DESCRIBE books;   -- view table structure"""},
    {
        "title": "MySQL Create Table Canteen",
        "language": "mysql",
        "tags": ["create", "table", "canteen", "mysql", "food", "menu"],
        "content": """-- Canteen management system — MySQL
CREATE TABLE menu_items (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    item_name   VARCHAR(100) NOT NULL,           -- food item name
    category    ENUM('breakfast','lunch','snack','beverage') NOT NULL,
    price       DECIMAL(6,2) NOT NULL,           -- item price
    is_veg      BOOLEAN DEFAULT TRUE,            -- veg or non-veg
    available   BOOLEAN DEFAULT TRUE,            -- in stock?
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE orders (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    item_id     INT NOT NULL,
    student_id  INT NOT NULL,
    quantity    INT DEFAULT 1,
    total_price DECIMAL(8,2),
    ordered_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (item_id) REFERENCES menu_items(id)
);

-- Insert sample data
INSERT INTO menu_items (item_name, category, price, is_veg)
VALUES
    ('Vada Pav',   'snack',     15.00, TRUE),
    ('Samosa',     'snack',     10.00, TRUE),
    ('Chai',       'beverage',   8.00, TRUE),
    ('Thali',      'lunch',     60.00, TRUE);

SELECT * FROM menu_items WHERE available = TRUE;
SELECT * FROM menu_items WHERE price < 20 ORDER BY price ASC;"""},
    {
        "title": "MySQL Create Table Hospital",
        "language": "mysql",
        "tags": ["create", "table", "hospital", "mysql", "patients", "doctors"],
        "content": """-- Hospital management system — MySQL
CREATE TABLE doctors (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    specialization VARCHAR(100),
    phone       VARCHAR(15),
    email       VARCHAR(150) UNIQUE
);

CREATE TABLE patients (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    age         INT CHECK (age > 0),
    gender      ENUM('M','F','Other'),
    blood_group VARCHAR(5),
    phone       VARCHAR(15),
    admitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE appointments (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    patient_id  INT NOT NULL,
    doctor_id   INT NOT NULL,
    appt_date   DATETIME NOT NULL,
    reason      TEXT,
    status      ENUM('scheduled','completed','cancelled') DEFAULT 'scheduled',
    FOREIGN KEY (patient_id) REFERENCES patients(id),
    FOREIGN KEY (doctor_id)  REFERENCES doctors(id)
);

SELECT p.name, d.name AS doctor, a.appt_date
FROM appointments a
JOIN patients p ON a.patient_id = p.id
JOIN doctors  d ON a.doctor_id  = d.id
WHERE a.status = 'scheduled';"""},
    # ── SQL ────────────────────────────────────────────────────────
    {
        "title": "SQL String Functions",
        "language": "sql",
        "tags": ["string", "functions", "upper", "lower", "length", "sql"],
        "content": """-- SQL String functions
SELECT UPPER('hello world');          -- HELLO WORLD
SELECT LOWER('HELLO WORLD');          -- hello world
SELECT LENGTH('QueryNest');           -- 9
SELECT SUBSTRING('QueryNest', 1, 5);  -- Query (1-based index)
SELECT TRIM('  hello  ');             -- 'hello'
SELECT REPLACE('hello world', 'world', 'SQL');  -- hello SQL
SELECT CONCAT('Hello', ' ', 'World');  -- Hello World
SELECT INSTR('QueryNest', 'Nest');    -- 6 (position of 'Nest')
SELECT LEFT('QueryNest', 5);          -- Query
SELECT RIGHT('QueryNest', 4);         -- Nest
SELECT LPAD('42', 5, '0');            -- 00042 (pad with zeros)
SELECT REVERSE('hello');              -- olleh

-- Practical example: format names
SELECT
    UPPER(SUBSTRING(name, 1, 1))       -- first letter uppercase
    CONCAT(LOWER(SUBSTRING(name, 2)))  -- rest lowercase
FROM students;"""},
]

def seed():
    print(f"🔌 Connecting to MongoDB at {MONGO_URI}...")
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        db  = client[DB_NAME]
        col = db[COLLECTION]
        print(f"✅ Connected → DB: '{DB_NAME}' | Collection: '{COLLECTION}'")
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        print("   Make sure mongod is running: mongod --dbpath /data/db")
        sys.exit(1)

    total_inserted = 0
    total_skipped  = 0

    # ── Load from JSON files ───────────────────────────────────────
    json_files = glob.glob(os.path.join(JSON_DIR, '*.json'))
    print(f"\n📂 Found {len(json_files)} JSON files in {JSON_DIR}")

    for jfile in json_files:
        try:
            with open(jfile, 'r', encoding='utf-8') as f:
                entries = json.load(f)
            if not isinstance(entries, list):
                entries = [entries]

            fname = os.path.basename(jfile)
            ins = skp = 0
            for entry in entries:
                if not isinstance(entry, dict) or not entry.get('title'):
                    continue
                # Upsert by title — safe, no duplicates
                result = col.update_one(
                    {'title': entry['title']},
                    {'$setOnInsert': entry},
                    upsert=True
                )
                if result.upserted_id:
                    ins += 1
                else:
                    skp += 1

            print(f"  ✅ {fname}: {ins} inserted, {skp} already existed")
            total_inserted += ins
            total_skipped  += skp
        except Exception as e:
            print(f"  ❌ Error reading {jfile}: {e}")

    # ── Insert extra entries ───────────────────────────────────────
    print(f"\n➕ Inserting {len(EXTRA_ENTRIES)} extra topic entries...")
    for entry in EXTRA_ENTRIES:
        result = col.update_one(
            {'title': entry['title']},
            {'$setOnInsert': entry},
            upsert=True
        )
        if result.upserted_id:
            total_inserted += 1
            print(f"  ✅ Inserted: {entry['title']}")
        else:
            total_skipped += 1
            print(f"  ⏭️  Exists:   {entry['title']}")

    # ── Create text index for fast searching ──────────────────────
    try:
        col.create_index([('title','text'),('content','text'),('tags','text')])
        print("\n🔍 Text index created (for fast search)")
    except Exception:
        pass

    final_count = col.count_documents({})
    print(f"\n{'='*50}")
    print(f"✅ Seed complete!")
    print(f"   Inserted : {total_inserted}")
    print(f"   Skipped  : {total_skipped}")
    print(f"   Total in DB: {final_count} documents")
    print(f"{'='*50}")

if __name__ == '__main__':
    seed()
