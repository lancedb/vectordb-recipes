import streamlit as st
from main import build_RAG
from gen_image import generate_image, RESPONSE_TO_DIFFUSER_PROMPT
from llama_index.core import Settings


def add_to_session(key, value):
    st.session_state[key] = value


def main():
    st.title("Databricks DBRX Website Bot")
    if st.session_state.get("query_engine") is None:
        context = st.text_area(
            "Enter the link to the context",
            value="https://harrypotter.fandom.com/wiki/Hogwarts_School_of_Witchcraft_and_Wizardry",
        )
        illustrate = st.checkbox("Illustrate")
        steps = st.selectbox("Select the number of steps for diffusion", (1, 2))
        build_rag = st.button("Build RAG")
        query_engine, model = None, None
        if build_rag:
            query_engine, model, _ = build_RAG(
                context,
                "mixedbread-ai/mxbai-embed-large-v1",
                "~/tmp/lancedb_hogwarts_12",
                False,
                illustrate,
                "sdxl",
            )
            add_to_session("query_engine", query_engine)
            add_to_session("model", model)
            add_to_session("steps", steps or 1)
            add_to_session("illustrate", illustrate)
            print("steps", steps)
            st._experimental_rerun()
    else:
        query_engine = st.session_state["query_engine"]
        model = st.session_state["model"]
        steps = st.session_state["steps"]
        illustrate = st.session_state["illustrate"]
        col1, col2 = st.columns(2)
        with col1:
            query = st.text_input(
                "Enter a question",
                value="What is Hogwarts?",
                label_visibility="collapsed",
            )
        with col2:
            enter = st.button("Enter")
            if enter:
                response = query_engine.chat(query)
                if illustrate:
                    with col1:
                        st.write("Response")
                        st.write(response.response)
                    with col2:
                        st.write("Illustration")
                        with st.spinner("waiting"):
                            image = generate_image(
                                model,
                                steps,
                                Settings.llm.complete(
                                    RESPONSE_TO_DIFFUSER_PROMPT.format(
                                        str(response.response)
                                    )
                                ).text,
                            )
                        st.image(image)
                else:
                    st.write("Response")
                    st.write(response)


if __name__ == "__main__":
    main()
