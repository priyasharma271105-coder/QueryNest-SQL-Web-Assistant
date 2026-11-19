/**
 * QueryNest — Search Module v2.0 (FIXED)
 * VERSION: 2.0 — Language-filtered search (SQL/MySQL/MongoDB tabs isolated)
 * Contains: SQL_SYNTAX, MONGO_SYNTAX, PROG_SYNTAX data
 * Functions: performSearch, findSyntax, showResult, showNotFound, etc.
 * FIX: DB tabs (sql/mysql/mongodb) now skip JS builtin, use server JSON files
 * FIX: pickBestBlock regex fixed for all languages including c++
 */

'use strict';

console.log('[QueryNest v2.0] search.js loaded — language-filtered search active');

let lastSearchCode = '';

// ══════════════════════════════════════════════════════════════
// SQL SYNTAX REFERENCE
// ══════════════════════════════════════════════════════════════
const SQL_SYNTAX = {
    'show tables': { title: 'SHOW Tables', lang: 'sql', code: `-- Saari tables dikhao (MySQL)
SHOW TABLES;

-- SQLite mein tables dikhao
SELECT name FROM sqlite_master WHERE type='table';

-- Table ki structure dikhao
DESCRIBE students;          -- MySQL
PRAGMA table_info(students); -- SQLite

-- Saare databases dikhao
SHOW DATABASES;` },

    'create': { title: 'CREATE TABLE', lang: 'sql', code: `-- Basic table create karo
CREATE TABLE students (
    id    INTEGER PRIMARY KEY, -- unique row ID
    name  TEXT    NOT NULL,    -- name column mandatory hai
    age   INTEGER,             -- umar
    marks REAL    DEFAULT 0    -- marks, default 0
);

-- MySQL mein (AUTO_INCREMENT ke saath)
CREATE TABLE teachers (
    id      INT AUTO_INCREMENT PRIMARY KEY, -- auto-increment primary key
    name    VARCHAR(100) NOT NULL,          -- name column
    subject VARCHAR(50),                   -- subject column
    salary  DECIMAL(10,2)                  -- salary column
);

-- Agar nahi hai to banao
CREATE TABLE IF NOT EXISTS courses (
    id    INTEGER PRIMARY KEY,
    title TEXT,
    credits INTEGER
);` },

    'insert': { title: 'INSERT Data', lang: 'sql', code: `-- Single row insert
INSERT INTO students VALUES (1, 'Alice', 20, 92.5);

-- Column names ke saath (recommended)
INSERT INTO students (name, age, marks)
VALUES ('Bob', 22, 78.0);

-- Ek saath multiple rows
INSERT INTO students (name, age, marks) VALUES
    ('Charlie', 19, 85.5), -- student 1
    ('Diana',   21, 91.0), -- student 2
    ('Evan',    23, 74.5); -- student 3

-- SELECT se insert karo
INSERT INTO toppers (name, marks)
SELECT name, marks FROM students WHERE marks > 90;` },

    'select': { title: 'SELECT Queries', lang: 'sql', code: `-- Sab kuch dikhao
SELECT * FROM students;

-- Specific columns
SELECT name, marks FROM students;

-- WHERE condition
SELECT * FROM students WHERE marks > 80;

-- ORDER BY
SELECT * FROM students ORDER BY marks DESC; -- high to low

-- LIMIT
SELECT * FROM students LIMIT 5; -- sirf 5 rows

-- COUNT, AVG, MAX, MIN (aggregate functions)
SELECT
    COUNT(*)    AS total,       -- total students
    AVG(marks)  AS avg_marks,   -- average marks
    MAX(marks)  AS highest,     -- sabse zyada
    MIN(marks)  AS lowest       -- sabse kam
FROM students;

-- GROUP BY
SELECT class, AVG(marks) AS avg
FROM students
GROUP BY class; -- class ke hisab se group

-- LIKE (pattern search)
SELECT * FROM students WHERE name LIKE 'A%'; -- A se shuru` },

    'update': { title: 'UPDATE Rows', lang: 'sql', code: `-- Single row update
UPDATE students
SET marks = 95.0
WHERE id = 1; -- sirf id=1 wale ko update karo

-- Multiple columns update
UPDATE students
SET marks = 88.0, age = 21
WHERE name = 'Bob'; -- Bob ko update karo

-- Multiple rows update
UPDATE students
SET marks = marks + 5   -- sabke marks mein 5 add karo
WHERE marks < 80;       -- sirf jinke 80 se kam hain

-- Sab rows update (caution!)
UPDATE students SET marks = marks * 1.1; -- 10% increase` },

    'delete': { title: 'DELETE Rows', lang: 'sql', code: `-- Single row delete
DELETE FROM students WHERE id = 1; -- id=1 wala hatao

-- Condition ke saath delete
DELETE FROM students WHERE marks < 33; -- fail wale hatao

-- Saari rows delete (table rakhni hai)
DELETE FROM students; -- sab hatao, table rahegi

-- Table completely hatao
DROP TABLE students;

-- Agar exist kare to hatao (safe)
DROP TABLE IF EXISTS students;

-- Fast delete (MySQL) — AUTO_INCREMENT reset bhi hota hai
TRUNCATE TABLE students;` },

    'join': { title: 'JOIN — All Types', lang: 'sql', code: `-- INNER JOIN: sirf matching rows
SELECT s.name, c.course_name
FROM students s
INNER JOIN courses c ON s.course_id = c.id;

-- LEFT JOIN: sab students (course na ho to NULL)
SELECT s.name, c.course_name
FROM students s
LEFT JOIN courses c ON s.course_id = c.id;

-- RIGHT JOIN: sab courses (student na ho to NULL)
SELECT s.name, c.course_name
FROM students s
RIGHT JOIN courses c ON s.course_id = c.id;

-- Self JOIN: ek hi table se join (e.g. employee-manager)
SELECT e.name AS employee, m.name AS manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.id;` },

    'where': { title: 'WHERE Conditions', lang: 'sql', code: `-- Basic condition
SELECT * FROM students WHERE marks > 80;

-- AND / OR
SELECT * FROM students WHERE age > 18 AND marks >= 75;
SELECT * FROM students WHERE class='10th' OR class='11th';

-- IN — multiple values
SELECT * FROM students WHERE class IN ('10th','11th','12th');

-- BETWEEN — range
SELECT * FROM students WHERE marks BETWEEN 70 AND 90;

-- LIKE — pattern
SELECT * FROM students WHERE name LIKE 'A%';   -- A se shuru
SELECT * FROM students WHERE name LIKE '%ali%'; -- ali kahin bhi

-- IS NULL / IS NOT NULL
SELECT * FROM students WHERE email IS NULL;
SELECT * FROM students WHERE phone IS NOT NULL;` },

    'index': { title: 'INDEX', lang: 'sql', code: `-- Index create karo (search fast hota hai)
CREATE INDEX idx_name ON students(name);

-- Unique index (duplicate allowed nahi)
CREATE UNIQUE INDEX idx_email ON students(email);

-- Composite index (multiple columns)
CREATE INDEX idx_class_marks ON students(class, marks);

-- Indexes dikhao (MySQL)
SHOW INDEX FROM students;

-- Index drop karo
DROP INDEX idx_name ON students;` },

    'alter': { title: 'ALTER TABLE', lang: 'sql', code: `-- Column add karo
ALTER TABLE students ADD COLUMN email VARCHAR(150);

-- Column drop karo
ALTER TABLE students DROP COLUMN email;

-- Column rename karo
ALTER TABLE students RENAME COLUMN marks TO score;

-- Column type change karo
ALTER TABLE students MODIFY COLUMN marks DECIMAL(5,2);

-- Primary key add karo
ALTER TABLE students ADD PRIMARY KEY (id);` },
};

