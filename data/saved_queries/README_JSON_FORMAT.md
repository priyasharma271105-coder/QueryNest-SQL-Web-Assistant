# 📁 Saved Queries — JSON File Format

Apni queries/programs yahan JSON files mein save karo.
Search karte waqt QueryNest **pehle in files mein dhundhega**, phir MongoDB mein.

---

## ✅ JSON File Format

Har file ek **JSON Array** hona chahiye jisme objects hon:

```json
[
  {
    "title": "Create Student Table",        ← required: search title
    "language": "sql",                      ← language: sql / mysql / mongodb / python / java / c / cpp
    "tags": ["create", "table", "students"], ← optional: keywords for better search
    "content": "CREATE TABLE students ..."   ← your actual code/query
  },
  {
    ...another entry...
  }
]
```

---

## 📌 Supported Language Values

| Language  | Value      |
|-----------|------------|
| SQL       | `"sql"`    |
| MySQL     | `"mysql"`  |
| MongoDB   | `"mongodb"`|
| Python    | `"python"` |
| Java      | `"java"`   |
| C         | `"c"`      |
| C++       | `"cpp"`    |

---

## 🗂️ File Organization

Aap multiple JSON files rakh sakte ho, for example:
```
saved_queries/
├── my_sql_queries.json
├── mongodb_queries.json
├── python_programs.json
└── java_programs.json
```

---

## 🔍 Search kaise kaam karta hai

1. User search karta hai → **JSON files pehle check hongi**
2. Match nahi mila → **MongoDB (query_library) check hoga**
3. Wahan bhi nahi → **Built-in answers check honge**
4. Kuch nahi mila → **AI se poochho** (Ask AI button)
