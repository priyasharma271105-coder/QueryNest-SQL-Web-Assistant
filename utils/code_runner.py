"""QueryNest — Code execution engine: Python, Java, C, C++, SQL, MySQL, MongoDB."""
import subprocess, tempfile, os, re, sys
import config

EXEC_TIMEOUT = config.EXEC_TIMEOUT

def run_subprocess(cmd, cwd=None, input_data=None, timeout=EXEC_TIMEOUT):
    try:
        result = subprocess.run(
            cmd, cwd=cwd, input=input_data,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout
        )
        def decode(b): 
            if not b: return ''
            for enc in ('utf-8','cp1252','latin-1'):
                try: return b.decode(enc)
                except: pass
            return b.decode('utf-8', errors='replace')
        return decode(result.stdout), decode(result.stderr), result.returncode
    except subprocess.TimeoutExpired:
        return '', '⏱ Timeout (10s limit). Infinite loop check karo.', -1
    except FileNotFoundError as e:
        return '', f'❌ Compiler not found: {e}', -1

def detect_input_calls(code, lang):
    """Detect if code uses stdin/input functions."""
    patterns = {
        'python': r'\binput\s*\(',
        'java':   r'Scanner|System\.in|BufferedReader|readLine\s*\(',
        'c':      r'\bscanf\s*\(|\bgets\s*\(|\bfgets\s*\(|\bgetchar\s*\(',
        'cpp':    r'\bcin\s*>>|\bgetline\s*\(|\bscanf\s*\(',
    }
    pat = patterns.get(lang)
    if not pat:
        return False
    return bool(re.search(pat, code))

def execute_python(code, stdin_data=None):
    env = {**os.environ, 'PYTHONIOENCODING':'utf-8', 'PYTHONUNBUFFERED':'1'}
    with tempfile.NamedTemporaryFile(suffix='.py', mode='w', delete=False, encoding='utf-8') as f:
        f.write(code); fname = f.name
    try:
        if stdin_data is not None:
            # Ensure every line ends with \n so each input() call gets its value
            lines = stdin_data.splitlines()
            input_bytes = ('\n'.join(lines) + '\n').encode('utf-8')
        else:
            input_bytes = None
        out, err, rc = run_subprocess([sys.executable, '-u', fname], input_data=input_bytes, timeout=EXEC_TIMEOUT)
        if rc == 0:
            return {'output': out.strip() or '(No print() output)', 'error': False}
        # EOFError means not enough inputs were provided
        if 'EOFError' in err:
            return {'output': '⚠️ Input kam pada! Program ne zyada inputs maange.\nStdin box mein saare inputs alag line pe likho aur dobara Run karo.\n\nError: ' + err.strip(), 'error': True}
        # Timeout means input() is waiting — no stdin was provided
        if 'Timeout' in err:
            return {'output': err, 'error': True, 'needs_input': True}
        return {'output': (err or out).strip(), 'error': True}
    finally:
        try: os.unlink(fname)
        except: pass

def execute_java(code, stdin_data=None):
    import shutil
    javac = shutil.which('javac'); java = shutil.which('java')
    if not javac:
        return {'output': '⚠️ Java JDK install karo:\nwinget install Microsoft.OpenJDK.21\nYa: https://adoptium.net/', 'error': True}
    m = re.search(r'public\s+class\s+(\w+)', code)
    cls = m.group(1) if m else 'Main'
    with tempfile.TemporaryDirectory() as d:
        jf = os.path.join(d, f'{cls}.java')
        with open(jf, 'w') as f: f.write(code)
        out, err, rc = run_subprocess([javac, jf], cwd=d)
        if rc != 0: return {'output': err or out, 'error': True}
        input_bytes = ('\n'.join(stdin_data.splitlines()) + '\n').encode('utf-8') if stdin_data else None
        out, err, rc = run_subprocess([java, '-cp', d, cls], cwd=d, input_data=input_bytes)
        return {'output': out or '(No output)', 'error': rc != 0}

def execute_c(code, stdin_data=None):
    with tempfile.TemporaryDirectory() as d:
        cf = os.path.join(d, 'prog.c'); of = os.path.join(d, 'prog')
        with open(cf, 'w') as f: f.write(code)
        out, err, rc = run_subprocess(['gcc', cf, '-o', of, '-lm'], cwd=d)
        if rc != 0: return {'output': err or out, 'error': True}
        input_bytes = ('\n'.join(stdin_data.splitlines()) + '\n').encode('utf-8') if stdin_data else None
        out, err, rc = run_subprocess([of], cwd=d, input_data=input_bytes)
        return {'output': out or '(No output)', 'error': rc != 0}

