import sys 
import os 
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import chromadb

from src.data.embeddings import embedding_of
from src.data.preprocess import preprocess_text
from src.data.loader import text_extract_from

def __main__() :
    pdf_text = text_extract_from("ReglementEvalEST.pdf")
    tokens = preprocess_text(pdf_text)

    embeddings = embedding_of(tokens)


    db_path = os.path.abspath("./chromadb_data_base")

    # Vérifier si le répertoire existe, sinon, le créer
    if not os.path.exists(db_path):
        os.makedirs(db_path)
        print(f"Le répertoire {db_path} a été créé.")

    # Initialiser la base de données Chroma
    client = chromadb.Client(database = db_path)

    # Créer une collection dans la base de données (si elle n'existe pas déjà)
    collection = client.create_collection(name="embeddings_collection")


    texts = tokens

    # Stocker les embeddings dans la collection
    # Ici, on stocke les embeddings sous forme de vecteurs associés à des IDs uniques
    for i, (text, embedding) in enumerate(zip(texts, embeddings)):
        collection.add(
            documents=[text],  # Texte original
            embeddings=[embedding],  # Embedding associé
            metadatas=[{"text": text}],  # Métadonnées optionnelles
            ids=[str(i)]  # Identifiant unique pour chaque document
        )

    # Récupérer les embeddings à partir d'un ID
    retrieved = collection.get(ids=["0", "2"])
    print(retrieved)
    

    """
    # Rechercher des documents similaires
    query = "Chroma DB est génial"
    query_embedding = model.encode([query])

    # Recherche par similarité
    results = collection.query(
    query_embeddings=query_embedding,
    n_results=3  # Nombre de résultats à retourner
    )

    print(results)
    """


__main__()