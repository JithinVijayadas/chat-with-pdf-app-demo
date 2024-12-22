import os

def get_api_key():
    """
    Retrieves the API key from environment variables.
    
    Returns:
        str: The API key.
    """
    return os.getenv("API_KEY")