def execute_cpp(code, stdin_data=None):
    with tempfile.TemporaryDirectory() as d:
        cf = os.path.join(d, 'prog.cpp'); of = os.path.join(d, 'prog')
        with open(cf, 'w') as f: f.write(code)
        out, err, rc = run_subprocess(['g++', cf, '-o', of, '-std=c++17'], cwd=d)
        if rc != 0: return {'output': err or out, 'error': True}
        input_bytes = ('\n'.join(stdin_data.splitlines()) + '\n').encode('utf-8') if stdin_data else None
        out, err, rc = run_subprocess([of], cwd=d, input_data=input_bytes)
        return {'output': out or '(No output)', 'error': rc != 0}

def execute_sql(code):
    import sqlite3, re as _re
    clean = _re.sub(r'--[^\n]*', '', code)
    stmts = [s.strip() for s in clean.split(';') if s.strip()]
    if not stmts: return {'output': '⚠ No SQL found', 'error': False}
    conn = sqlite3.connect(':memory:'); cur = conn.cursor(); lines = []
    for stmt in stmts:
        kw = stmt.upper().split()[0] if stmt.strip() else ''
        try:
            cur.execute(stmt); rows = cur.fetchall()
            if cur.description:
                cols = [d[0] for d in cur.description]
                if rows:
                    w = [max(len(str(c)), max(len(str(r[i])) for r in rows)) for i,c in enumerate(cols)]
                    sep = '+' + '+'.join('-'*(x+2) for x in w) + '+'
                    lines += [sep, '|'+'|'.join(f' {c.ljust(w[i])} ' for i,c in enumerate(cols)) + '|', sep]
                    for r in rows: lines.append('|'+'|'.join(f' {str(v).ljust(w[i])} ' for i,v in enumerate(r))+'|')
                    lines += [sep, f'{len(rows)} row(s)']
                else: lines.append('(0 rows)')
            else:
                n = cur.rowcount if cur.rowcount >= 0 else 0
                msgs = {'CREATE':'✅ Table created','INSERT':f'✅ {n} row(s) inserted',
                        'UPDATE':f'✅ {n} row(s) updated','DELETE':f'✅ {n} row(s) deleted',
                        'DROP':'✅ Dropped','ALTER':'✅ Altered'}
                lines.append(msgs.get(kw, f'✅ {kw} executed'))
        except sqlite3.Error as e: lines.append(f'❌ {e}')
    conn.commit(); conn.close()
    return {'output': '\n'.join(lines) or '✅ Done', 'error': False}

def execute_mysql(code):
    adapted = re.sub(r'AUTO_INCREMENT','AUTOINCREMENT', code, flags=re.I)
    adapted = re.sub(r'INT\s+AUTO_INCREMENT','INTEGER', adapted, flags=re.I)
    adapted = re.sub(r'VARCHAR\s*\(\s*\d+\s*\)','TEXT', adapted, flags=re.I)
    adapted = re.sub(r'DECIMAL\s*\([^)]+\)','REAL', adapted, flags=re.I)
    adapted = re.sub(r'ENUM\s*\([^)]+\)','TEXT', adapted, flags=re.I)
    adapted = re.sub(r'SHOW\s+TABLES\s*;?',"SELECT name FROM sqlite_master WHERE type='table';", adapted, flags=re.I)
    adapted = re.sub(r'TRUNCATE\s+TABLE\s+(\w+)\s*;?', r'DELETE FROM \1;', adapted, flags=re.I)
    r = execute_sql(adapted)
    r['note'] = '(Running on SQLite — MySQL-compatible)'
    return r

def execute_mongodb(code):
    return {'output': '⚠️ MongoDB execution: run mongod aur MongoDB Compass use karo for live queries.', 'error': False}

def run_code(code, lang, stdin_data=None):
    """Main entry point — dispatch to correct executor."""
    lang = lang.lower()
    dangerous = ['os.system(','subprocess.Popen(','rm -rf','format c:']
    if any(d in code.lower() for d in dangerous):
        return {'output': '⚠️ Dangerous command blocked', 'error': True}

    # For interactive languages, detect input usage and ask for stdin if not provided
    interactive_langs = ['python', 'java', 'c', 'cpp']
    if lang in interactive_langs and stdin_data is None and detect_input_calls(code, lang):
        return {
            'output': '',
            'error': False,
            'needs_input': True,
            'message': '📥 Yeh program user se input leta hai. Neeche stdin box mein apna input likho aur phir Run karo.'
        }

    stdin_runners = {
        'python': execute_python, 'java': execute_java,
        'c': execute_c,           'cpp': execute_cpp,
    }
    other_runners = {
        'sql': execute_sql, 'mysql': execute_mysql,
        'mongodb': execute_mongodb,
    }

    if lang in stdin_runners:
        return stdin_runners[lang](code, stdin_data=stdin_data)
    runner = other_runners.get(lang)
    if not runner:
        return {'output': f'Language "{lang}" not supported', 'error': True}
    return runner(code)
