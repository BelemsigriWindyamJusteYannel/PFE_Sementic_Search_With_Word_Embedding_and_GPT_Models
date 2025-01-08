import pandas as pd
import re
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import spacy
import requests

# Charger le texte depuis un fichier
with open("Reglement1.txt", "r", encoding="utf-8") as file:
    texte = file.read()

# Segmentation plus précise avec spaCy
nlp = spacy.load("fr_core_news_sm")
doc = nlp(texte)
paragraphes = [sent.text.strip() for sent in doc.sents if sent.text.strip()]

# --------------------------------------------------------------------------------------------
# Nettoyage de données

def nettoyer_texte(texte):
    texte = re.sub(r'\s+', ' ', texte)  # Supprime les espaces multiples
    texte = re.sub(r"[^\w\s,.()%]", '', texte)  # Supprime les caractères spéciaux inutiles
    return texte.lower()

paragraphes = [nettoyer_texte(paragraphe) for paragraphe in paragraphes]
print(paragraphes)

# --------------------------------------------------------------------------------------------
# Création des embeddings

# Charger un modèle d'embeddings avancé
modele_embeddings = SentenceTransformer('multi-qa-mpnet-base-dot-v1')

# Générer des embeddings pour chaque passage
embeddings = modele_embeddings.encode(paragraphes)

# --------------------------------------------------------------------------------------------
# Indexation et recherche sémantique

# Initialiser un index FAISS
if not paragraphes:
    raise ValueError("La liste des paragraphes est vide. Vérifiez le fichier d'entrée.")
else:
    dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)

# Ajouter les embeddings à l'index
index.add(np.array(embeddings))

# --------------------------------------------------------------------------------------------
# Utilisation de LMStudio pour la génération de texte

def poser_question_lmstudio(question, contexte):
    """
    Pose une question au modèle déployé sur LMStudio et génère une réponse.
    """
    # Endpoint de l'API LMStudio
    url = "http://localhost:1234/v1/chat/completions"  # Vérifiez le port et endpoint corrects
    headers = {"Content-Type": "application/json"}

    # Structure des messages pour le modèle
    messages = [
        {"role": "system", "content": "Vous êtes un assistant qui répond aux questions basées sur un texte réglementaire."},
        {"role": "user", "content": f"Voici un texte. Répondez à la question suivante en utilisant ce contexte : {contexte}\n\nQuestion : {question}\nRéponse :"}
    ]

    # Payload de la requête
    payload = {
        "messages": messages,
        "temperature": 1,
        "max_tokens": 300,
        "stop": ["\n"]
    }

    # Envoyer la requête POST
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            result = response.json()
            return result.get("choices", [{}])[0].get("message", {}).get("content", "Aucune réponse générée.")
        else:
            return f"Erreur {response.status_code} : {response.text}"
    except Exception as e:
        return f"Erreur lors de l'appel à l'API LMStudio : {e}"

# --------------------------------------------------------------------------------------------
# Exemple d'utilisation

while True :
    # Question de l'utilisateur
    question = input("Entrez votre question :")

    # Recherche sémantique pour trouver le contexte pertinent
    embedding_requete = modele_embeddings.encode([question])
    distances, indices = index.search(embedding_requete, k=8)  # Plus de résultats pour un contexte étendu

    # Obtenir les paragraphes correspondants
    resultats = [paragraphes[i] for i in indices[0]]

    # Joindre les paragraphes pour former un contexte complet
    contexte = " ".join(resultats[:len(resultats)])


    # Obtenir une réponse en utilisant LMStudio
    reponse = poser_question_lmstudio(question, contexte)
    print("Réponse :", reponse)
