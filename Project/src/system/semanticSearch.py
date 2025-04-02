import chromadb,os
from sentence_transformers import SentenceTransformer
from llama_cpp import Llama

# 🔹 Chargement du modèle GGUF Mistral avec llama-cpp
model_path = "model/mistral-7b-instruct-v0.2.Q4_K_M.gguf"
model = Llama(model_path=model_path)

from sentence_transformers import SentenceTransformer
# 
semantic_model = SentenceTransformer("BAAI/bge-m3")

def generate_final_answer(question, best_responses):
    """ Génère une réponse bien structurée en utilisant Mistral. """
    context = "\n".join(best_responses)
    
    prompt = (
        f"Tu es un assistant au service de scolarité de l école supérieure de technologie de fès qui répond aux questions basées sur un texte réglementaire."
        f"Voici le texte. Répondez à la question suivante en utilisant ce contexte : {context}\n\nQuestion : {question}\nRéponse :"
    )

    output = model(prompt, max_tokens=200, temperature=0.3)
    return output["choices"][0]["text"].strip()



def get_model_response(query):
    
    db_path = os.path.abspath("./../data/chromadb_data_base")
    client = chromadb.PersistentClient(path=db_path)
    collection = client.get_collection(name="embeddings_collection")
    print(collection)
    query_embedding = semantic_model.encode(query)

    # Recherche dans ChromaDB
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=2 # Nombre de résultats à retourner
    )

    response = generate_final_answer(query, results['documents'][0])
    
    return response
        

# get_model_response()
