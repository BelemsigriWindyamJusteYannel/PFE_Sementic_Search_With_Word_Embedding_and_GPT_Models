import chromadb,requests,os
from sentence_transformers import SentenceTransformer


# Utilisation de LMStudio pour la génération de texte
def send_question_to_lmstudio_LLM(question, contexte):
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


def get_model_response(query):
    model = SentenceTransformer("BAAI/bge-m3")
    # Initialiser la base de données Chroma

    db_path = os.path.abspath("./../data/chromadb_data_base")
    client = chromadb.PersistentClient(path=db_path)
    collection = client.get_collection(name="embeddings_collection")
    print(collection)

    # embeddings gettings
    data = collection.get(include=["embeddings"])
    collect_parag = collection.get(include=["documents"])


    embeddings = data["embeddings"]
    paragraphes = collect_parag["documents"]

    import faiss
    import numpy as np
    # --------------------------------------------------------------------------------------------
    # Indexation et recherche sémantique

    # Initialiser un index FAISS
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)

    # Ajouter les embeddings à l'index
    index.add(np.array(embeddings))

    # Encodage de la requête de l'utilisateur
    query_embedding = model.encode([query])

    distances, indices = index.search(query_embedding, k=8)  # Plus de résultats pour un contexte étendu

    # Obtenir les paragraphes correspondants
    results = [paragraphes[i] for i in indices[0]]

    # Joindre les paragraphes pour former un contexte complet
    context = " ".join(results[:len(results)])

    #Sending to LLM studio and obtaining the result
    response = send_question_to_lmstudio_LLM(query, context)
    
    return response
        



# get_model_response()