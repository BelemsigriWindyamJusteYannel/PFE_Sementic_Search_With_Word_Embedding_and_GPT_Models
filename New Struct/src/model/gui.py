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

# Initialisation des conversations
if "chats" not in st.session_state:
    st.session_state.chats = {}
if "chat_titles" not in st.session_state:  # Stocker les titres des conversations
    st.session_state.chat_titles = {}
if "current_chat" not in st.session_state:
    chat_id = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.chats[chat_id] = []
    st.session_state.chat_titles[chat_id] = "Nouvelle conversation"
    st.session_state.current_chat = chat_id

# Fonction pour mettre à jour le titre du chat
def update_chat_title(chat_id):
    messages = st.session_state.chats[chat_id]
    if messages:
        first_user_message = next((msg["content"] for msg in messages if msg["role"] == "user"), None)
        if first_user_message:
            title = " ".join(first_user_message.split()[:5]) + ("..." if len(first_user_message.split()) > 5 else "")
            st.session_state.chat_titles[chat_id] = title
    else:
        st.session_state.chat_titles[chat_id] = "Nouvelle conversation"

# Fonction principale
def __main__():
    st.markdown("<h1 class='fixed-title'>ESTF: Règlement des Évaluations📚</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    #Sidebar : Historique des conversations
    with st.sidebar:
        st.subheader("Historique des recherches")

        # 🆕 Bouton pour un nouveau chat
        if st.button("Nouveau Chat"):
            chat_id = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.session_state.chats[chat_id] = []
            st.session_state.chat_titles[chat_id] = "Nouvelle conversation"
            st.session_state.current_chat = chat_id

        # 📂 Liste des anciens chats avec leur titre
        for chat_id, title in sorted(st.session_state.chat_titles.items(), key=lambda x: x[0], reverse=True):
            if st.button(title):
                st.session_state.current_chat = chat_id

    # Vérification et sélection du chat courant
    if st.session_state.current_chat is None:
        return

    # Initialisation du chat courant s'il n'existe pas
    if st.session_state.current_chat not in st.session_state.chats:
        st.session_state.chats[st.session_state.current_chat] = []

    # 📜 Affichage de l'historique des messages
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    for msg in st.session_state.chats[st.session_state.current_chat]:
        if msg["role"] == "user":
            st.markdown(f'<div class="chat-wrapper"><div class="user-message"> <div>{msg["content"]}</div> 🧑 </div></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-wrapper"><div class="bot-message">🤖 <div>{msg["content"]}</div></div></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 💬 Entrée utilisateur
    prompt = st.chat_input("Entrer votre requête...")
    if prompt:
        # 📝 Ajout du message utilisateur
        st.session_state.chats[st.session_state.current_chat].append({"role": "user", "content": prompt})
        st.markdown(f'<div class="chat-wrapper"><div class="user-message"> <div>{prompt}</div> 🧑 </div></div>', unsafe_allow_html=True)

        # 🔄 Mise à jour du titre du chat
        update_chat_title(st.session_state.current_chat)

        # 🤖 Simulation de la réponse de l'IA
        with st.spinner("Réponse en cours..."):
            #response = "Salut ! Comment puis-je vous aider ?"  # Réponse simulée
            response = get_model_response(prompt)  # Appel réel à  l'API LMStudio. 
        # 📝 Ajout de la réponse du bot
        st.session_state.chats[st.session_state.current_chat].append({"role": "assistant", "content": response})
        st.markdown(f'<div class="chat-wrapper"><div class="bot-message">🤖 <div>{response}</div></div></div>', unsafe_allow_html=True)

if __name__ == "__main__":
    __main__()
