import streamlit as st

def display_ui():
    """
    Displays the UI for uploading a PDF file.
    
    Returns:
        uploaded_file (UploadedFile): The uploaded PDF file, or None if no file is uploaded or the file exceeds the size limit.
    """
    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")
    if uploaded_file:
        if uploaded_file.size > 2 * 1024 * 1024:  # 2 MB limit
            st.error("The uploaded file exceeds the 2 MB size limit. Please upload a smaller file.")
            uploaded_file = None
    return uploaded_file