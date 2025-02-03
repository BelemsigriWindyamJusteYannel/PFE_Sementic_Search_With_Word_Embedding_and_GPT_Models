import os
import sys
import streamlit as st
from sentence_transformers import SentenceTransformer



# Charger le modèle d'embeddings
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

# Ajouter le chemin du dossier parent au sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from model import semantique_search
from model import send_question_lmstudio_LLM

# Fonction pour charger le CSS
def load_css(file):
    with open(file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Charger le CSS
css_file ="./../css/style.css"
load_css(css_file)

# Fonction principale
def __main__() :
    
    st.title("📚Règlement Intérieur des Évaluations à l'EST")
    st.markdown("---")

    # Champ de saisie de la requête utilisateur
    query = st.text_input("🔍 **Entrez votre requête de recherche :**")

    # Si une requête est saisie
    if query:
        st.markdown("### Résultat de la recherche:")

        # Generer l'embedding de la requête
        results = semantique_search(query)

        
        # Obtenir une réponse en utilisant LMStudio
        reponse = send_question_lmstudio_LLM(query, results)
        
        #st.success(f"{results}")
        st.success(f"{reponse}")
    else:
        st.info("Veuillez entrer une requête dans le champ ci-dessus.")


if __name__ == "__main__":
    __main__()