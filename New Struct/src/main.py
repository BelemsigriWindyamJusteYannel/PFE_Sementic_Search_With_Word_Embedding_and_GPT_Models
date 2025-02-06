import streamlit as st

st.title("Renseignement")

# Where we will store questions history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Now were will display our history in the interface
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# User input
if prompt:=st.chat_input("what's up?"):
    # Were're going to display user message in the interface
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # We will add the user message to the history
    st.session_state.messages.append({"role":"user","content":prompt})

    response = f"Echo : {prompt}"
    # We are now about to display the response
    with st.chat_message("assistart"):
        st.markdown(response)
    
    # Finally we will add to the history the response
    st.session_state.messages.append({"role":"assistant","content":response})