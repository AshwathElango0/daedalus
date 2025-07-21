import sqlparse

def validate_sql_schema(schema_sql: str) -> dict:
    try:
        parsed = sqlparse.parse(schema_sql)
        if not parsed:
            return {"valid": False, "error": "No SQL statements found."}
        # Basic check: ensure at least one CREATE TABLE
        if not any('CREATE TABLE' in stmt.value.upper() for stmt in parsed):
            return {"valid": False, "error": "No CREATE TABLE statement found."}
        return {"valid": True, "error": None}
    except Exception as e:
        return {"valid": False, "error": str(e)} 