// ══════════════════════════════════════════════════════════════
// MYSQL SYNTAX REFERENCE  (MySQL-specific — shown only on MySQL tab)
// ══════════════════════════════════════════════════════════════
const MYSQL_SYNTAX = {
    'create': { title: 'CREATE TABLE (MySQL)', lang: 'mysql', code: `-- MySQL: Table banao with AUTO_INCREMENT
CREATE TABLE students (
    id         INT AUTO_INCREMENT PRIMARY KEY, -- auto id
    name       VARCHAR(100) NOT NULL,          -- naam
    age        INT CHECK (age > 0),            -- age
    class      VARCHAR(20),                    -- class
    marks      DECIMAL(5,2) DEFAULT 0.00,      -- marks
    status     ENUM('active','inactive') DEFAULT 'active', -- status
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- timestamp
);

-- Table structure dekho
DESCRIBE students;` },

    'insert': { title: 'INSERT (MySQL)', lang: 'mysql', code: `-- Single row insert
INSERT INTO students (name, age, class, marks)
VALUES ('Alice', 20, '10th', 92.5);

-- Multiple rows ek saath
INSERT INTO students (name, age, class, marks) VALUES
    ('Bob',     21, '11th', 78.0),
    ('Charlie', 19, '10th', 85.5),
    ('Diana',   22, '12th', 91.0);

-- Upsert: id duplicate ho to marks update karo
INSERT INTO students (id, name, marks)
VALUES (1, 'Alice', 97)
ON DUPLICATE KEY UPDATE marks = 97;` },

    'select': { title: 'SELECT (MySQL)', lang: 'mysql', code: `-- Sab rows
SELECT * FROM students;

-- Specific columns with condition
SELECT name, marks FROM students WHERE marks > 80;

-- ORDER BY + LIMIT
SELECT * FROM students ORDER BY marks DESC LIMIT 5;

-- OFFSET (pagination)
SELECT * FROM students LIMIT 5 OFFSET 10; -- page 3

-- GROUP BY with HAVING
SELECT class, COUNT(*) AS total, ROUND(AVG(marks),2) AS avg
FROM students
GROUP BY class
HAVING AVG(marks) > 75
ORDER BY avg DESC;` },

    'update': { title: 'UPDATE (MySQL)', lang: 'mysql', code: `-- Single row update
UPDATE students SET marks = 95 WHERE name = 'Alice';

-- Multiple columns update
UPDATE students SET marks = 98, status = 'active' WHERE id = 1;

-- All rows mein 5% increase
UPDATE students SET marks = marks * 1.05 WHERE class = '10th';

-- Upsert (ON DUPLICATE KEY)
INSERT INTO students (id, name, marks) VALUES (1, 'Alice', 99)
ON DUPLICATE KEY UPDATE marks = 99;` },

    'delete': { title: 'DELETE (MySQL)', lang: 'mysql', code: `-- Single row delete
DELETE FROM students WHERE id = 1;

-- Condition ke saath
DELETE FROM students WHERE marks < 33;

-- TRUNCATE: sab rows + AUTO_INCREMENT reset
TRUNCATE TABLE students;

-- Table drop karo
DROP TABLE IF EXISTS students;` },

    'join': { title: 'JOINs (MySQL)', lang: 'mysql', code: `-- INNER JOIN: sirf matching rows
SELECT s.name, c.course_name
FROM students s
INNER JOIN enrollments e ON s.id = e.student_id
INNER JOIN courses c ON e.course_id = c.id;

-- LEFT JOIN: sab students (unenrolled bhi)
SELECT s.name, c.course_name
FROM students s
LEFT JOIN courses c ON s.class = c.class;

-- Self JOIN: employee-manager
SELECT e.name AS employee, m.name AS manager
FROM employees e
LEFT JOIN employees m ON e.manager_id = m.id;` },

    'index': { title: 'INDEX (MySQL)', lang: 'mysql', code: `-- Regular index
CREATE INDEX idx_marks ON students(marks);

-- Unique index
CREATE UNIQUE INDEX idx_email ON students(email);

-- Composite index
CREATE INDEX idx_class_marks ON students(class, marks);

-- FULLTEXT index (text search ke liye)
CREATE FULLTEXT INDEX ft_name ON students(name);

-- Indexes dekho
SHOW INDEX FROM students;

-- Query optimization check
EXPLAIN SELECT * FROM students WHERE marks > 80;

-- Index drop karo
DROP INDEX idx_marks ON students;` },

    'show': { title: 'SHOW / DESCRIBE (MySQL)', lang: 'mysql', code: `-- Sab databases dekho
SHOW DATABASES;

-- Database use karo
USE school_db;

-- Sab tables dekho
SHOW TABLES;

-- Table structure dekho
DESCRIBE students;
SHOW CREATE TABLE students;

-- Current user aur DB
SELECT USER(), DATABASE();

-- Table sizes
SELECT TABLE_NAME, TABLE_ROWS,
  ROUND((DATA_LENGTH+INDEX_LENGTH)/1024, 2) AS size_kb
FROM information_schema.TABLES
WHERE TABLE_SCHEMA = DATABASE();` },

    'group by': { title: 'GROUP BY + HAVING (MySQL)', lang: 'mysql', code: `-- Count per class
SELECT class, COUNT(*) AS total
FROM students
GROUP BY class;

-- Average marks per class
SELECT class, ROUND(AVG(marks),2) AS avg, MAX(marks) AS highest
FROM students
GROUP BY class
HAVING AVG(marks) > 75
ORDER BY avg DESC;

-- Multiple aggregates
SELECT class,
    COUNT(*)       AS students,
    AVG(marks)     AS avg_marks,
    SUM(marks)     AS total_marks,
    MAX(marks)     AS highest,
    MIN(marks)     AS lowest
FROM students
GROUP BY class;` },

    'where': { title: 'WHERE Conditions (MySQL)', lang: 'mysql', code: `-- Basic condition
SELECT * FROM students WHERE marks > 80;

-- AND / OR
SELECT * FROM students WHERE age > 18 AND marks >= 75;
SELECT * FROM students WHERE class='10th' OR class='11th';

-- IN — multiple values
SELECT * FROM students WHERE class IN ('10th','11th','12th');

-- BETWEEN — range
SELECT * FROM students WHERE marks BETWEEN 70 AND 90;

-- LIKE — pattern
SELECT * FROM students WHERE name LIKE 'A%';    -- A se shuru
SELECT * FROM students WHERE name LIKE '%ali%'; -- ali kahin bhi

-- IS NULL / IS NOT NULL
SELECT * FROM students WHERE email IS NULL;
SELECT * FROM students WHERE phone IS NOT NULL;

-- IFNULL (MySQL specific)
SELECT name, IFNULL(email, 'no-email') AS email FROM students;` },

    'alter': { title: 'ALTER TABLE (MySQL)', lang: 'mysql', code: `-- Column add karo
ALTER TABLE students ADD COLUMN phone VARCHAR(15);

-- Column type modify karo
ALTER TABLE students MODIFY COLUMN marks FLOAT NOT NULL DEFAULT 0;

-- Column rename karo (MySQL 8.0+)
ALTER TABLE students RENAME COLUMN phone TO mobile;

-- Column drop karo
ALTER TABLE students DROP COLUMN mobile;

-- Index add karo
ALTER TABLE students ADD INDEX idx_class (class);

-- Primary key add karo
ALTER TABLE students ADD PRIMARY KEY (id);` },

    'stored procedure': { title: 'Stored Procedure (MySQL)', lang: 'mysql', code: `DELIMITER //
CREATE PROCEDURE GetTopStudents(IN min_marks DECIMAL(5,2))
BEGIN
    SELECT name, class, marks        -- students fetch karo
    FROM students
    WHERE marks >= min_marks         -- min_marks se zyada
    ORDER BY marks DESC;             -- marks ke hisab se sort
END //
DELIMITER ;

-- Procedure call karo
CALL GetTopStudents(85.0);

-- Procedures dekho
SHOW PROCEDURE STATUS WHERE Db = DATABASE();` },

    'trigger': { title: 'TRIGGER (MySQL)', lang: 'mysql', code: `-- Log table banao
CREATE TABLE student_log (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    student_name VARCHAR(100),
    action       VARCHAR(50),
    action_time  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

DELIMITER //
CREATE TRIGGER after_student_insert
AFTER INSERT ON students
FOR EACH ROW
BEGIN
    INSERT INTO student_log (student_name, action) -- log entry
    VALUES (NEW.name, 'INSERTED');                 -- NEW = naya record
END //
DELIMITER ;` },
};

