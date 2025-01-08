import nltk
nltk.download('stopwords')
nltk.download('punkt_tab')
nltk.download('wordnet')

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re

def preprocess_text(text):
    # Réduire le texte en miniscule
    text.lower()

    # Nettoyage du texte
    text = re.sub(r"[^a-zA-Zàâçéèêëîïôûùüÿñæœ\s'`]", '', text)
                    
    # Segmentation du texte
    tokens = word_tokenize(text)

    # Suppression des mots inutiles
    stop_words = set(stopwords.words('french'))
    tokens = [word for word in tokens if word not in stop_words]

    # Réduisez les mots à leur forme de base
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]

    return ' '.join(tokens)

