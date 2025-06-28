# deepseek_interface.py

from typing import Tuple
import ollama  # Assure-toi que le modèle 'deepseek-coder-v2:latest' est lancé via Ollama

def generate_plots(nl_query_for_plots: str, df_info: str) -> Tuple[str, str]:
    """
    Génère deux scripts de visualisation Python à partir d'une requête en langage naturel :
    - un avec matplotlib/seaborn
    - un avec plotly express

    Args:
        nl_query_for_plots (str): La requête utilisateur en langage naturel
        df_info (str): La structure de la DataFrame (résultat de df.info() sous forme de texte)

    Returns:
        Tuple[str, str]: (code_statique_matplotlib, code_interactif_plotly)
    """
    
    prompt = f"""
    You are a Python data visualization expert.

    You are given:
    - The structure of a pandas DataFrame (`df`) as returned by `df.info()`:
    {df_info}

    - A user request in natural language describing a data visualization:
    "{nl_query_for_plots}"

    Your task:

    1. Generate a Python code block to produce a static visualization using **matplotlib** or **seaborn**.
    2. Then generate a second Python code block for the equivalent **interactive** visualization using **plotly express**.

    Assumptions & Instructions:
    - The DataFrame is already loaded and named `df`.
    - Ensure all column names used exist in the provided structure.
    - Do not include import statements or `plt.show()`.

    Return exactly two code blocks, in this order:
    1. Matplotlib/Seaborn code
    2. Plotly Express code
    """

    try:
        response = ollama.chat(
            model="deepseek-coder-v2:latest",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        content = response['message']['content']

        # Extraction simple des deux blocs de code (entre triple backticks)
        import re
        code_blocks = re.findall(r"```(?:python)?\n(.*?)```", content, re.DOTALL)
        if len(code_blocks) >= 2:
            return code_blocks[0].strip(), code_blocks[1].strip()
        elif len(code_blocks) == 1:
            return code_blocks[0].strip(), "# Plotly code not generated"
        else:
            return "# Matplotlib code not generated", "# Plotly code not generated"
    
    except Exception as e:
        return f"# Error generating matplotlib/seaborn code: {e}", f"# Error generating plotly code: {e}"