// ══════════════════════════════════════════════════════════════
// MONGODB SYNTAX REFERENCE
// ══════════════════════════════════════════════════════════════
const MONGO_SYNTAX = {
    'create collection': { title: 'Create Collection', lang: 'mongodb', code: `// Collection explicitly create karo
db.createCollection("students")  // "students" collection banao

// Ya insert karte waqt auto-create hoti hai
db.students.insertOne({ name: "Test" }) // insert se collection ban jaati hai

// Validation ke saath create karo
db.createCollection("orders", {       // "orders" collection
    validator: {                      // validation rules
        $jsonSchema: {                // JSON Schema format
            bsonType: "object",       // document type
            required: ["name", "email"] // mandatory fields
        }
    }
})` },

    'insert': { title: 'Insert Documents', lang: 'mongodb', code: `// Ek document insert karo
db.students.insertOne({       // ek document daalo
    name:  "Alice",           // naam
    age:   20,                // umar
    class: "10th",            // class
    marks: 92.5               // marks
})

// Multiple documents ek saath
db.students.insertMany([      // array mein multiple documents
    { name: "Bob",     age: 21, class: "11th", marks: 78.0 }, // student 1
    { name: "Charlie", age: 19, class: "10th", marks: 85.5 }, // student 2
    { name: "Diana",   age: 22, class: "12th", marks: 91.0 }  // student 3
])` },

    'find': { title: 'Find / Query', lang: 'mongodb', code: `// Saare documents dekho
db.students.find()                           // sab documents

// Condition ke saath dhundho
db.students.find({ age: 20 })                // sirf age=20 wale

// Comparison operators
db.students.find({ marks: { $gt: 80 } })     // marks > 80 ($gt = greater than)
db.students.find({ marks: { $gte: 80 } })    // marks >= 80
db.students.find({ marks: { $lt: 50 } })     // marks < 50
db.students.find({ age: { $in: [20,21] } })  // age 20 ya 21

// Sirf kuch fields dikhao (projection)
db.students.find({}, { name: 1, marks: 1, _id: 0 }) // naam aur marks hi

// Sort + Limit + Skip
db.students.find().sort({ marks: -1 })       // marks high to low
db.students.find().limit(5)                  // sirf 5 results
db.students.find().skip(10).limit(5)         // page 2 (10 skip karke 5)` },

    'update': { title: 'Update Documents', lang: 'mongodb', code: `// Ek document update karo
db.students.updateOne(
    { name: "Alice" },          // yeh condition match karo
    { $set: { marks: 95 } }     // $set se marks update karo
)

// Multiple documents update
db.students.updateMany(
    { class: "10th" },          // 10th ke sab students
    { $set: { promoted: true } } // promoted = true kar do
)

// Value increment karo
db.students.updateOne(
    { name: "Bob" },            // Bob ko dhundho
    { $inc: { marks: 5 } }      // marks mein 5 add karo
)

// Upsert: nahi mila to insert karo
db.students.updateOne(
    { email: "new@test.com" },   // email dhundho
    { $set: { name: "New", age: 20 } },
    { upsert: true }             // nahi mila to banao
)` },

    'delete': { title: 'Delete Documents', lang: 'mongodb', code: `// Ek document delete karo
db.students.deleteOne({ name: "Alice" })       // Alice ka pehla record

// Multiple documents delete
db.students.deleteMany({ marks: { $lt: 33 } }) // 33 se kam marks wale sab

// Saare documents delete (collection rahegi)
db.students.deleteMany({})  // sab documents — caution!

// Poori collection drop karo
db.students.drop()          // collection completely hatao

// Database drop karo
db.dropDatabase()           // poora DB — bahut caution!` },

    'aggregate': { title: 'Aggregation Pipeline', lang: 'mongodb', code: `// Average marks by class
db.students.aggregate([
    { $group: {              // GROUP BY jaisa
        _id: "$class",       // class ke hisab se group
        avgMarks: { $avg: "$marks" }, // average marks
        total: { $sum: 1 }   // count
    }},
    { $sort: { avgMarks: -1 } } // average ke hisab se sort
])

// Filter + Group (WHERE + GROUP BY)
db.students.aggregate([
    { $match: { marks: { $gte: 60 } } }, // sirf 60+ wale
    { $group: {
        _id: "$class",
        count:   { $sum: 1 },
        highest: { $max: "$marks" }
    }}
])` },

    'index': { title: 'Indexes', lang: 'mongodb', code: `// Index create karo (search fast hota hai)
db.students.createIndex({ name: 1 })         // name pe ascending index

// Unique index
db.students.createIndex({ email: 1 }, { unique: true }) // email unique

// Compound index
db.students.createIndex({ class: 1, marks: -1 }) // class + marks

// Indexes dekho
db.students.getIndexes()

// Index drop karo
db.students.dropIndex("name_1")` },
};

