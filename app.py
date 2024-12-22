import streamlit as st
from components.ui import display_ui
from components.chat import handle_chat
from utils.config import get_api_key

def main():
    """
    Main function to run the Streamlit app.
    Displays the title and handles the PDF upload and chat functionality.
    """
    st.title("Chat with your PDF")
    st.markdown('<h3>Demo by <span style="color: green;">JITHIN V</span></h3>', unsafe_allow_html=True)

    api_key = get_api_key()
    uploaded_file = display_ui()

    if uploaded_file and api_key:
        handle_chat(uploaded_file, api_key)

if __name__ == "__main__":
    main()