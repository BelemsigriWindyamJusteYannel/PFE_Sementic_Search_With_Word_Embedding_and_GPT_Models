from loader import text_extract_from

#Cleaning
import re,spacy

# Nettoyage de données

def nettoyer_texte(text):
    text = re.sub(r'\b[ivxlcdm]+\.\s', ' ', text, flags=re.IGNORECASE)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def chunks():
    # Extraction du texte
    pdf_text = text_extract_from()
    
    # Charger le modèle SpaCy
    nlp = spacy.load("fr_core_news_sm")
    doc = nlp(pdf_text)
    
    # Découpage initial en phrases
    phrases = [sent.text.strip() for sent in doc.sents if sent.text.strip()]
    
    # Nettoyage du texte
    phrases = [nettoyer_texte(p) for p in phrases]

    # Paramètres du chunking
    max_tokens = 100  # Limite de tokens par chunk
    sliding_window = 1  # Nombre de phrases chevauchées

    chunks = []
    temp_chunk = ""
    token_count = 0
    
    for i in range(len(phrases)):
        phrase = phrases[i]
        num_tokens = len(phrase.split())

        # Si on dépasse la taille max, on sauvegarde le chunk et on recommence
        if token_count + num_tokens > max_tokens:
            chunks.append(temp_chunk.strip())
            temp_chunk = ""
            token_count = 0

        # Ajouter la phrase au chunk en cours
        temp_chunk += " " + phrase
        token_count += num_tokens

        # Ajouter une phrase supplémentaire en sliding window
        if i + 1 < len(phrases) and sliding_window > 0:
            temp_chunk += " " + phrases[i + 1]
            token_count += len(phrases[i + 1].split())

    # Ajouter le dernier chunk restant
    if temp_chunk:
        chunks.append(temp_chunk.strip())

    return chunks

#chunks = chunks()

#for i, chunk in enumerate(chunks):
#    print(f"Chunk {i+1}:\n{chunk}\n")