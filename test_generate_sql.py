from sqlcoder_interface import generate_sql
from db_utils import run_query
from schema_info import dvdrental_schema
import pandas as pd

# Étape 1 : Saisie de la question en langage naturel
question = input("Entrez une question en langage naturel (ex: What are the 10 most rented films?):\n> ")

# Étape 2 : Génération de la requête SQL
try:
    sql = generate_sql(question, dvdrental_schema)
    print("\n Requête SQL générée :\n")
    print(sql)
except Exception as e:
    print(f"\n Erreur lors de la génération SQL : {e}")
    exit()

# Étape 3 : Exécution de la requête SQL
try:
    columns, rows = run_query(sql)
    df = pd.DataFrame(rows, columns=columns)

    if df.empty:
        print("\n La requête a été exécutée mais n'a retourné aucun résultat.")
    else:
        print(f"\n Résultats de la requête (Total rows: {len(df)}):\n")
        print(df.head(10))  # Affiche les 10 premières lignes
except Exception as e:
    print(f"\n Erreur lors de l'exécution de la requête SQL : {e}")
