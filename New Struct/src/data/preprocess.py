from loader import text_extract_from

#Cleaning
import re
import unicodedata

# Nettoyer le texte
def clean_text(text):
    # Remplacer les caractères accentués par leur équivalent non accentué
    text = unicodedata.normalize('NFD', text).encode('ascii', 'ignore').decode('utf-8')
    # Supprimer les énumérations avec chiffres romains suivis de tirets
    text = re.sub(r'\b[ivxlcdm]+\.\s', '', text, flags=re.IGNORECASE)
    # Retirer les caractères spéciaux sauf les points, virgules, pourcentages, slashs et sauts de ligne
    text = re.sub(r'[^\w\s\.,%/\n]', '', text)
    # Supprimer les espaces multiples
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

import spacy

#Fonction pour diviser le texte en chunks
def split_text_with_overlap(text, chunk_size=250, chunk_overlap=3, length_function=len, separator="\n"):  #chunk size = 250 et overlap = 3 
    """
    Divise le texte en chunks avec un chevauchement entre les morceaux pour préserver le contexte.

    :param text: Texte à diviser
    :param chunk_size: Taille maximale d'un chunk en tokens
    :param chunk_overlap: Nombre de tokens à chevaucher entre les chunks
    :param length_function: Fonction utilisée pour calculer la longueur des morceaux (par défaut len)
    :param separator: Séparateur utilisé pour joindre les tokens dans chaque chunk
    :return: Liste de chunks
    """
    nlp = spacy.load("fr_core_news_lg")   # Charger le modèle de langage spaCy pour le français
    doc = nlp(text)
    
    # Initialiser les variables
    chunks = []
    current_chunk = []
    current_length = 0
    
    for sent in doc.sents:
        sent_length = length_function(sent.text.split())
        
        # Si la taille du chunk dépasse la limite maximale
        if current_length + sent_length > chunk_size:
            # Ajouter le chunk actuel à la liste
            chunks.append(separator.join(current_chunk))
            
            # Ajouter un chevauchement (phrases des derniers tokens)
            overlap_chunk = current_chunk[-chunk_overlap:] if chunk_overlap > 0 else []
            current_chunk = overlap_chunk
            current_length = length_function(" ".join(current_chunk).split())
        
        # Ajouter la phrase actuelle au chunk
        current_chunk.append(sent.text)
        current_length += sent_length
    
    # Ajouter le dernier chunk
    if current_chunk:
        chunks.append(separator.join(current_chunk))
    
    return chunks


def chunks():
    pdf_text = text_extract_from()
    text = clean_text(pdf_text)
    chunks = split_text_with_overlap(text)
    return chunks

