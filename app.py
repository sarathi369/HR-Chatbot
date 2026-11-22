
import streamlit as st
from src.rag_pipeline import generate_answer

st.set_page_config(
    page_title="HR Policy Assistant",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 HR Policy Assistant")

st.write(
    "Welcome! Ask me questions about company HR policies "
    "and procedures."
)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept employee question
if question := st.chat_input("Ask your HR question..."):

    # Display user question
    st.chat_message("user").markdown(question)

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    # Generate chatbot response
    with st.chat_message("assistant"):
        with st.spinner("Searching HR documents..."):
            try:
                answer = generate_answer(question)
                st.markdown(answer)

            except Exception as e:
                answer = (
                    "Sorry, I encountered an error while processing "
                    "your question. Please try again."
                )
                st.error(answer)
                print("Error:", e)

    # Save assistant response in chat history
    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })
