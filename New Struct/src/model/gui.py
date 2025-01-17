import streamlit as st
from sentence_transformers import SentenceTransformer, util


# Charger le modèle d'embeddings
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

# Liste de documents
documents = [
    "Les examens doivent se dérouler dans le respect des horaires définis.",
    "Les étudiants doivent présenter leur carte d'étudiant lors des évaluations.",
    "Tout retard au début des épreuves sera sanctionné par une exclusion. L'usage des téléphones",
    "L'usage des téléphones portables pendant les évaluations est strictement interdit.",
    "Une note inférieure à 5/20 est considérée comme un échec à l'évaluation."
]

# Fonction pour charger le CSS
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Charger le CSS
load_css("style.css")

# Titre de l'application
st.title("📚Règlement Intérieur des Évaluations à l'EST")
st.markdown("---")

# Champ de saisie de la requête utilisateur
query = st.text_input("🔍 **Entrez votre requête de recherche :**")

# Si une requête est saisie
if query:
    st.markdown("### Résultat de la recherche:")
    # Calculer l'embedding de la requête
    query_embedding = model.encode(query)

   
    doc_embeddings = model.encode(documents)

     # Calculer la similarité entre la requête et les documents
    scores = util.cos_sim(query_embedding, doc_embeddings)[0]

    #recuperer l'id de la similarité le plus  élévé en terme de score .
    best_idx = scores.argmax()

    best_score = scores[best_idx].item()
    best_doc = documents[best_idx] #Recuperer la meilleur reponse à travers son id . 

    # Afficher le résultat
    st.success(f"{best_doc}")
    #st.info(f"Confiance : {best_score:.4f}")
else:
    st.info("Veuillez entrer une requête dans le champ ci-dessus.")
