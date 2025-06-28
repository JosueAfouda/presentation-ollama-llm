import streamlit as st
import io
import contextlib
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from deepseek_interface import generate_plots

st.title("📊 Exécutez du code Python avec visualisation")

# Upload CSV
uploaded_file = st.file_uploader("📂 Chargez un fichier CSV pour l'explorer :", type="csv")

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        st.session_state["df"] = df  # 🧠 rendre df accessible globalement

        # Capture structure
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            df.info()
        st.session_state["df_info"] = buffer.getvalue()

        st.subheader("👀 Aperçu des données & Structure")
        col1, col2 = st.columns([0.7, 0.3], border=True, gap="large")

        with col1:
            st.markdown("**Aperçu (max 20 lignes)**")
            st.dataframe(df.head(20))

        with col2:
            st.markdown("**Structure de la DataFrame**")
            st.text(st.session_state["df_info"])

    except Exception as e:
        st.error(f"Erreur de chargement du fichier : {e}")

# Zone de saisie de code manuel
code = st.text_area(
    "📝 Écrivez votre code Python ici (matplotlib, seaborn, plotly express supporté) :",
    height=300,
    placeholder="""import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

df = sns.load_dataset("penguins")
sns.histplot(df['flipper_length_mm'].dropna())
plt.title("Distribution des longueurs de nageoires")
""",
)

if st.button("Run"):
    st.subheader("🖥️ Résultat de l'exécution")
    output_buffer = io.StringIO()
    with contextlib.redirect_stdout(output_buffer), contextlib.redirect_stderr(output_buffer):
        try:
            local_vars = {}
            exec(code, {"plt": plt, "sns": sns, "px": px, "go": go, "__name__": "__main__"}, local_vars)

            output = output_buffer.getvalue()
            if output:
                st.code(output)

            fig = plt.gcf()
            if fig.axes:
                st.pyplot(fig)
            plt.clf()

            for var in local_vars.values():
                if isinstance(var, go.Figure):
                    st.plotly_chart(var)

        except Exception as e:
            st.error(f"❌ Erreur lors de l'exécution : {e}")

# Génération de graphiques via LLM
st.markdown("---")
st.subheader("🤖 Génération assistée de graphiques avec IA")

nl_query = st.text_area("🗣️ Décrivez le graphique souhaité (ex : évolution de la température au fil du temps)")

if st.button("Générer & Exécuter les graphiques"):
    df = st.session_state.get("df", None)
    df_info = st.session_state.get("df_info", "")

    if df is not None and nl_query:
        with st.spinner("🧠 Génération des graphiques avec DeepSeek..."):
            try:
                full_prompt = f"Given the structure of my dataframe df:\n{df_info}\n\n{nl_query}"
                matplotlib_code, plotly_code = generate_plots(full_prompt, df_info)
                
                # Nettoyage du code généré
                matplotlib_code = matplotlib_code.replace("plt.show()", "").strip()
                plotly_code = plotly_code.replace("fig.show()", "").strip()

                st.code(matplotlib_code, language="python")
                st.subheader("📈 Graphique Matplotlib/Seaborn")
                local_vars = {"df": df, "plt": plt, "sns": sns}
                exec(matplotlib_code, local_vars)
                fig = plt.gcf()
                if fig.axes:
                    st.pyplot(fig)
                plt.clf()

                st.code(plotly_code, language="python")
                st.subheader("📊 Graphique Plotly Express")
                local_vars = {"df": df, "px": px}
                exec(plotly_code, local_vars)

                for var in local_vars.values():
                    if isinstance(var, go.Figure):
                        st.plotly_chart(var)

            except Exception as e:
                st.error(f"❌ Erreur lors de la génération ou l'exécution du code : {e}")
    else:
        st.warning("Veuillez décrire le graphique et charger un fichier valide.")