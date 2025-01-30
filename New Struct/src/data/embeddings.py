from sentence_transformers import SentenceTransformer
from preprocess import chunks

chunks = chunks()

model = SentenceTransformer("paraphrase-multilingual-mpnet-base-v2")

embeddings = model.encode(chunks)

import chromadb,os

# Initialiser la base de données Chroma
client = chromadb.Client()
db_path = os.path.abspath("./chromadb_data_base")

# Vérifier si le répertoire existe, sinon, le créer
if not os.path.exists(db_path):
    os.makedirs(db_path)
    print(f"Le répertoire {db_path} a été créé.")

client = chromadb.PersistentClient(path=db_path)

try:
    # Vérifier si la collection existe
    collection = client.get_collection(name="embeddings_collection")
    print("Collection exists. Using existing collection.")
except Exception:
    # Créer la collection si elle n'existe pas
    collection = client.create_collection(name="embeddings_collection")
    print("Collection created. Adding embeddings.")

    # Ajouter les documents par batch
    collection.add(
        documents=chunks,  # Données textuelles
        embeddings=embeddings,  # Vecteurs d'embeddings
        metadatas=[{"text": text} for text in chunks],  # Métadonnées
        ids=[str(i) for i in range(len(chunks))]  # Identifiants uniques
    )

def collection():
    return collection