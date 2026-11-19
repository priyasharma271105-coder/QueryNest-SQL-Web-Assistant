"""
QueryNest — Serverless AWS Lambda Function
Purpose: Serverless SQL Query Formatter, Beautifier & Syntax Validator
Can be packaged and uploaded to AWS Lambda as a standalone serverless function.
"""
import json
import re

SQL_KEYWORDS = [
    "SELECT", "FROM", "WHERE", "JOIN", "LEFT JOIN", "RIGHT JOIN", "INNER JOIN", "FULL JOIN",
    "ON", "GROUP BY", "ORDER BY", "HAVING", "LIMIT", "OFFSET", "INSERT INTO", "VALUES",
    "UPDATE", "SET", "DELETE FROM", "CREATE TABLE", "ALTER TABLE", "DROP TABLE",
    "UNION", "UNION ALL", "AS", "AND", "OR", "IN", "NOT IN", "BETWEEN", "LIKE", "IS NULL",
    "IS NOT NULL", "CASE", "WHEN", "THEN", "ELSE", "END", "DISTINCT", "COUNT", "SUM", "AVG", "MIN", "MAX"
]

def format_sql(raw_sql: str) -> dict:
    """
    Parses and beautifies raw SQL text, checking basic balance of quotes and brackets.
    """
    if not raw_sql or not raw_sql.strip():
        return {
            "success": False,
            "error": "Query cannot be empty",
            "formatted_sql": "",
            "is_valid": False,
            "keywords": []
        }

    clean_sql = raw_sql.strip()
    
    # Check quotation and bracket balance
    single_quotes = clean_sql.count("'") % 2 == 0
    double_quotes = clean_sql.count('"') % 2 == 0
    brackets_ok = (clean_sql.count('(') == clean_sql.count(')')) and (clean_sql.count('[') == clean_sql.count(']'))
    is_valid = single_quotes and double_quotes and brackets_ok

    detected_keywords = set()
    formatted = clean_sql

    # Normalize major clause keywords onto newlines with uppercase
    major_clauses = ["SELECT", "FROM", "WHERE", "GROUP BY", "HAVING", "ORDER BY", "LIMIT", "OFFSET", "INSERT INTO", "UPDATE", "SET", "DELETE FROM"]
    
    for kw in sorted(major_clauses, key=len, reverse=True):
        pattern = re.compile(rf'\b{kw}\b', re.IGNORECASE)
        if pattern.search(formatted):
            detected_keywords.add(kw)
            # Add newline before major clauses
            formatted = pattern.sub(f"\n{kw}", formatted)

    # Indent clauses cleanly
    lines = [line.strip() for line in formatted.split('\n') if line.strip()]
    formatted_sql = '\n'.join(lines)

    return {
        "success": True,
        "is_valid": is_valid,
        "validation_warnings": [] if is_valid else ["Unclosed quotation marks or mismatched parentheses detected."],
        "formatted_sql": formatted_sql,
        "keywords_detected": sorted(list(detected_keywords)),
        "character_count": len(formatted_sql),
        "lines_count": len(lines)
    }

def lambda_handler(event, context):
    """
    AWS Lambda entry point.
    Accepts:
      event = {'query': 'SELECT * FROM users'}
      or API Gateway event = {'body': '{"query": "..."}'}
    """
    try:
        body = event
        if isinstance(event, dict) and 'body' in event and isinstance(event['body'], str):
            body = json.loads(event['body'])
            
        sql_input = body.get('query', '') if isinstance(body, dict) else ''
        result = format_sql(sql_input)
        
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(result)
        }
    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"success": False, "error": str(e)})
        }
