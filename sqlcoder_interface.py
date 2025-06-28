import requests
import re

def generate_sql(natural_language_query: str, schema: str) -> str:
    # Prompt bien structuré
    prompt = f"""
### Instructions:
Your task is to convert a question into a SQL query, given a Postgres database schema.
Adhere to these rules:
- Only return a single SQL query
- Do NOT include explanations, multiple answers, or any text outside the SQL query
- Wrap your answer inside a SQL code block like this: ```sql ... ```

### Input:
Generate a SQL query that answers the question: "{natural_language_query}"
This query will run on a database whose schema is represented in this string:

{schema}

### Response:
```sql
"""

    # Appel à Ollama
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": "sqlcoder", "prompt": prompt, "stream": False}
    )
    response.raise_for_status()
    result = response.json()

    # Extraction propre de la requête SQL dans le bloc ```sql ... ```
    sql_response = result.get("response", "")

    match = re.search(r'```sql\s+(.*?)```', sql_response, re.DOTALL | re.IGNORECASE)
    if match:
        sql = match.group(1).strip()
    else:
        # Fallback : retour du premier statement terminé par un ;
        sql = sql_response.strip().split(';')[0] + ';'

    # Nettoyage de balises parasites (ex. <s>)
    sql_cleaned = re.sub(r'^<.*?>', '', sql.strip())
    return sql_cleaned