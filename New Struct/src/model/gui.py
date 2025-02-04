"""
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

"""


from model import get_model_response
import streamlit as st

st.title("Renseignement")

# Where we will store questions history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Now were will display our history in the interface
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# User input
if prompt:=st.chat_input("what's up?"):
    # Were're going to display user message in the interface
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # We will add the user message to the history
    st.session_state.messages.append({"role":"user","content":prompt})

    response = f"Echo : {get_model_response(prompt)}"
    # We are now about to display the response
    with st.chat_message("assistart"):
        st.markdown(response)
    
    # Finally we will add to the history the response
    st.session_state.messages.append({"role":"assistant","content":response})