import chromadb,os
from sentence_transformers import SentenceTransformer

def get_model_response(query):
    model = SentenceTransformer("paraphrase-multilingual-mpnet-base-v2")
    # Initialiser la base de données Chroma

    db_path = os.path.abspath("./../data/chromadb_data_base")
    client = chromadb.PersistentClient(path=db_path)
    collection = client.get_collection(name="embeddings_collection")

    # Encodage de la requête de l'utilisateur

    def semantique_search(query):
        # Recherche dans ChromaDB
        query_embedding = model.encode(query)
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=6 # Nombre de résultats à retourner
        )
        return results['documents'][0]


    import requests

    def send_question_lmstudio_LLM(question, contexte):
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
            "max_tokens": 200,
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


    results = semantique_search(query)

    #Sending to LLM studio and obtaining the result
    response = send_question_lmstudio_LLM(query, results)

    return response