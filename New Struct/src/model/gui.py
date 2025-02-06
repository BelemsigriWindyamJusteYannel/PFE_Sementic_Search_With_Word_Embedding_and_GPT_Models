import streamlit as st
from model import get_model_response
import datetime

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
    # Créer automatiquement un chat au démarrage
    chat_id = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.chats[chat_id] = []
    st.session_state.current_chat = chat_id

# Fonction principale
def __main__():
    st.markdown("<h1 class='fixed-title'>ESTF: Règlement des Évaluations📚</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar pour l'historique et nouveau chat
    with st.sidebar:
        st.subheader("Historique des conversations")
        
        # Bouton pour démarrer un nouveau chat
        if st.button("🆕 Nouveau Chat"):
            chat_id = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.session_state.chats[chat_id] = []
            st.session_state.current_chat = chat_id
        
        # Affichage des anciens chats et sélection d'un chat
        for chat_id in sorted(st.session_state.chats.keys(), reverse=True):
            if st.button(chat_id):
                st.session_state.current_chat = chat_id
    
    # Vérification et sélection du chat courant
    if st.session_state.current_chat is None:
        return
    
    # Initialisation du chat courant s'il n'existe pas
    if st.session_state.current_chat not in st.session_state.chats:
        st.session_state.chats[st.session_state.current_chat] = []
    
    # Affichage de l'historique des messages
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for msg in st.session_state.chats[st.session_state.current_chat]:
        if msg["role"] == "user":
            st.markdown(f'<div class="chat-wrapper"><div class="user-message"> <div>{msg["content"]}</div> 🧑 </div></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-wrapper"><div class="bot-message">🤖 <div>{msg["content"]}</div></div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Entrée utilisateur
    prompt = st.chat_input("Entrer votre requête...")
    if prompt:
        # Ajout du message utilisateur à l'historique
        st.session_state.chats[st.session_state.current_chat].append({"role": "user", "content": prompt})
        
        st.markdown(f'<div class="chat-wrapper"><div class="user-message"> <div>{prompt}</div> 🧑 </div></div>', unsafe_allow_html=True)
        
        # Envoi de la requête à l'API (simulation ici)
        with st.spinner("Réponse en cours..."):
          #response = get_model_response(prompt)  # Appel réel à votre API
           response = "Salut ! Comment puis-je vous aider ?" # Réponse simulée
        # Ajout de la réponse à l'historique
        st.session_state.chats[st.session_state.current_chat].append({"role": "assistant", "content": response})
        
        st.markdown(f'<div class="chat-wrapper"><div class="bot-message">🤖 <div>{response}</div></div></div>', unsafe_allow_html=True)

if __name__ == "__main__":
    __main__()
