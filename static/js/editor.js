/**
 * QueryNest — Code Editor Module
 * Handles: code editor, Run Code, Clear, language switching, save
 * Real execution via /api/execute (Python, Java, C, C++, SQL, MySQL, MongoDB)
 */

'use strict';

// ── Output Helpers ────────────────────────────────────────────
function setOutput(html, isError = false) {
    const out = document.getElementById('codeOutput');
    const pre = document.getElementById('outputText');
    if (!out || !pre) return;
    out.classList.add('active');
    out.style.display = 'block';          // ensure visible always
    out.style.borderColor = isError ? '#ef4444' : '#22c55e';
    pre.innerHTML = html;
    out.scrollTop = 0;                    // scroll to top of output
}

function esc(t) {
    return String(t)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');
}
function escapeHtml(t) { return esc(t); }

function colorLine(t, type) {
    const colors = {
        success: '#86efac',
        error:   '#f87171',
        info:    '#60a5fa',
        warn:    '#fbbf24',
        dim:     '#6b7280',
    };
    return `<span style="color:${colors[type] || colors.success}">${esc(t)}</span>`;
}

// ── Stdin Input Box (shown when program needs user input) ──────
function ensureStdinBox() {
    if (document.getElementById('stdinBox')) return;
    const outputEl = document.getElementById('outputArea') || document.getElementById('output');
    if (!outputEl) return;
    const wrapper = document.createElement('div');
    wrapper.id = 'stdinBox';
    wrapper.style.cssText = 'margin-top:10px;padding:10px;background:#1e293b;border:1px solid #3b82f6;border-radius:6px;display:none;';
    wrapper.innerHTML = `
        <div style="color:#93c5fd;font-size:13px;margin-bottom:6px;">
            📥 <strong>Program ka Input (stdin)</strong> — har value alag line pe likho:
        </div>
        <textarea id="stdinInput" rows="4" placeholder="Example:\nAlice\n25\nhello world"
            style="width:100%;box-sizing:border-box;background:#0f172a;color:#e2e8f0;border:1px solid #475569;border-radius:4px;padding:8px;font-family:monospace;font-size:13px;resize:vertical;"></textarea>
        <div style="margin-top:6px;display:flex;gap:8px;align-items:center;">
            <button id="stdinRunBtn" onclick="runCodeWithStdin()"
                style="background:#3b82f6;color:#fff;border:none;padding:6px 16px;border-radius:4px;cursor:pointer;font-size:13px;">
                ▶ Input de ke Run karo
            </button>
            <button onclick="hideStdinBox()"
                style="background:#475569;color:#e2e8f0;border:none;padding:6px 12px;border-radius:4px;cursor:pointer;font-size:13px;">
                ✕ Cancel
            </button>
        </div>
    `;
    outputEl.parentNode.insertBefore(wrapper, outputEl.nextSibling);
}

function showStdinBox(message) {
    ensureStdinBox();
    const box = document.getElementById('stdinBox');
    if (box) { box.style.display = 'block'; }
    if (message) setOutput(colorLine(message, 'info'));
    const ta = document.getElementById('stdinInput');
    if (ta) ta.focus();
}

function hideStdinBox() {
    const box = document.getElementById('stdinBox');
    if (box) box.style.display = 'none';
}

async function runCodeWithStdin() {
    const stdinEl = document.getElementById('stdinInput');
    const stdin = stdinEl ? stdinEl.value : '';
    hideStdinBox();
    await runCode(stdin);
}

// ── Run Code — sends to /api/execute ─────────────────────────
async function runCode(stdinData) {
    const codeEl  = document.getElementById('codeInput');
    const langEl  = document.getElementById('langSelect');
    const runBtn  = document.getElementById('runBtn') || document.querySelector('.btn-run');
    if (!codeEl || !langEl) {
        console.error('Editor elements not found!');
        return;
    }

    const code = codeEl.value.trim();
    const lang = langEl.value;

    if (!code) {
        setOutput(colorLine('⚠ Pehle kuch code likho, phir Run karo!', 'error'), true);
        return;
    }

    if (runBtn) { runBtn.disabled = true; runBtn.textContent = '⏳ Running...'; }

    const langLabels = {
        python:  '🐍 Python',
        java:    '☕ Java',
        c:       '⚙ C',
        cpp:     '⚙ C++',
        sql:     '🗄 SQL (SQLite)',
        mysql:   '🐬 MySQL (SQLite engine)',
        mongodb: '🍃 MongoDB',
    };
    const label = langLabels[lang] || lang.toUpperCase();
    setOutput(colorLine(`⏳ ${label} code server pe execute ho raha hai...`, 'info'));

    // Build request body — include stdin only if provided
    const body = { code, lang };
    if (stdinData !== undefined && stdinData !== null) {
        body.stdin = stdinData;
    }

    try {
        const res = await fetch('/api/execute', {
            method:  'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body:    JSON.stringify(body),
        });
        const data = await res.json();

        // Server says program needs stdin input
        if (data.needs_input) {
            if (runBtn) { runBtn.disabled = false; runBtn.textContent = '▶ Run Code'; }
            showStdinBox(data.message || '📥 Apna input neeche likho aur Run karo.');
            return;
        }

        const note = data.note
            ? colorLine('ℹ ' + data.note, 'dim') + '\n'
            : '';

        if (data.error) {
            const errText = esc(data.output || 'Unknown error').replace(/\n/g, '<br>');
            setOutput(
                colorLine('❌ ' + label + ' Error:', 'error') + '<br>' +
                note +
                '<span style="color:#f87171">' + errText + '</span>',
                true
            );
        } else {
            const rawOut = (data.output !== undefined && data.output !== null)
                ? String(data.output) : '';
            const displayOut = rawOut.trim()
                ? rawOut.trim()
                : '(Program ran successfully — no output printed)';
            const outText = esc(displayOut).replace(/\n/g, '<br>');
            setOutput(
                colorLine('✅ ' + label + ' Output:', 'success') + '<br>' +
                note +
                '<span style="color:#e2e8f0;font-family:monospace;">' + outText + '</span>'
            );
        }
    } catch (err) {
        setOutput(
            colorLine('❌ Network Error: ' + err.message + '\nServer chal raha hai?', 'error'),
            true
        );
    } finally {
        if (runBtn) { runBtn.disabled = false; runBtn.textContent = '▶ Run Code'; }
    }
}

