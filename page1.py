import streamlit as st
from sqlcoder_interface import generate_sql
from db_utils import run_query
from schema_info import dvdrental_schema
import pandas as pd

st.title("🎬 Interrogez la base dvdrental en langage naturel")

# Question de l'utilisateur
query = st.text_input("Ask your question (eg: What are the first 10 rows of the actor table?)")

# Étape 2 : génération de la requête SQL
if st.button("Run", key="run_llm_sql"):
    with st.spinner("Generating SQL query..."):
        try:
            sql = generate_sql(query, dvdrental_schema)
            st.code(sql, language="sql")

            with st.spinner("Running query..."):
                columns, rows = run_query(sql)
                df = pd.DataFrame(rows, columns=columns)

                if not df.empty:
                    st.dataframe(df)
                    # Affichage du nombre de lignes (comme pgAdmin)
                    st.caption(f"Total rows: {len(df)}")

                    # Préparation du fichier CSV pour téléchargement
                    csv = df.to_csv(index=False).encode('utf-8')

                    # Bouton vert de téléchargement
                    st.download_button(
                        label="📥 Download results in CSV",
                        data=csv,
                        file_name="query_results.csv",
                        mime="text/csv",
                        key="download_csv",
                        help="Download the results in CSV format",
                        use_container_width=True
                    )
                else:
                    st.warning("The query was successful, but returned no results.")
        except Exception as e:
            st.error(f"Error generating SQL: {e}")

# Étape 3 : Affichage de la requête SQL éditable par l'utilisateur
edited_sql = st.text_area(
    "✍️ Modify the SQL if needed and click Execute", 
    value="", height=200, key="editable_sql", 
    help="You can copy/paste the generated SQL here and modify it if needed before execution."
)

if st.button("Execute Modified SQL", key="execute_modified_sql"):
    with st.spinner("Running query..."):
        try:
            columns, rows = run_query(edited_sql)
            df = pd.DataFrame(rows, columns=columns)

            if not df.empty:
                st.dataframe(df)
                st.caption(f"Total rows: {len(df)}")

                # Préparation du CSV
                csv = df.to_csv(index=False).encode("utf-8")

                # Bouton de téléchargement
                st.download_button(
                    label="📥 Télécharger les résultats en CSV",
                    data=csv,
                    file_name="modified_query_results.csv",
                    mime="text/csv",
                    key="download_modified_csv",
                    help="Télécharge les résultats au format CSV",
                    use_container_width=True
                )
            else:
                st.warning("The modified query was successful, but returned no results.")
        except Exception as e:
            st.error(f"Error executing SQL: {e}")
                
                