from .common_imports import *
def utility_function_1():
    success = load_dotenv()
    if not success:
        raise FileNotFoundError("Could not find .env file.")
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY environment variable is missing")
    openai_engine = os.environ.get("OPENAI_ENGINE", "text-davinci-003")

    nltk.download("punkt")
    pickle_directory = os.getenv("PICKLE_DIRECTORY")
    if not pickle_directory:
        raise ValueError("PICKLE_DIRECTORY environment variable is missing")

    logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    return pickle_directory, openai_api_key
