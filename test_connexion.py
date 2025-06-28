from db_utils import run_query
import pandas as pd

query = """
    SELECT
        first_name,
        last_name
    FROM
        customer
    WHERE
        first_name LIKE 'Bra%'
        AND last_name <> 'Motley';
"""
columns, rows = run_query(query)
#print("Columns:", columns)
#print("Rows:", rows)

df = pd.DataFrame(rows, columns=columns)
print(df)

# Essayez d'autres requêtes sur les tables de votre choix