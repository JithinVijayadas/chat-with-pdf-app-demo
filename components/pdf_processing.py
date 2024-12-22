import tempfile
from langchain.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings

def process_pdf(uploaded_file, api_key):
    """
    Processes the uploaded PDF file and creates a retriever for question-answering.
    
    Args:
        uploaded_file (UploadedFile): The uploaded PDF file.
        api_key (str): The API key for accessing the OpenAI API.
    
    Returns:
        retriever (Retriever): The retriever for the processed PDF content.
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(uploaded_file.getbuffer())
        temp_file_path = temp_file.name

    loader = PyPDFLoader(temp_file_path)
    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200, separators=["\n\n", "\n"])
    splits = text_splitter.split_documents(docs)
    if not splits:
        return None
    embeddings = OpenAIEmbeddings(api_key=api_key)
    vectorstore = FAISS.from_documents(documents=splits, embedding=embeddings)
    retriever = vectorstore.as_retriever()

    return retriever