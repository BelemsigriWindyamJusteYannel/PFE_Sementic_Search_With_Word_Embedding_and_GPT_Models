from sentence_transformers import SentenceTransformer
from preprocess import chunks

# Chunks
chunks = chunks()

# Model from sentenceTransformer and embeddings creation
model = SentenceTransformer("BAAI/bge-m3")
embeddings = model.encode(chunks)

# Saving embeddings in chromaDB dataBase
import chromadb,os

# Initialiser la base de données Chroma
client = chromadb.Client()
db_path = os.path.abspath("./chromadb_data_base")

# Vérifier si le répertoire existe, sinon, le créer
if not os.path.exists(db_path):
    os.makedirs(db_path)
    print(f"Le répertoire {db_path} a été créé.")

client = chromadb.PersistentClient(path=db_path)

# Collection creation
collection = client.create_collection(name="embeddings_collection")
print("Collection created. Adding embeddings.")

# Add embeddings and chunks in the dataBase
collection.add(
    documents=chunks,  # Données textuelles
    embeddings=embeddings,  # Vecteurs d'embeddings
    metadatas=[{"text": text} for text in chunks],  # Métadonnées
    ids=[str(i) for i in range(len(chunks))]  # Identifiants uniques
)