// ══════════════════════════════════════════════════════════════
// PROGRAMMING SYNTAX REFERENCE (Python / Java / C / C++)
// ══════════════════════════════════════════════════════════════
const PROG_SYNTAX = {
    // ── "prime numbers till n" — specific query, N=50 default ──
    'prime numbers till': {
        python: { title: 'Prime Numbers Till N — Python', lang: 'python', code: `# Prime Numbers Till N — Python
# Prime = sirf 1 aur khud se divisible (2, 3, 5, 7 ...)

# ── Step 1: Check function ──────────────────────────────────
def is_prime(n):
    if n < 2:
        return False               # 0 aur 1 prime nahi hote
    for i in range(2, int(n**0.5) + 1):   # sirf sqrt tak check karo
        if n % i == 0:
            return False           # divisor mila — prime nahi
    return True                    # prime hai!

# ── Step 2: N set karo ──────────────────────────────────────
n = 50   # <-- yahan apna number dalo

# ── Step 3: Saare primes nikalo ─────────────────────────────
primes = [num for num in range(2, n + 1) if is_prime(num)]

# ── Step 4: Result print karo ───────────────────────────────
print(f"Prime numbers till {n}:")
print(primes)
print(f"Total count: {len(primes)}")
# Output: [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
# Total count: 15` },
        java: { title: 'Prime Numbers Till N — Java', lang: 'java', code: `// Prime Numbers Till N — Java
// Prime = sirf 1 aur khud se divisible (2, 3, 5, 7 ...)

public class PrimeTillN {

    // ── Check karo: prime hai ya nahi ───────────────────────
    static boolean isPrime(int n) {
        if (n < 2) return false;              // 0,1 prime nahi hote
        for (int i = 2; i <= Math.sqrt(n); i++) // sqrt tak check
            if (n % i == 0) return false;     // divisor mila
        return true;                          // prime hai!
    }

    public static void main(String[] args) {
        int limit = 50;   // <-- yahan apna number dalo
        System.out.println("Prime numbers till " + limit + ":");
        int count = 0;
        for (int i = 2; i <= limit; i++) {
            if (isPrime(i)) {
                System.out.print(i + " ");    // prime print karo
                count++;
            }
        }
        System.out.println("\nTotal: " + count);
        // Output: 2 3 5 7 11 13 ... 47   Total: 15
    }
}` },
        c: { title: 'Prime Numbers Till N — C', lang: 'c', code: `// Prime Numbers Till N — C
// Prime = sirf 1 aur khud se divisible (2, 3, 5, 7 ...)
#include <stdio.h>
#include <math.h>

// ── Check function ──────────────────────────────────────────
int isPrime(int n) {
    if (n < 2) return 0;                    // 0,1 prime nahi
    for (int i = 2; i <= (int)sqrt(n); i++) // sqrt tak check
        if (n % i == 0) return 0;           // divisor mila
    return 1;                               // prime hai!
}

int main() {
    int limit = 50;   // <-- yahan apna number dalo
    printf("Prime numbers till %d:\n", limit);
    int count = 0;
    for (int i = 2; i <= limit; i++) {
        if (isPrime(i)) {
            printf("%d ", i);               // prime print karo
            count++;
        }
    }
    printf("\nTotal: %d\n", count);
    // Output: 2 3 5 7 11 ... 47   Total: 15
    return 0;
}` },
        cpp: { title: 'Prime Numbers Till N — C++', lang: 'cpp', code: `// Prime Numbers Till N — C++
// Prime = sirf 1 aur khud se divisible (2, 3, 5, 7 ...)
#include <iostream>
#include <cmath>
using namespace std;

// ── Check function ──────────────────────────────────────────
bool isPrime(int n) {
    if (n < 2) return false;               // 0,1 prime nahi
    for (int i = 2; i <= sqrt(n); i++)    // sqrt tak check
        if (n % i == 0) return false;      // divisor mila
    return true;                           // prime hai!
}

int main() {
    int limit = 50;   // <-- yahan apna number dalo
    cout << "Prime numbers till " << limit << ":" << endl;
    int count = 0;
    for (int i = 2; i <= limit; i++) {
        if (isPrime(i)) {
            cout << i << " ";              // prime print karo
            count++;
        }
    }
    cout << endl << "Total: " << count << endl;
    // Output: 2 3 5 7 11 ... 47   Total: 15
    return 0;
}` },
    },

    // ── General "prime" — check + print ──
    'prime': {
        python: { title: 'Prime Number — Python', lang: 'python', code: `# Prime Number — Python
# Prime = sirf 1 aur khud se divisible (2, 3, 5, 7 ...)

# ── Part 1: Check karo — ek number prime hai ya nahi ──────────
def is_prime(n):
    if n < 2:
        return False                  # 0 aur 1 prime nahi hote
    if n == 2:
        return True                   # 2 sabse chhota prime hai
    if n % 2 == 0:
        return False                  # even numbers prime nahi hote
    for i in range(3, int(n**0.5) + 1, 2):   # sirf odd check karo
        if n % i == 0:
            return False              # divisor mila — prime nahi
    return True                       # prime hai!

# Test karo
num = 37
print(f"{num} is {'PRIME ✓' if is_prime(num) else 'NOT prime ✗'}")   # 37 is PRIME ✓

# ── Part 2: Range mein saare primes nikalo ─────────────────────
primes = [n for n in range(2, 51) if is_prime(n)]
print("Primes (2-50):", primes)
print("Total:", len(primes))
# Output: [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]  Total: 15

# ── Part 3: Sieve — bade range ke liye fast method ────────────
def sieve(limit):
    is_p = [True] * (limit + 1)      # pehle sab prime maan lo
    is_p[0] = is_p[1] = False        # 0 aur 1 prime nahi
    for i in range(2, int(limit**0.5) + 1):
        if is_p[i]:
            for j in range(i*i, limit + 1, i):
                is_p[j] = False       # multiples mark karo
    return [i for i in range(2, limit + 1) if is_p[i]]

print("Sieve (1-100):", sieve(100))` },
        java: { title: 'Prime Number — Java', lang: 'java', code: `// Prime Number — Java
// Prime = sirf 1 aur khud se divisible (2, 3, 5, 7 ...)

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
        // ── Part 2: Single check ──
        int num = 37;
        System.out.println(num + " is " + (isPrime(num) ? "PRIME ✓" : "NOT prime ✗"));

        // ── Part 3: Range mein saare primes ──
        System.out.print("Primes (2-50): ");
        int count = 0;
        for (int i = 2; i <= 50; i++) {
            if (isPrime(i)) { System.out.print(i + " "); count++; }
        }
        System.out.println("\nTotal: " + count);
        // Output: 2 3 5 7 11 13 17 19 23 29 31 37 41 43 47  Total: 15
    }
}` },
        c: { title: 'Prime Number — C', lang: 'c', code: `// Prime Number — C
// Prime = sirf 1 aur khud se divisible (2, 3, 5, 7 ...)
#include <stdio.h>
#include <math.h>

// ── Part 1: Check karo ──────────────────────────────────────
int isPrime(int n) {
    if (n < 2) return 0;                    // 0,1 prime nahi hote
    if (n == 2) return 1;                   // 2 prime hai
    if (n % 2 == 0) return 0;              // even = not prime
    for (int i = 3; i <= (int)sqrt(n); i += 2)  // sirf odd check
        if (n % i == 0) return 0;           // divisor mila
    return 1;                               // prime hai!
}

int main() {
    // ── Part 2: Single check ────────────────────────────────
    int num = 37;
    printf("%d is %s\n", num, isPrime(num) ? "PRIME" : "NOT prime");

    // ── Part 3: 2 se 50 tak saare primes ────────────────────
    printf("Primes (2-50): ");
    int count = 0;
    for (int i = 2; i <= 50; i++) {
        if (isPrime(i)) { printf("%d ", i); count++; }
    }
    printf("\nTotal: %d\n", count);
    // Output: 2 3 5 7 11 13 17 19 23 29 31 37 41 43 47  Total: 15
    return 0;
}` },
        cpp: { title: 'Prime Number — C++', lang: 'cpp', code: `// Prime Number — C++
// Prime = sirf 1 aur khud se divisible (2, 3, 5, 7 ...)
#include <iostream>
#include <cmath>
using namespace std;

// ── Part 1: Check function ──────────────────────────────────
bool isPrime(int n) {
    if (n < 2) return false;               // 0,1 prime nahi hote
    if (n == 2) return true;              // 2 prime hai
    if (n % 2 == 0) return false;         // even = not prime
    for (int i = 3; i <= sqrt(n); i += 2) // sirf odd check karo
        if (n % i == 0) return false;      // divisor mila
    return true;                           // prime hai!
}

int main() {
    // ── Part 2: Single check ──
    int num = 37;
    cout << num << " is " << (isPrime(num) ? "PRIME ✓" : "NOT prime ✗") << endl;

    // ── Part 3: 2 se 50 tak saare primes ──
    cout << "Primes (2-50): ";
    int count = 0;
    for (int i = 2; i <= 50; i++) {
        if (isPrime(i)) { cout << i << " "; count++; }
    }
    cout << endl << "Total: " << count << endl;
    // Output: 2 3 5 7 11 13 17 19 23 29 31 37 41 43 47  Total: 15
    return 0;
}` },
    },

    'fibonacci': {
        python: { title: 'Fibonacci — Python', lang: 'python', code: `# Python: Fibonacci series
def fibonacci(n):      # n terms ki Fibonacci series
    a, b = 0, 1        # initialize first two terms
    series = []        # empty list to store series
    for _ in range(n): # repeat n times
        series.append(a) # append current term
        a, b = b, a + b  # calculate next two terms
    return series

result = fibonacci(10)          # generate 10 terms
print("Fibonacci:", result)     # print the result
print("10th term:", result[-1]) # access last/10th term` },
        java: { title: 'Fibonacci — Java', lang: 'java', code: `// Java: Fibonacci series
public class Fibonacci {
    public static void main(String[] args) { // main function
        int n = 10;        // kitne terms chahiye
        int a = 0, b = 1;  // pehle do terms
        System.out.print("Fibonacci: "); // label
        for (int i = 0; i < n; i++) {   // n baar loop
            System.out.print(a + " ");  // current term print
            int temp = a + b; // agla calculate karo
            a = b;            // a update karo
            b = temp;         // b update karo
        }
        System.out.println(); // new line
    }
}` },
        c: { title: 'Fibonacci — C', lang: 'c', code: `// C: Fibonacci series
#include <stdio.h> // printf ke liye
int main() {
    int a = 0, b = 1, n = 10, temp; // variables initialize
    printf("Fibonacci: ");           // label print
    for (int i = 0; i < n; i++) {   // n baar loop chalao
        printf("%d ", a);            // current term print karo
        temp = a + b;  // agla term calculate karo
        a = b;         // a ko update karo
        b = temp;      // b ko update karo
    }
    return 0; // success
}` },
        cpp: { title: 'Fibonacci — C++', lang: 'cpp', code: `// C++: Fibonacci series
#include <iostream>  // cout ke liye
using namespace std; // std:: prefix hatao
int main() {
    int a = 0, b = 1, n = 10; // initialize karo
    cout << "Fibonacci: ";    // label print karo
    for (int i = 0; i < n; i++) { // n baar loop
        cout << a << " ";     // current term print
        int t = a + b;        // next term calculate
        a = b;  // a update
        b = t;  // b update
    }
    cout << endl; // new line
    return 0;
}` },
    },

    'factorial': {
        python: { title: 'Factorial — Python', lang: 'python', code: `# Python: Factorial (recursive)
def factorial(n):                    # n ka factorial nikalo
    if n <= 1: return 1              # base case: 0! = 1! = 1
    return n * factorial(n - 1)      # recursive call: n * (n-1)!

for i in range(1, 8):                # loop from 1 to 7
    print(f"{i}! = {factorial(i)}")  # print the result` },
        java: { title: 'Factorial — Java', lang: 'java', code: `// Java: Factorial
public class Factorial {
    static long factorial(int n) {          // factorial function
        return (n <= 1) ? 1 : n * factorial(n-1); // recursive
    }
    public static void main(String[] args) {
        for (int i = 1; i <= 7; i++)        // 1 se 7 tak
            System.out.println(i + "! = " + factorial(i)); // print
    }
}` },
        c: { title: 'Factorial — C', lang: 'c', code: `// C: Factorial
#include <stdio.h>
long factorial(int n) {               // factorial function
    return (n <= 1) ? 1 : n * factorial(n-1); // recursive
}
int main() {
    for (int i = 1; i <= 7; i++)     // 1 se 7 tak
        printf("%d! = %ld\\n", i, factorial(i)); // result print
    return 0;
}` },
        cpp: { title: 'Factorial — C++', lang: 'cpp', code: `// C++: Factorial
#include <iostream>
using namespace std;
long long factorial(int n) {          // factorial function
    return (n <= 1) ? 1 : n * factorial(n-1); // recursive
}
int main() {
    for (int i = 1; i <= 7; i++)     // 1 se 7 tak
        cout << i << "! = " << factorial(i) << endl; // print
    return 0;
}` },
    },

    'palindrome': {
        python: { title: 'Palindrome — Python', lang: 'python', code: `# Python: Palindrome check
def is_palindrome(s):           # helper function to check prime
    s = s.lower().strip()       # normalize: lowercase and strip spaces
    return s == s[::-1]         # reverse and compare

words = ['madam', 'hello', 'racecar', 'level', 'python']
for w in words:                 # check each word
    result = "✅ Palindrome" if is_palindrome(w) else "❌ Not"
    print(f"{w:10s}: {result}") # print the result` },
        java: { title: 'Palindrome — Java', lang: 'java', code: `// Java: Palindrome check
public class Palindrome {
    static boolean isPalin(String s) {  // string check
        String r = new StringBuilder(s).reverse().toString(); // ulta karo
        return s.equalsIgnoreCase(r);   // compare karo
    }
    public static void main(String[] args) {
        String[] words = {"madam","hello","racecar","level"};
        for (String w : words)           // har word
            System.out.println(w + ": " + (isPalin(w) ? "Palindrome" : "Not"));
    }
}` },
        c: { title: 'Palindrome — C', lang: 'c', code: `// C: Palindrome check
#include <stdio.h>
#include <string.h>
int isPalin(char s[]) {        // check function
    int n = strlen(s);         // string length
    for (int i = 0; i < n/2; i++) // aadha tak check karo
        if (s[i] != s[n-1-i]) return 0; // match nahi = not palindrome
    return 1;                  // palindrome hai
}
int main() {
    char *words[] = {"madam","hello","racecar","level"};
    for (int i = 0; i < 4; i++)
        printf("%s: %s\\n", words[i], isPalin(words[i]) ? "Palindrome" : "Not");
    return 0;
}` },
        cpp: { title: 'Palindrome — C++', lang: 'cpp', code: `// C++: Palindrome check
#include <iostream>
#include <algorithm>
using namespace std;
bool isPalin(string s) {       // check function
    string r = s;              // copy banao
    reverse(r.begin(), r.end()); // ulta karo
    return s == r;             // compare karo
}
int main() {
    string words[] = {"madam","hello","racecar","level"};
    for (auto& w : words)      // har word
        cout << w << ": " << (isPalin(w) ? "Palindrome" : "Not") << endl;
    return 0;
}` },
    },

    'sorting': {
        python: { title: 'Bubble Sort — Python', lang: 'python', code: `# Python: Bubble Sort
def bubble_sort(arr):          # bubble sort function
    n = len(arr)               # get array size
    for i in range(n):         # n baar outer loop
        for j in range(n-i-1): # inner pass — skip sorted elements
            if arr[j] > arr[j+1]:      # if larger element comes first
                arr[j], arr[j+1] = arr[j+1], arr[j] # swap the elements
    return arr

arr = [64, 34, 25, 12, 22, 11, 90] # unsorted array
print("Before:", arr)               # print original array
bubble_sort(arr)                    # sort the array
print("After: ", arr)               # print sorted array` },
        java: { title: 'Bubble Sort — Java', lang: 'java', code: `// Java: Bubble Sort
import java.util.Arrays;
public class BubbleSort {
    static void sort(int[] arr) {              // sort function
        int n = arr.length;                    // array size
        for (int i = 0; i < n-1; i++)         // outer loop
            for (int j = 0; j < n-i-1; j++)   // inner loop
                if (arr[j] > arr[j+1]) {       // compare
                    int t = arr[j]; arr[j] = arr[j+1]; arr[j+1] = t; // swap
                }
    }
    public static void main(String[] args) {
        int[] arr = {64,34,25,12,22,11,90};    // unsorted
        System.out.println("Before: " + Arrays.toString(arr));
        sort(arr);                             // sort karo
        System.out.println("After:  " + Arrays.toString(arr));
    }
}` },
        c: { title: 'Bubble Sort — C', lang: 'c', code: `// C: Bubble Sort
#include <stdio.h>
void bubbleSort(int arr[], int n) { // sort function
    for (int i = 0; i < n-1; i++)  // outer loop
        for (int j = 0; j < n-i-1; j++) // inner loop
            if (arr[j] > arr[j+1]) {    // compare
                int t = arr[j]; arr[j] = arr[j+1]; arr[j+1] = t; // swap
            }
}
int main() {
    int arr[] = {64,34,25,12,22,11,90}, n = 7; // unsorted
    printf("Before: "); for(int i=0;i<n;i++) printf("%d ",arr[i]);
    bubbleSort(arr, n);  // sort karo
    printf("\\nAfter:  "); for(int i=0;i<n;i++) printf("%d ",arr[i]);
    return 0;
}` },
        cpp: { title: 'Bubble Sort — C++', lang: 'cpp', code: `// C++: Bubble Sort
#include <iostream>
#include <vector>
using namespace std;
void bubbleSort(vector<int>& arr) { // reference se sort
    int n = arr.size();             // size
    for (int i = 0; i < n-1; i++)  // outer loop
        for (int j = 0; j < n-i-1; j++) // inner loop
            if (arr[j] > arr[j+1]) swap(arr[j], arr[j+1]); // swap
}
int main() {
    vector<int> arr = {64,34,25,12,22,11,90}; // unsorted
    cout << "Before: "; for(int x:arr) cout << x << " ";
    bubbleSort(arr);   // sort karo
    cout << "\\nAfter:  "; for(int x:arr) cout << x << " ";
    cout << endl; return 0;
}` },
    },

    'loop': {
        python: { title: 'Loops — Python', lang: 'python', code: `# Python: Different loops
# For loop
for i in range(1, 6):              # loop from 1 to 5
    print(f"{i} x {i} = {i*i}")    # print multiplication table

# While loop
n = 5                  # start from
while n > 0:           # continue while n > 0
    print(f"Countdown: {n}") # print value
    n -= 1             # decrement n

# List comprehension (short loop)
squares = [x**2 for x in range(1, 6)] # list of squares
print("Squares:", squares)` },
        java: { title: 'Loops — Java', lang: 'java', code: `// Java: Different loops
public class Loops {
    public static void main(String[] args) {
        // For loop
        for (int i = 1; i <= 5; i++)         // 1 se 5
            System.out.println(i + "x" + i + "=" + (i*i));

        // While loop
        int n = 5;                            // counter
        while (n > 0) {                       // condition
            System.out.println("Count: " + n);
            n--;                              // decrement
        }

        // Enhanced for (array ke liye)
        int[] arr = {10, 20, 30, 40, 50};    // array
        for (int x : arr) System.out.print(x + " "); // each element
    }
}` },
        c: { title: 'Loops — C', lang: 'c', code: `// C: Different loops
#include <stdio.h>
int main() {
    // For loop
    for (int i = 1; i <= 5; i++)           // 1 se 5 tak
        printf("%d x %d = %d\\n", i, i, i*i); // table

    // While loop
    int n = 5;                             // counter
    while (n > 0) {                        // condition
        printf("Countdown: %d\\n", n);     // print
        n--;                               // decrement
    }

    // Do-while (at least ek baar chalega)
    int x = 1;
    do {
        printf("x = %d\\n", x); x++;       // print aur increment
    } while (x <= 3);                      // condition
    return 0;
}` },
        cpp: { title: 'Loops — C++', lang: 'cpp', code: `// C++: Different loops
#include <iostream>
#include <vector>
using namespace std;
int main() {
    // For loop
    for (int i = 1; i <= 5; i++)           // 1 se 5
        cout << i << "x" << i << "=" << i*i << endl;

    // While loop
    int n = 5;                             // counter
    while (n > 0) { cout << "Count: " << n << endl; n--; }

    // Range-based for (modern C++)
    vector<int> v = {10, 20, 30, 40, 50}; // vector
    for (int x : v) cout << x << " ";     // each element
    cout << endl; return 0;
}` },
    },

    'array': {
        python: { title: 'Arrays/Lists — Python', lang: 'python', code: `# Python: Lists (arrays)
arr = [10, 20, 30, 40, 50] # list create karo
print("Array:", arr)       # print value
print("Length:", len(arr)) # size
print("Sum:", sum(arr))    # sum
print("Max:", max(arr))    # maximum

arr.append(60)             # element add karo
print("After append:", arr)

arr.remove(20)             # element remove karo
print("After remove:", arr)

# Slicing
print("First 3:", arr[:3]) # pehle 3
print("Last 2:", arr[-2:]) # aakhri 2
print("Reversed:", arr[::-1]) # ulta` },
        java: { title: 'Arrays — Java', lang: 'java', code: `// Java: Arrays
import java.util.Arrays;
import java.util.ArrayList;
public class ArrayDemo {
    public static void main(String[] args) {
        int[] arr = {10, 20, 30, 40, 50};        // fixed array
        System.out.println("Array: " + Arrays.toString(arr));
        System.out.println("Length: " + arr.length);

        Arrays.sort(arr);                         // sort karo
        System.out.println("Sorted: " + Arrays.toString(arr));

        // ArrayList (dynamic size)
        ArrayList<Integer> list = new ArrayList<>();
        list.add(100); list.add(200); list.add(300); // add karo
        System.out.println("List: " + list);
        list.remove(Integer.valueOf(200));           // remove karo
        System.out.println("After remove: " + list);
    }
}` },
        c: { title: 'Arrays — C', lang: 'c', code: `// C: Arrays
#include <stdio.h>
int main() {
    int arr[] = {10, 20, 30, 40, 50}; // array declare
    int n = 5;                         // size

    printf("Array: ");
    for (int i = 0; i < n; i++) printf("%d ", arr[i]); // print

    // Find max
    int max = arr[0];              // pehla element max maan lo
    for (int i = 1; i < n; i++)   // baaki se compare karo
        if (arr[i] > max) max = arr[i]; // agar bada mila update karo
    printf("\\nMax: %d\\n", max);

    // Sum
    int sum = 0;
    for (int i = 0; i < n; i++) sum += arr[i]; // sum nikalo
    printf("Sum: %d\\n", sum);
    return 0;
}` },
        cpp: { title: 'Arrays — C++', lang: 'cpp', code: `// C++: Arrays + Vectors
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;
int main() {
    vector<int> v = {10, 20, 30, 40, 50}; // dynamic array
    cout << "Size: " << v.size() << endl;  // size

    v.push_back(60);  // end mein add karo
    v.erase(v.begin() + 1); // index 1 remove karo

    sort(v.begin(), v.end()); // sort karo
    cout << "Sorted: ";
    for (int x : v) cout << x << " "; // print

    cout << "\\nMax: " << *max_element(v.begin(), v.end()); // max
    cout << "\\nMin: " << *min_element(v.begin(), v.end()); // min
    cout << endl; return 0;
}` },
    },

    'function': {
        python: { title: 'Functions — Python', lang: 'python', code: `# Python: Functions
def add(a, b):         # define basic function
    return a + b       # sum return karo

def greet(name, msg="Hello"): # function with default argument
    return f"{msg}, {name}!"  # formatted string

def multiply(*nums):    # accept any number of arguments
    result = 1
    for n in nums: result *= n # multiply all numbers together
    return result

# Lambda (anonymous function)
square = lambda x: x**2 # one-line lambda function

print(add(3, 4))                    # 7
print(greet("Alice"))               # Hello, Alice!
print(greet("Bob", "Hi"))           # Hi, Bob!
print(multiply(2, 3, 4))            # 24
print([square(x) for x in range(1,6)]) # [1,4,9,16,25]` },
        java: { title: 'Methods — Java', lang: 'java', code: `// Java: Methods (Functions)
public class Methods {
    // Static method — class object banaye bina call kar sakte
    static int add(int a, int b) { return a + b; }

    // Overloaded method — same naam, alag parameters
    static double add(double a, double b) { return a + b; }

    // Recursive method — apne aap ko call kare
    static int factorial(int n) {
        return (n <= 1) ? 1 : n * factorial(n-1);
    }

    // Variable arguments
    static int sum(int... nums) {   // kitne bhi numbers
        int s = 0;
        for (int n : nums) s += n;  // sab add karo
        return s;
    }

    public static void main(String[] args) {
        System.out.println(add(3, 4));      // 7
        System.out.println(add(1.5, 2.5));  // 4.0
        System.out.println(factorial(5));   // 120
        System.out.println(sum(1,2,3,4,5)); // 15
    }
}` },
        c: { title: 'Functions — C', lang: 'c', code: `// C: Functions
#include <stdio.h>

// Function declaration (prototype)
int add(int a, int b);
long factorial(int n);

int main() {
    printf("add(3,4) = %d\\n", add(3, 4));         // 7
    printf("5! = %ld\\n", factorial(5));            // 120
    return 0;
}

// Function definition
int add(int a, int b) {
    return a + b; // sum return karo
}

long factorial(int n) {         // recursive function
    if (n <= 1) return 1;       // base case
    return n * factorial(n-1);  // recursive call
}` },
        cpp: { title: 'Functions — C++', lang: 'cpp', code: `// C++: Functions + Overloading
#include <iostream>
using namespace std;

// Function overloading — same naam, alag types
int    add(int a, int b)       { return a + b; }
double add(double a, double b) { return a + b; }

// Template function — koi bhi type ke liye
template<typename T>
T getMax(T a, T b) { return (a > b) ? a : b; }

// Recursive function
int factorial(int n) {
    return (n <= 1) ? 1 : n * factorial(n-1);
}

int main() {
    cout << add(3, 4) << endl;          // 7 (int)
    cout << add(1.5, 2.5) << endl;      // 4.0 (double)
    cout << getMax(10, 20) << endl;     // 20
    cout << getMax(3.14, 2.71) << endl; // 3.14
    cout << factorial(5) << endl;       // 120
    return 0;
}` },
    },
};

