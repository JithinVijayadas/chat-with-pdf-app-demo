import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from components.pdf_processing import process_pdf

def handle_chat(uploaded_file, api_key):
    """
    Handles the chat functionality for the uploaded PDF file.
    
    Args:
        uploaded_file (UploadedFile): The uploaded PDF file.
        api_key (str): The API key for accessing the OpenAI API.
    """
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []

    if "rag_chain" not in st.session_state:
        st.session_state.rag_chain = None
    if uploaded_file:
        with st.spinner("Processing the uploaded PDF... Please wait."):
            retriever = process_pdf(uploaded_file, api_key)
            if not retriever:
                st.error("Couldn't detect any text in the PDF. Try another PDF.")
                return
    llm = ChatOpenAI(model="gpt-4", api_key=api_key)
    prompt_template = (
        "You are an assistant for question-answering tasks. Use the context and the "
        "conversation history below to answer the question. If you don't know the answer, "
        "say that you don't know. Use three sentences maximum and keep the answer concise.\n\n"
        "{context}\n\n"
        "Conversation History:\n{history}\n\n"
        "New Question: {input}"
    )

    def ask_question(input_question):
        """
        Asks a question to the chat model and handles the response.
        
        Args:
            input_question (str): The question asked by the user.
        
        Returns:
            str: The answer generated by the chat model.
        """
        with st.spinner("Generating the answer... Please wait."):
            st.session_state.conversation_history.append({"role": "user", "content": input_question})
            formatted_history = "\n".join(
                f"{entry['role']}: {entry['content']}" for entry in st.session_state.conversation_history
            )
            prompt = ChatPromptTemplate.from_template(prompt_template)
            question_answer_chain = create_stuff_documents_chain(llm, prompt)
            st.session_state.rag_chain = create_retrieval_chain(retriever, question_answer_chain)
            result = st.session_state.rag_chain.invoke({
                "input": input_question,
                "history": formatted_history
            })
            st.session_state.conversation_history.append({"role": "assistant", "content": result["answer"]})
        return result["answer"]

    for message in st.session_state.conversation_history:
        if message["role"] == "user":
            st.chat_message("user").write(message["content"])
        else:
            st.chat_message("assistant").write(message["content"])

    user_input = st.chat_input("Ask a question about the PDF")
    if user_input:
        st.chat_message("user").write(user_input)
        answer = ask_question(user_input)
        st.chat_message("assistant").write(answer)