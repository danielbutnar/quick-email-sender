from .common_imports import *

def load_environment_variables():
    """
    Load environment variables.

    Raises:
        FileNotFoundError: If the .env file is not found.
        ValueError: If the OPENAI_API_KEY or PICKLE_DIRECTORY environment variables are missing.

    Returns:
        tuple: A tuple containing the pickle_directory (str) and the openai_api_key (str).
    """
    success = load_dotenv()
    if not success:
        raise FileNotFoundError("Could not find .env file.")
    
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY environment variable is missing")
    
    pickle_directory = os.getenv("PICKLE_DIRECTORY")
    if not pickle_directory:
        raise ValueError("PICKLE_DIRECTORY environment variable is missing")

    return pickle_directory, openai_api_key

def setup_resources_and_logging():
    """
    Download required resources and set up logging.
    """
    nltk.download("punkt")

    logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def utility_function_1():
    """
    Load environment variables, download required resources, and set up logging.

    Returns:
        tuple: A tuple containing the pickle_directory (str) and the openai_api_key (str).
    """
    pickle_directory, openai_api_key = load_environment_variables()
    setup_resources_and_logging()

    return pickle_directory, openai_api_key
