
import streamlit as st
import random
from streamlit_chat import message
from scripts.models_preprocess import HRChatbot

# Create an instance of the HRChatbot class
chatbot = HRChatbot("data/employee_data_akash_modified.csv", "data/hr_policy_sample.txt", "aks desai")

def process_input(user_input):
    response = chatbot.get_response(user_input)
    return response

st.header("HR Chatbot ask personal query ")
st.markdown("Ask your HR-related questions of yours.")

if "past" not in st.session_state:
    st.session_state["past"] = []
if "generated" not in st.session_state:
    st.session_state["generated"] = []

if "input_message_key" not in st.session_state:
    st.session_state["input_message_key"] = str(random.random())

chat_container = st.container()

user_input = st.text_input("Type your message and  send.", key=st.session_state["input_message_key"])

if st.button("Send"):
    response = process_input(user_input)

    st.session_state["past"].append(user_input)
    st.session_state["generated"].append(response)

    st.session_state["input_message_key"] = str(random.random())

    st.experimental_rerun()

if st.session_state["generated"]:
    with chat_container:
        for i in range(len(st.session_state["generated"])):
            message(st.session_state["past"][i], is_user=True, key=str(i) + "_user")
            message(st.session_state["generated"][i], key=str(i),
                    avatar_style="Aneka",  # change this for a different user icon
                    seed=123)
