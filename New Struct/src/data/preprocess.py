from loader import text_extract_from

#Cleaning
import re,spacy

# Nettoyage de données

def nettoyer_texte(text):
    text = re.sub(r'\b[ivxlcdm]+\.\s', ' ', text, flags=re.IGNORECASE)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def chunks():
    pdf_text = text_extract_from()
    nlp = spacy.load("fr_core_news_sm")
    doc = nlp(pdf_text)
    paragraphes = [sent.text.strip() for sent in doc.sents if sent.text.strip()]
    #print(paragraphes)

    paragraphes = [nettoyer_texte(paragraphe) for paragraphe in paragraphes]
    #print(paragraphes)
    return paragraphes