// ══════════════════════════════════════════════════════════════
// SEARCH LOGIC
// ══════════════════════════════════════════════════════════════

function getActiveLangFilter() {
    const activeTab = document.querySelector('.nav-tab.active');
    if (!activeTab) return 'all';
    // Prefer data-lang attribute (reliable), fallback to textContent
    const dataLang = activeTab.getAttribute('data-lang');
    if (dataLang) return dataLang.toLowerCase();
    return activeTab.textContent.trim().toLowerCase();
}

function findSyntax(query) {
    const q = query.toLowerCase().trim();
    const filterRaw = getActiveLangFilter();
    const filterMap = {
        'all': 'all', 'sql': 'sql', 'mysql': 'mysql', 'mongodb': 'mongodb',
        'python': 'python', 'java': 'java', 'c/c++': 'cpp', 'cpp': 'cpp', 'c': 'c',
    };
    const filter = filterMap[filterRaw] || 'all';
    const editorLang = document.getElementById('langSelect')?.value || 'python';
    const progLang = ['java', 'c', 'cpp'].includes(filter) ? filter
        : ['java', 'c', 'cpp'].includes(editorLang) ? editorLang
        : filter === 'python' ? 'python' : 'python';

    // Strict match: key must be at least 4 chars AND query must contain key as whole word/phrase
    function matches(key, query) {
        if (key.length < 4) return false;              // skip short/ambiguous keys
        return query.includes(key);                    // query contains the key phrase
    }

    // MongoDB tab → MONGO_SYNTAX only
    if (filter === 'mongodb') {
        for (const [key, val] of Object.entries(MONGO_SYNTAX)) {
            if (matches(key, q)) return val;
        }
        return null;
    }

    // MySQL tab → MYSQL_SYNTAX first, fallback to SQL_SYNTAX (lang override to mysql)
    if (filter === 'mysql') {
        for (const [key, val] of Object.entries(MYSQL_SYNTAX)) {
            if (matches(key, q)) return val;
        }
        for (const [key, val] of Object.entries(SQL_SYNTAX)) {
            if (matches(key, q)) {
                return Object.assign({}, val, { lang: 'mysql' });
            }
        }
        return null;
    }

    // SQL tab → SQL_SYNTAX only
    if (filter === 'sql') {
        for (const [key, val] of Object.entries(SQL_SYNTAX)) {
            if (matches(key, q)) return val;
        }
        return null;
    }

    // Programming tabs → PROG_SYNTAX with correct language
    if (['java', 'python', 'c', 'cpp'].includes(filter)) {
        for (const [key, val] of Object.entries(PROG_SYNTAX)) {
            if (matches(key, q)) return val[filter] || val['python'];
        }
        return null;
    }

    // ALL tab → check all syntaxes
    for (const [key, val] of Object.entries(SQL_SYNTAX)) {
        if (matches(key, q)) return val;
    }
    for (const [key, val] of Object.entries(MYSQL_SYNTAX)) {
        if (matches(key, q)) return val;
    }
    for (const [key, val] of Object.entries(MONGO_SYNTAX)) {
        if (matches(key, q)) return val;
    }
    for (const [key, val] of Object.entries(PROG_SYNTAX)) {
        if (matches(key, q)) return val[progLang] || val['python'];
    }
    return null;
}

