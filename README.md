# presentation-ollama-llm

## Setup PostgreSQL Database

- Installer PostgreSQL

- Installer pgAdmin4

- Créer la database [dvdrental](https://neon.com/postgresql/postgresql-getting-started/postgresql-sample-database). Regardez cette vidéo : https://youtu.be/DyMeZ0p92Qk

- Stocker les paramètres de connexion à la database dvdrental dans un fichier .env (à ne as versionner dans le git) au niveau de la racine du projet. Votre fichier .env doit ressembler à cela : 

DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=password
DB_NAME=dvdrental

- Créer une fonction d'exécution de requêtes

    - On aura besoin d'installer les packages psycopg2-binary et python-dotenv 

    pip install psycopg2-binary python-dotenv

- Créer un script pour tester votre connexion à la database dvdrental

    - On aura besoin de Pandas : pip install pandas

    query = """
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema = 'public' 
    AND table_type = 'BASE TABLE';
    """


Et si je ne connais pas SQL et que j'ai envie d'interroher ma base en langage naturel. >>> IA Générative/LLM

## Définition de Concepts

- IA Générative

- LLM

- Ollama

- Téléchargement et Installation d'Ollama (https://ollama.com/)

## Création de l'application

On peut essayer n'importe quel LLM qui peut générer du code. Mais il est mieux de tester des LLMS optimisés (fine-tuned) pour les tâches de génération de code SQL.

- Petite recherche directement sur Ollama en tapant sql dans la barre de recherche et voir les propositions.

- sqlcoder : https://ollama.com/library/sqlcoder

- Ouvrir le terminal et exécuter la commande suivante : ollama run sqlcoder

/bye

ollama list

ollama run sqlcoder:latest

Tapez un Prompt

/bye

D'après la documentation de sqlcoder (https://ollama.com/library/sqlcoder:latest), il faut fournir le schema de votre database au modèle.

- Créer un script schema_info.py et dans ce script, créer une variable String dvdrental_schema contenant le schema de la database dvdrental et les informations sur les relations entre les tables.

- Dans un autre script Python, Créer une fonction de génération  de code SQL

    On aura besoin de la librairie requests (pip install requests)

Voici une **explication claire et concise** de la fonction `generate_sql`, à présenter lors de ta démo pour Isheero :

---

### 🔍 **Que fait la fonction `generate_sql` ?**

La fonction `generate_sql` transforme automatiquement une **question en langage naturel** (ex. : "Quels sont les 10 premiers acteurs ?") en une **requête SQL valide** que l'on peut exécuter sur une base de données PostgreSQL.

---

### ⚙️ **Fonctionnement global :**

1. **Construction d’un prompt structuré**
   → La fonction prépare un message clair à envoyer au LLM, en lui donnant :

   * Des instructions précises (ne renvoyer **qu'une seule requête SQL**, sans explication),
   * La **question utilisateur**,
   * Le **schéma de la base** (tables, colonnes, etc.).

2. **Appel à un modèle LLM local via Ollama**
   → Le prompt est envoyé à **Ollama**, avec le modèle nommé `"sqlcoder"`, capable de générer du SQL à partir de texte.

3. **Récupération et extraction de la requête SQL générée**
   → La réponse du LLM est analysée pour extraire uniquement la **requête SQL propre**, même si le modèle a parfois ajouté des balises inutiles (ex. : bloc `sql` ou `<s>`).

4. **Retour de la requête prête à être exécutée**
   → La requête SQL générée est nettoyée et renvoyée, prête à être utilisée pour interroger la base de données.

---

### ✅ **Pourquoi c’est important ?**

* Cette fonction est **le cœur de l’application** : elle permet à un utilisateur non technique de dialoguer avec une base SQL comme s’il parlait à un assistant.
* Elle montre comment **un LLM local (grâce à Ollama)** peut être utilisé pour **générer du code utile** de manière contrôlée et sécurisée.
* C’est un excellent exemple d’**IA générative appliquée à la Data**.

---

Très bonne question, car **cette ligne est essentielle pour comprendre comment fonctionne l’interaction avec Ollama**. Voici une explication claire et pédagogique pour ta présentation :

---

### 🔁 **Appel à l’API d’Ollama en local**

```python
response = requests.post(
    "http://localhost:11434/api/generate",
    json={"model": "sqlcoder", "prompt": prompt, "stream": False}
)
```

---

### 📍 **Pourquoi `http://localhost:11434/api/generate` ?**

* `http://localhost:11434` → Cela signifie que **le modèle LLM tourne en local** sur la machine, via **Ollama**.

  * Ollama installe un petit serveur sur le port `11434`.
  * Ce serveur expose une API pour **dialoguer avec le modèle localement**, sans passer par internet.

* `/api/generate` → C’est le **point d’entrée (endpoint)** de l’API qui permet de **générer une réponse** à partir d’un *prompt*.
  👉 En d'autres termes, c’est l’adresse à laquelle on **envoie la question** pour obtenir une **réponse générée par le modèle**.

---

### ⚙️ **Que fait exactement cette requête POST ?**

* Elle envoie au serveur :

  * `"model": "sqlcoder"` → on précise **le modèle de LLM à utiliser**, ici un modèle spécialisé dans le SQL.
  * `"prompt": prompt` → le **texte complet (question + schéma + instructions)** à traiter.
  * `"stream": False` → indique qu’on **attend une réponse complète d’un seul coup**, et non petit à petit.

---

### 📦 **Que renvoie Ollama ?**

* Une réponse au format JSON contenant le champ `response` :

  ````json
  {
    "response": "```sql\nSELECT * FROM actor LIMIT 10;\n```"
  }
  ````
* Ensuite, le code extrait uniquement la **requête SQL** contenue dans cette réponse.

---

### ✅ **En résumé :**

Cette ligne permet d’**envoyer la question à un modèle LLM qui tourne sur votre propre machine** (via Ollama), et de recevoir une **requête SQL générée automatiquement**, sans dépendre d’un service cloud.

C’est ce qui rend la solution :

* **Privée** (pas de données envoyées à l'extérieur),
* **Gratuite**,
* **Ultra-réactive** en local.

---

- Créer un autre script pour tester la génération de code SQL. Tester avec quelques requêtes en langage naturel comme :

    What are the first 10 rows of the actor table?

    Find customers whose first names start with Bra and last names are not Motley

    (pendant que le modèle tourne, je prendrai quelques questions).

- Vérifier les codes SQL générés par le modèle. Vous pouvez utiliser le script test_connexion.py

- Intégration de cette fonction de génération de code SQL dans une web Streamlit (https://streamlit.io/) multi-pages

    Installer Streamlit : pip install streamlit

    Pour ceux qui veulent démarrer avec Streamlit, j'ain une playlist sur ma chaîne YouTube : https://www.youtube.com/playlist?list=PLmJWMf9F8euQKADN-mSCpTlp7uYDyCQNF

- Tester l'application avec des prompts comme :

    Find the actors who have the last name in the list 'Allen', 'Chase', and 'Davis'

    Vérifiez le résultat avec la requête ci-dessous soit directement dans l'app ou via le script test_connexion.py :

    SELECT
        first_name,
        last_name
    FROM
        actor
    WHERE
        
    ORDER BY
        last_name;

    Which films do not have any inventory available? Requête de vérification :

SELECT
  f.film_id,
  f.title,
  i.inventory_id
FROM
  film f
  LEFT JOIN inventory i USING (film_id)
WHERE
  i.film_id IS NULL
ORDER BY
  f.title;

    List all customer payments along with the customer name, staff member who handled the payment, the amount, and the payment date, ordered by payment date.

SELECT
  c.customer_id,
  c.first_name || ' ' || c.last_name customer_name,
  s.first_name || ' ' || s.last_name staff_name,
  p.amount,
  p.payment_date
FROM
  customer c
  INNER JOIN payment p USING (customer_id)
  INNER JOIN staff s using(staff_id)
ORDER BY
  payment_date;

    Which customers have made the highest total payments?

SELECT
  first_name || ' ' || last_name full_name,
  SUM (amount) amount
FROM
  payment
  INNER JOIN customer USING (customer_id)
GROUP BY
  full_name
ORDER BY
  amount DESC;


- Ajout de la page de visualisation de données. L'idée est que l'utilisateur puisse charger un fichier de données, voir un aperçu de la dataframe et de sa structure, écrire un Prompt pour le graphique qu'il veut sur cette dataframe. En backend un modèle LLM tourne, génère le code Matplotlib/Seaborn (visuel statique) et Plotly (visuel interactif) du graphique. Les graphiques sont affichés directement dans l'application.

    - Télécharger un autre modèle LLM via Ollama : deepseek-coder-v2:latest

        ollama run deepseek-coder-v2:latest (https://ollama.com/library/deepseek-coder-v2)

        Ecrire un prompt pour tester : Can you help me build a Seaborn plot?

        /bye

    - pip install ollama (pour voir une autre manière d'interagir un modèle LLM via Ollama dans un script python)
    
    - pip install plotly-express seaborn

    - Créer la fonction generate_plots qui retourne un tuple de code Matplotlib/Seaborn et de code Plotly

    - Testez d'abord la génération de graphiques avec des codes simples :

Code Matplotlib/Seaborn :

import matplotlib.pyplot as plt
import seaborn as sns

df = sns.load_dataset("penguins")
sns.boxplot(x="species", y="bill_length_mm", data=df)
plt.title("Longueur du bec par espèce")
#plt.show() # Pas besoin de plt.show() pour Matplotlib / Seaborn)

Code Plotly :

import plotly.express as px
df = px.data.gapminder().query("year == 2007")
fig = px.scatter(df, x="gdpPercap", y="lifeExp", color="continent", size="pop", log_x=True)
#fig # Le graphique s'affiche même sans cette ligne.


## Test 1 réussi avec les prompts (dataset 01001099999.csv)  :

- Affiche l'évolution de la température moyenne (TEMP) au fil du temps (DATE), avec une courbe de tendance.

- Show the evolution of average temperature (TEMP) over time (DATE), including a trend line.

## Test 2 réussi avec les prompts (dataset 01001099999.csv) :

- Compare l'évolution mensuelle des températures maximales (MAX) et minimales (MIN) au cours de l'année. Affiche deux courbes sur le même graphique, avec une moyenne mensuelle calculée à partir de la date. Les mois doivent être affichés sous forme de noms (janvier, février, etc.) et triés chronologiquement.

- Compare the monthly evolution of maximum (MAX) and minimum (MIN) temperatures over the year. Display two curves on the same chart, using monthly averages computed from the DATE column. The x-axis should show month names (January, February, etc.) in chronological order.

## Test 3 réussi (dataset X_train_J01Z4CN.csv) avec les prompts :

- Construis un diagramme à barres montrant le pourcentage de valeurs manquantes par colonne.


QUESTIONS

CLOTURE DE LA SEANCE