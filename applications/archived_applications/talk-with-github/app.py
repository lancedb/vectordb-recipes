from chat_retreival import retrieverSetup, chat

import streamlit as st


@st.cache_resource
def loading_urls(query):
    # Setting Up Reteriver
    qa = retrieverSetup(query)
    return qa


st.header("Talk with Github Codespaces", divider="green")

query_wiki = st.text_input("Enter Topic")
if query_wiki:
    # Chat Agent getting ready
    qa = loading_urls(query_wiki)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Enter Prompt"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Display assistant response in chat message container
    response = chat(qa, prompt)
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