async function performSearch(useAI = false) {
    const query = document.getElementById('searchInput')?.value.trim();
    if (!query) return;

    const _afMap = {
        'all': 'all', 'sql': 'sql', 'mysql': 'mysql', 'mongodb': 'mongodb',
        'python': 'python', 'java': 'java', 'c/c++': 'cpp', 'cpp': 'cpp', 'c': 'c',
    };
    const _activeLang = _afMap[getActiveLangFilter()] || 'all';

    document.getElementById('searchResultPanel').style.display = 'none';
    document.getElementById('searchLoading').style.display    = 'block';
    document.getElementById('searchLoading').scrollIntoView({ behavior: 'smooth', block: 'center' });

    // ── ALWAYS call server first — JSON files have the real answers ──
    try {
        const res  = await fetch('/api/search', {
            method:  'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body:    JSON.stringify({ query, use_ai: useAI, lang: _activeLang }),
        });

        // Handle non-200 responses (e.g. 401 not logged in)
        if (!res.ok) {
            document.getElementById('searchLoading').style.display = 'none';
            showSearchError('Server error ' + res.status + '. Please refresh and try again.');
            return;
        }

        const data = await res.json();
        document.getElementById('searchLoading').style.display = 'none';

        // Out of scope — not DB/programming topic
        if (data.source === 'out_of_scope') { showOutOfScope(query); return; }

        // Not found in DB/JSON → show Ask AI button directly, no fake syntax
        if (data.source === 'not_found' || !data.success) {
            showNotFound(query, data.lang || _activeLang);
            return;
        }

        // Got a result — pick best code block for active language
        if (data.result && data.result.content) {
            data.result.content  = pickBestBlock(data.result.content, _activeLang);
            data.result.language = data.result.language || _activeLang;
        }
        showResult(data.result, data.source);

    } catch (err) {
        document.getElementById('searchLoading').style.display = 'none';
        showSearchError('Network error — check if server is running.');
    }
}