// ── Clear Editor ──────────────────────────────────────────────
function clearCode() {
    const el = document.getElementById('codeInput');
    if (el) el.value = '';
    const out = document.getElementById('codeOutput');
    if (out) {
        out.style.display = 'block';
        out.style.borderColor = 'var(--border-color)';
    }
    setOutput(colorLine('// Output will appear here after clicking Run Code ▶', 'dim'));
}

// ── Language switching ────────────────────────────────────────
// Default starter code for each language
const STARTER_CODE = {
    sql: `-- SQL: Students table banao aur data daalo
CREATE TABLE students (
    id    INTEGER PRIMARY KEY, -- unique ID
    name  TEXT    NOT NULL,    -- student ka naam
    age   INTEGER,             -- age field
    marks REAL    DEFAULT 0    -- marks
);

INSERT INTO students (name, age, marks) VALUES
    ('Alice',   20, 92.5), -- Alice ka record
    ('Bob',     21, 78.0), -- Bob ka record
    ('Charlie', 19, 85.5); -- Charlie ka record

SELECT * FROM students ORDER BY marks DESC; -- sort by marks descending`,

    mysql: `-- MySQL: Students table
CREATE TABLE students (
    id    INT AUTO_INCREMENT PRIMARY KEY, -- auto-increment primary key
    name  VARCHAR(100) NOT NULL,          -- name column
    age   INT,                            -- age field
    marks DECIMAL(5,2) DEFAULT 0.00       -- decimal marks field
);

INSERT INTO students (name, age, marks) VALUES
    ('Alice', 20, 92.5),   -- first record
    ('Bob',   21, 78.0);   -- second record

SELECT name, marks FROM students WHERE marks > 80; -- 80+ marks wale`,

    mongodb: `// MongoDB: students collection mein data daalo
db.students.insertMany([                   // insert multiple documents at once
    { name: "Alice",   age: 20, marks: 92.5, class: "10th" }, // first student
    { name: "Bob",     age: 21, marks: 78.0, class: "11th" }, // second student
    { name: "Charlie", age: 19, marks: 85.5, class: "10th" }  // third student
]);

db.students.find({ marks: { $gt: 80 } })  // find students with marks greater than 80
    .sort({ marks: -1 });                 // sort by marks in descending order`,

    python: `# Python: Prime numbers nikalo
def is_prime(n):           # returns True if n is prime
    if n < 2: return False # 2 se chhota koi prime nahi
    for i in range(2, int(n**0.5) + 1): # check divisors from 2 to sqrt(n) check karo
        if n % i == 0: return False      # divisor found — not prime
    return True                          # no divisor found — it is prime

primes = [n for n in range(2, 51) if is_prime(n)]  # collect primes from 2 to 50
print("Primes 2-50:", primes)                       # print the result
print("Total:", len(primes), "primes found")        # print the total count`,

    java: `// Java: Fibonacci series
public class Fibonacci {
    public static void main(String[] args) {  // main method — program entry point
        int n = 10;          // number of Fibonacci terms
        int a = 0, b = 1;    // initialize first two Fibonacci terms
        System.out.print("Fibonacci: "); // print label
        for (int i = 0; i < n; i++) {   // loop n times
            System.out.print(a + " ");   // print current Fibonacci term
            int temp = a + b;  // compute next term
            a = b;             // update a with b
            b = temp;          // update b with temp
        }
        System.out.println(); // new line
    }
}`,

    c: `// C: Calculate Factorial
#include <stdio.h>   // input/output ke liye header

long factorial(int n) {         // factorial function
    if (n <= 1) return 1;       // base case: 0! = 1! = 1
    return n * factorial(n-1);  // recursive case: n * (n-1)!
}

int main() {                    // main function — program entry point
    for (int i = 1; i <= 7; i++) {            // loop from 1 to 7
        printf("%d! = %ld\\n", i, factorial(i)); // print factorial result
    }
    return 0; // exit with success
}`,

    cpp: `// C++: Bubble Sort
#include <iostream>   // for cout output
#include <vector>     // for dynamic array
using namespace std;  // use std namespace

void bubbleSort(vector<int>& arr) {  // sort array by reference
    int n = arr.size();              // get array size
    for (int i = 0; i < n-1; i++) { // outer iteration
        for (int j = 0; j < n-i-1; j++) { // inner iteration
            if (arr[j] > arr[j+1]) {       // if larger element comes first
                swap(arr[j], arr[j+1]);    // swap the elements
            }
        }
    }
}

int main() {
    vector<int> arr = {64, 34, 25, 12, 22, 11, 90}; // unsorted array
    cout << "Before: ";
    for (int x : arr) cout << x << " "; // print original array
    cout << endl;
    bubbleSort(arr);   // perform bubble sort
    cout << "After:  ";
    for (int x : arr) cout << x << " "; // print sorted array
    cout << endl;
    return 0;
}`,
};

