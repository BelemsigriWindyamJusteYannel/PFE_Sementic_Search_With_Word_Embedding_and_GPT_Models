import streamlit as st
from model import get_model_response
import datetime
import re

# Fonction pour charger le CSS
def load_css(file):
    with open(file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Charger le CSS
css_file = "./../css/style.css"
load_css(css_file)

# Initialisation de l'historique des conversations
if "chats" not in st.session_state:
    st.session_state.chats = {}
if "current_chat" not in st.session_state:
    chat_id = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.chats[chat_id] = {"messages": [], "title": "Nouvelle conversation"}
    st.session_state.current_chat = chat_id

# Fonction pour générer un titre basé sur le contenu de la conversation
def generate_chat_title(messages):
    if not messages:
        return "Nouvelle conversation"
    
    text = " ".join(msg["content"] for msg in messages if msg["role"] == "user")
    text = re.sub(r'[^\w\s]', '', text)  # Supprimer les caractères spéciaux
    words = text.split()
    
    if len(words) >= 5:
        return " ".join(words[:5]) + "..."
    return " ".join(words) if words else "Nouvelle conversation"

# Fonction principale
def __main__():
    st.markdown("<div class='fixed-title'><h1>Maroc : Loi de Commerce📚</h1></div>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar pour l'historique et nouveau chat ..
    with st.sidebar:
        st.subheader("Historique des conversations")
        
        # Bouton pour démarrer un nouveau chat
        if st.button("🆕 Nouveau Chat"):
            chat_id = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.session_state.chats[chat_id] = {"messages": [], "title": "Nouvelle conversation"}
            st.session_state.current_chat = chat_id
        
        # Affichage des anciens chats avec titres générés
        for chat_id, chat_data in sorted(st.session_state.chats.items(), reverse=True):
            if st.button(chat_data["title"]):
                st.session_state.current_chat = chat_id
    
    # Vérification et sélection du chat courant
    if st.session_state.current_chat is None:
        return
    
    chat_data = st.session_state.chats[st.session_state.current_chat]
    messages = chat_data["messages"]
    
    # Affichage de l'historique des messages
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for msg in messages:
        if msg["role"] == "user":
            st.markdown(f'<div class="chat-wrapper"><div class="user-message"> <div>{msg["content"]}</div> 🧑 </div></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-wrapper"><div class="bot-message">🤖 <div>{msg["content"]}</div></div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Entrée utilisateur
    prompt = st.chat_input("Entrer votre requête...")
    if prompt:
        messages.append({"role": "user", "content": prompt})
        
        st.markdown(f'<div class="chat-wrapper"><div class="user-message"> <div>{prompt}</div> 🧑 </div></div>', unsafe_allow_html=True)
        
        # Envoi de la requête à l'API
        with st.spinner("Réponse en cours..."):
            response = "Salut ! Comment puis-je vous aider ?" # Réponse simulée
            #response = get_model_response(prompt)
        
        messages.append({"role": "assistant", "content": response})
        
        st.markdown(f'<div class="chat-wrapper"><div class="bot-message">🤖 <div>{response}</div></div></div>', unsafe_allow_html=True)
        
        # Mise à jour du titre du chat
        chat_data["title"] = generate_chat_title(messages)

if __name__ == "__main__":
    __main__()