function showResult(result, source) {
    const badge = document.getElementById('searchResultBadge');
    const icon  = document.getElementById('searchResultIcon');
    const srcMap = {
        database:   ['🗄️', '✅ Found in QueryNest DB',    'rgba(16,185,129,.2)',  '#6ee7b7', 'rgba(16,185,129,.35)'],
        local_json: ['📁', '📁 Found in JSON Files',       'rgba(16,185,129,.2)',  '#6ee7b7', 'rgba(16,185,129,.35)'],
        builtin:    ['📚', '📚 Syntax Reference',          'rgba(59,130,246,.2)',  '#93c5fd', 'rgba(59,130,246,.35)'],
        ai:         ['🤖', '🤖 AI Generated Answer',       'rgba(107,76,227,.2)', '#c4b5fd', 'rgba(107,76,227,.35)'],
    };
    const [ico, txt, bg, color, border] = srcMap[source] || srcMap.ai;
    icon.textContent  = ico;
    badge.textContent = txt;
    badge.style.cssText = `background:${bg};color:${color};border:1px solid ${border};display:inline-flex;align-items:center;gap:5px;margin-top:4px;padding:3px 14px;border-radius:99px;font-size:11px;font-weight:700;`;

    // Title: use result.title, fall back to current query
    const queryVal = document.getElementById('searchInput')?.value.trim() || '';
    document.getElementById('searchResultTitle').textContent = result.title || queryVal || 'Result';

    // Extract code for "Load into Editor" button
    lastSearchCode = extractCode(result.content || '');
    document.getElementById('searchResultContent').innerHTML = formatSearchContent(result.content || '');
    document.getElementById('searchLoadBtn').style.display = lastSearchCode ? 'flex' : 'none';

    // Sync langSelect if it exists (IDE page only)
    const rl = result.language;
    const langSel = document.getElementById('langSelect') || document.getElementById('langSel');
    if (rl && langSel && ['sql','mysql','mongodb','python','java','c','cpp'].includes(rl)) {
        langSel.value = rl;
    }

    document.getElementById('searchResultPanel').style.display = 'block';
    document.getElementById('searchResultPanel').scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// ── Not Found: show Ask AI button ────────────────────────────
function showNotFound(query, lang) {
    // Store for AI call
    window._lastNotFoundQuery = query;
    window._lastNotFoundLang  = lang || _activeLang || 'python';

    document.getElementById('searchResultIcon').textContent = '🔍';
    const badge = document.getElementById('searchResultBadge');
    badge.textContent = '🔍 Saved DB mein Nahi Mila';
    badge.style.cssText = 'background:rgba(107,76,227,.15);color:#c4b5fd;border:1px solid rgba(107,76,227,.3);display:inline-flex;align-items:center;gap:5px;margin-top:4px;padding:3px 14px;border-radius:99px;font-size:11px;font-weight:700;';
    document.getElementById('searchResultTitle').textContent = '"' + esc(query) + '" — saved queries mein nahi hai';

    document.getElementById('searchResultContent').innerHTML =
        '<div style="background:rgba(107,76,227,.08);border:1px solid rgba(107,76,227,.25);border-radius:14px;padding:20px 22px;margin-bottom:18px;">' +
          '<p style="color:rgba(220,200,255,.95);margin:0 0 8px;font-size:15px;font-weight:700;">🔍 "' + esc(query) + '" offline database mein nahi hai.</p>' +
          '<p style="color:rgba(220,200,255,.6);margin:0;font-size:13px;line-height:1.7;">AI se real-time answer lo — fresh, accurate, aur complete code milega.<br>' +
          '<span style="color:rgba(196,181,253,.5);font-size:12px;">⚡ Powered by Gemini AI — free aur fast</span></p>' +
        '</div>' +
        '<div style="display:flex;gap:12px;flex-wrap:wrap;align-items:center;">' +
          '<button id="searchWithAIBtn" onclick="askAIFromSearch()" ' +
            'style="background:linear-gradient(135deg,#6b4ce3,#ec4899);color:#fff;border:none;padding:14px 32px;border-radius:12px;cursor:pointer;font-weight:700;font-size:15px;font-family:inherit;box-shadow:0 4px 20px rgba(107,76,227,.45);transition:transform .15s,box-shadow .15s;letter-spacing:.3px;" ' +
            'onmouseover="this.style.transform='scale(1.04)';this.style.boxShadow='0 6px 28px rgba(107,76,227,.6)'" ' +
            'onmouseout="this.style.transform='scale(1)';this.style.boxShadow='0 4px 20px rgba(107,76,227,.45)'">' +
            '🤖 Search with AI' +
          '</button>' +
          '<button onclick="closeSearch()" ' +
            'style="background:rgba(255,255,255,.07);color:var(--text-muted);border:1.5px solid rgba(255,255,255,.12);padding:14px 20px;border-radius:12px;cursor:pointer;font-weight:600;font-size:13px;font-family:inherit;">✕ Close</button>' +
        '</div>';

    document.getElementById('searchLoadBtn').style.display = 'none';
    document.getElementById('searchResultPanel').style.display = 'block';
    document.getElementById('searchResultPanel').scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// ── Called when user clicks "Search with AI" button ───────────────
async function askAIFromSearch() {
    const query = window._lastNotFoundQuery || document.getElementById('searchInput')?.value.trim() || '';
    const lang  = window._lastNotFoundLang  || _activeLang || 'python';
    if (!query) return;

    // Update button to loading state
    const btn = document.getElementById('searchWithAIBtn');
    if (btn) {
        btn.disabled = true;
        btn.innerHTML = '⏳ AI soch raha hai...';
        btn.style.opacity = '0.75';
    }

    // Update badge
    const badge = document.getElementById('searchResultBadge');
    badge.textContent = '🤖 AI Answer Generate Ho Raha Hai...';
    badge.style.cssText = 'background:rgba(107,76,227,.2);color:#c4b5fd;border:1px solid rgba(107,76,227,.4);display:inline-flex;align-items:center;gap:5px;margin-top:4px;padding:3px 14px;border-radius:99px;font-size:11px;font-weight:700;';

    try {
        const res  = await fetch('/api/search', {
            method:  'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body:    JSON.stringify({ query, use_ai: true, lang }),
        });
        const data = await res.json();

        if (data.success && data.result && data.result.content) {
            // Normalize language block
            data.result.content  = pickBestBlock(data.result.content, lang);
            data.result.language = data.result.language || lang;
            showResult(data.result, 'ai');
        } else {
            // AI also failed — show error message inside panel
            document.getElementById('searchResultContent').innerHTML =
                '<div style="background:rgba(239,68,68,.1);border:1px solid rgba(239,68,68,.25);border-radius:12px;padding:18px 20px;">' +
                '<p style="color:#fca5a5;margin:0 0 6px;font-weight:700;">⚠️ AI abhi available nahi hai.</p>' +
                '<p style="color:rgba(220,200,255,.6);margin:0;font-size:13px;">config.py mein <strong style="color:#c4b5fd;">GEMINI_API_KEY</strong> set karo.<br>' +
                '<a href="https://aistudio.google.com/app/apikey" target="_blank" style="color:#818cf8;">🔑 Free key yahan milegi →</a></p>' +
                '</div>';
            badge.textContent = '⚠️ AI Unavailable';
            badge.style.cssText = 'background:rgba(239,68,68,.15);color:#fca5a5;border:1px solid rgba(239,68,68,.3);display:inline-flex;align-items:center;gap:5px;margin-top:4px;padding:3px 14px;border-radius:99px;font-size:11px;font-weight:700;';
        }
    } catch (err) {
        document.getElementById('searchResultContent').innerHTML =
            '<span style="color:#f87171;">Network error — server se connect nahi ho pa raha.</span>';
    }
}

// ── Out of scope: non-DB/programming query ────────────────────
function showOutOfScope(query) {
    document.getElementById('searchResultIcon').textContent = '⚠️';
    const badge = document.getElementById('searchResultBadge');
    badge.textContent = '⚠️ Scope se Bahar';
    badge.style.cssText = 'background:rgba(245,158,11,.15);color:#fcd34d;border:1px solid rgba(245,158,11,.3);display:inline-flex;align-items:center;gap:5px;margin-top:4px;padding:3px 14px;border-radius:99px;font-size:11px;font-weight:700;';
    document.getElementById('searchResultTitle').textContent = 'Galat Query — "' + esc(query) + '"';
    document.getElementById('searchResultContent').innerHTML =
        '<div style="background:rgba(245,158,11,.08);border:1px solid rgba(245,158,11,.2);border-radius:12px;padding:16px 18px;margin-bottom:16px;">' +
        '<p style="color:rgba(220,200,255,.85);margin:0 0 10px;font-size:14px;line-height:1.8;">' +
        '⚠️ <strong style="color:#fcd34d;">"' + esc(query) + '"</strong> — QueryNest ke scope se bahar hai.<br>' +
        'QueryNest sirf <strong style="color:#c4b5fd;">Database</strong> aur <strong style="color:#c4b5fd;">Programming</strong> topics support karta hai.</p>' +
        '<p style="color:rgba(220,200,255,.65);margin:0;font-size:13px;line-height:1.7;">' +
        '✅ <strong>Supported:</strong> SQL · MySQL · MongoDB · Python · Java · C · C++<br>' +
        '✅ <strong>Examples:</strong> "create table", "find query mongodb", "fibonacci python", "bubble sort in C"</p>' +
        '</div>' +
        '<div style="display:flex;gap:12px;flex-wrap:wrap;">' +
        '<button onclick="document.getElementById(\'searchInput\').value=\'\';closeSearch();document.getElementById(\'searchInput\').focus();" ' +
        'style="background:linear-gradient(135deg,#6b4ce3,#764ba2);color:#fff;border:none;padding:11px 24px;border-radius:12px;cursor:pointer;font-weight:700;font-size:14px;font-family:inherit;">✏️ Naya Search</button>' +
        '<button onclick="closeSearch()" ' +
        'style="background:rgba(255,255,255,.07);color:var(--text-muted);border:1.5px solid rgba(255,255,255,.12);padding:11px 20px;border-radius:12px;cursor:pointer;font-weight:600;font-size:13px;font-family:inherit;">✕ Close</button>' +
        '</div>';
    document.getElementById('searchLoadBtn').style.display = 'none';
    document.getElementById('searchResultPanel').style.display = 'block';
    document.getElementById('searchResultPanel').scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// ── Generic error ─────────────────────────────────────────────
function showSearchError(msg) {
    document.getElementById('searchResultTitle').textContent = 'Error';
    document.getElementById('searchResultBadge').textContent = '⚠ Error';
    document.getElementById('searchResultBadge').style.cssText = 'background:rgba(239,68,68,.15);color:#fca5a5;border:1px solid rgba(239,68,68,.3);display:inline-flex;align-items:center;gap:5px;margin-top:4px;padding:3px 14px;border-radius:99px;font-size:11px;font-weight:700;';
    document.getElementById('searchResultIcon').textContent = '⚠️';
    document.getElementById('searchResultContent').innerHTML = '<span style="color:#f87171">' + esc(msg) + '</span>';
    document.getElementById('searchLoadBtn').style.display = 'none';
    document.getElementById('searchResultPanel').style.display = 'block';
}

function closeSearch() {
    document.getElementById('searchResultPanel').style.display = 'none';
    const si = document.getElementById('searchInput');
    if (si) si.value = '';
}

function loadResultToEditor() {
    // Editor has been removed from this page — redirect to IDE instead
    loadInIDE();
}

// Open code in full IDE
function loadInIDE() {
    if (!lastSearchCode) return;
    // Detect language from code content first (most reliable)
    const code = lastSearchCode.toLowerCase();
    let lang = 'python'; // default

    // Check active tab
    const activeTab = document.querySelector('.nav-tab.active');
    const tabLang   = activeTab ? (activeTab.getAttribute('data-lang') || 'all') : 'all';
    const langMap   = { 'sql':'sql', 'mysql':'mysql', 'mongodb':'mongodb', 'python':'python', 'java':'java', 'c/c++':'cpp', 'cpp':'cpp', 'c':'c' };

    if (tabLang !== 'all' && langMap[tabLang]) {
        lang = langMap[tabLang];
    } else {
        // Auto-detect from code
        if (/\b(create table|select\s+\*|insert into|drop table|alter table|where\s+\w|order by|group by)\b/.test(code)) {
            lang = 'sql';
        } else if (/\b(db\.|insertone|insertmany|find\(|aggregate\()\b/.test(code)) {
            lang = 'mongodb';
        } else if (/\b(public\s+class|system\.out|void\s+main)\b/.test(code)) {
            lang = 'java';
        } else if (/#include\s*</.test(code) && /cout\s*<</.test(code)) {
            lang = 'cpp';
        } else if (/#include\s*</.test(code) && /printf\(/.test(code)) {
            lang = 'c';
        } else if (/\bdef\s+\w+\s*\(|^\s*print\s*\(/.test(code)) {
            lang = 'python';
        }
    }

    sessionStorage.setItem('ide_code', lastSearchCode);
    sessionStorage.setItem('ide_lang', lang);
    window.location.href = '/ide';
}

function copyCodeBlock(btn) {
    const wrap = btn && btn.closest ? btn.closest('.code-wrap') : null;
    const pre = wrap ? wrap.querySelector('pre') : null;
    if (!pre) return;
    let text = '';
    if (pre.querySelector('br')) {
        const clone = pre.cloneNode(true);
        clone.querySelectorAll('br').forEach(br => br.replaceWith('\n'));
        text = clone.textContent || '';
    } else {
        text = pre.textContent || '';
    }
    text = text.replace(/\r\n/g, '\n');
    if (!text) return;
    const orig = btn.textContent;
    const done = function () {
        btn.textContent = '✅ Copied!';
        btn.style.color = '#6ee7b7';
        setTimeout(function () {
            btn.textContent = orig;
            btn.style.color = '#c4b5fd';
        }, 1800);
    };
    const fallback = function () {
        const ta = document.createElement('textarea');
        ta.value = text;
        document.body.appendChild(ta);
        ta.select();
        document.execCommand('copy');
        document.body.removeChild(ta);
    };
    if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(done).catch(function () { fallback(); done(); });
    } else {
        fallback();
        done();
    }
}

// Copy code to clipboard
function copySearchCode() {
    if (!lastSearchCode) return;
    navigator.clipboard.writeText(lastSearchCode).then(() => {
        const btn = event.target;
        const orig = btn.textContent;
        btn.textContent = '✅ Copied!';
        btn.style.background = 'rgba(16,185,129,.3)';
        btn.style.color = '#6ee7b7';
        setTimeout(() => { btn.textContent = orig; btn.style.background = 'rgba(107,76,227,.2)'; btn.style.color = '#c4b5fd'; }, 1800);
    }).catch(() => {
        const ta = document.createElement('textarea');
        ta.value = lastSearchCode;
        document.body.appendChild(ta);
        ta.select();
        document.execCommand('copy');
        document.body.removeChild(ta);
    });
}

// ── Extract first code block ──────────────────────────────────
function extractCode(text) {
    const m = text.match(/```[\w+]*\n?([\s\S]*?)```/);
    return m ? m[1].trim() : '';
}

// ── Pick best matching code block for a given language ────────
function pickBestBlock(raw, lang) {
    if (!raw || !lang || lang === 'all') return raw;

    // C/C++ tab: try both 'cpp' and 'c' blocks
    const tryLangs = (lang === 'cpp') ? ['cpp', 'c'] : [lang];

    for (const tryLang of tryLangs) {
        const langEsc = tryLang.replace(/[+]/g, '\\+');
        const reExact = new RegExp('```' + langEsc + '\\n([\\s\\S]*?)```', 'i');
        const mExact  = raw.match(reExact);
        if (mExact) return '```' + tryLang + '\n' + mExact[1] + '```';
    }

    // No exact match — return first code block as-is
    const clean = raw.replace(/^###[^\n]*\n?/gm, '').trim();
    const mFirst = clean.match(/```[\w+]*\n?[\s\S]*?```/);
    return mFirst ? mFirst[0] : clean;
}

// ── Render search result content ──────────────────────────────
function formatSearchContent(text) {
    if (!text) return '';
    // Remove section headers
    text = text.replace(/^###[^\n]*\n?/gm, '');

    const codeBlocks = [];

    // Render code blocks protected by placeholders
    text = text.replace(/```([\w+]*)?\n?([\s\S]*?)```/g, function (_, l, code) {
        const placeholder = '___CODEBLOCK_' + codeBlocks.length + '___';
        const langLabel = (l || 'code').toUpperCase();
        let cleanCode = code.replace(/\r\n/g, '\n').replace(/^\n+|\s+$/g, '');
        let escaped = cleanCode
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;');
        // Highlight comments
        escaped = escaped
            .replace(/(\/\/[^\n]*)/g,          '<span style="color:#6ee7b7;font-style:italic;">$1</span>')
            .replace(/(--\s[^\n]*)/g,           '<span style="color:#6ee7b7;font-style:italic;">$1</span>')
            .replace(/((?:^|\n)(#[^\n]*))/g,    '$1<span style="color:#6ee7b7;font-style:italic;">$2</span>');
        const blockHtml = '<div class="code-wrap" style="margin:8px 0;border-radius:10px;overflow:hidden;border:1px solid rgba(255,255,255,.1);">'
            + '<div style="display:flex;align-items:center;justify-content:space-between;background:rgba(255,255,255,.05);padding:4px 12px;font-size:11px;color:rgba(220,200,255,.45);font-weight:700;letter-spacing:.05em;">'
            + '<span>' + langLabel + '</span>'
            + '<button type="button" class="code-copy" onclick="copyCodeBlock(this)" style="background:rgba(167,139,250,.15);border:1px solid rgba(167,139,250,.35);color:#c4b5fd;border-radius:6px;padding:3px 10px;cursor:pointer;font-size:11px;font-weight:700;">📋 Copy</button>'
            + '</div>'
            + '<pre style="margin:0;padding:14px;background:rgba(0,0,0,.4);overflow-x:auto;font-size:12.5px;line-height:1.75;white-space:pre;color:#e2e8f0;">' + escaped + '</pre>'
            + '</div>';
        codeBlocks.push(blockHtml);
        return placeholder;
    });

    // Inline markdown
    text = text.replace(/\*\*(.*?)\*\*/g,  '<strong style="color:#e2d9f3;">$1</strong>');
    text = text.replace(/`([^`]+)`/g,       '<code style="background:rgba(124,58,237,.2);padding:2px 6px;border-radius:4px;color:#c4b5fd;font-size:12px;">$1</code>');
    text = text.replace(/^[-•]\s+(.+)$/gm,  '<li style="margin:3px 0;color:rgba(220,200,255,.75);">$1</li>');
    text = text.replace(/\n\n+/g, '<br><br>');
    text = text.replace(/\n/g, '<br>');

    // Restore code blocks
    text = text.replace(/___CODEBLOCK_(\d+)___/g, function (_, idx) {
        return codeBlocks[Number(idx)];
    });
    return text;
}

    return '<div style="font-size:13.5px;color:rgba(220,200,255,.8);line-height:1.7;">' + text + '</div>';
}

// ── Keyboard shortcut: Enter = search ────────────────────────
document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('searchInput')?.addEventListener('keypress', function (e) {
        if (e.key === 'Enter') performSearch();
    });
});