function updateLanguage() {
    const langEl = document.getElementById('langSelect');
    const codeEl = document.getElementById('codeInput');
    if (!langEl || !codeEl) return;
    const lang = langEl.value;

    // Clear AI chat history when language switches (prevents stale repeated responses)
    if (typeof clearChatHistory === 'function') {
        clearChatHistory();
    }

    // Update placeholder / starter code if editor is empty or has previous starter
    const currentCode = codeEl.value.trim();
    const isStarterCode = Object.values(STARTER_CODE).some(s =>
        currentCode === '' || currentCode === s.trim()
    );
    if (!currentCode || isStarterCode) {
        codeEl.value = STARTER_CODE[lang] || '';
    }

    // Reset output
    const out = document.getElementById('codeOutput');
    if (out) {
        out.style.display = 'block';
        out.classList.add('active');
        out.style.borderColor = 'var(--border-color)';
    }
    setOutput(colorLine('// Output will appear here after clicking Run Code ▶', 'dim'));

    // Update language indicator if exists
    const indicator = document.getElementById('currentLangLabel');
    if (indicator) {
        const labels = {
            python: '🐍 Python', java: '☕ Java', c: '⚙ C', cpp: '⚙ C++',
            sql: '🗄 SQL', mysql: '🐬 MySQL', mongodb: '🍃 MongoDB',
        };
        indicator.textContent = labels[lang] || lang.toUpperCase();
    }
}

function selectLanguage(lang) {
    const el = document.getElementById('langSelect');
    if (el) el.value = lang;
    updateLanguage();
    // Scroll to editor
    const editor = document.querySelector('.code-editor');
    if (editor) editor.scrollIntoView({ behavior: 'smooth', block: 'center' });
}

// ── Save to MongoDB ───────────────────────────────────────────
async function saveToMongoDB() {
    const codeEl = document.getElementById('codeInput');
    const langEl = document.getElementById('langSelect');
    if (!codeEl || !langEl) return;

    const code = codeEl.value.trim();
    const lang = langEl.value;
    if (!code) { alert('Pehle code likho, phir save karo!'); return; }

    const name = prompt('File name do (e.g. "Student Table SQL"):');
    if (!name || !name.trim()) return;

    const isDB    = ['sql', 'mysql', 'mongodb'].includes(lang);
    const endpoint = isDB ? '/api/saved-files/save' : '/api/saved-programs/save';
    const body     = isDB
        ? { name: name.trim(), db_type: lang, code, description: '' }
        : { name: name.trim(), lang, code, topic: '', description: '' };

    try {
        const r = await fetch(endpoint, {
            method:  'POST',
            headers: { 'Content-Type': 'application/json' },
            credentials: 'include',
            body:    JSON.stringify(body),
        });
        const d = await r.json();
        if (d.success) {
            alert(`✅ "${name}" saved!\n\nMongoDB Compass mein:\n  DB: QueryNest\n  Collection: ${isDB ? 'saved_files' : 'saved_programs'}`);
        } else {
            alert('❌ Save failed: ' + (d.message || 'Unknown error'));
        }
    } catch (e) {
        alert('❌ Error: ' + e.message);
    }
}

// ── Keyboard shortcut: Ctrl+Enter = Run ──────────────────────
document.addEventListener('DOMContentLoaded', function () {
    const codeInput = document.getElementById('codeInput');
    if (codeInput) {
        codeInput.addEventListener('keydown', function (e) {
            if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
                e.preventDefault();
                runCode();
            }
        });
    }
    // Force output panel visible on page load
    const out = document.getElementById('codeOutput');
    if (out) {
        out.style.display = 'block';
        out.classList.add('active');
    }
    // Set default starter code
    updateLanguage();
});
