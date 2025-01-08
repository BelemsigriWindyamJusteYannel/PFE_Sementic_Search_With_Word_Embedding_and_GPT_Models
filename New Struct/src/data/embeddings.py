""""
from gensim.models import Word2Vec

def embedding_of(sentences):
    # Train Word2Vec
    model = Word2Vec(sentences, vector_size=100, window=5, min_count=1, workers=4)
    return model
"""

import spacy

def embedding_of(sentences):
    nlp = spacy.load("fr_core_news_lg")  # Modèle français
    doc = nlp(sentences)
    embeddings = [token.vector for token in doc]
    return embeddings