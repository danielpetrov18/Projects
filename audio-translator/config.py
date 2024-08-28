import os
from dotenv import load_dotenv

load_dotenv() # Loads all the environment variables

ASSEMBLY_AI_KEY = os.getenv('ASSEMBLY_AI_KEY') # Make sure you have an existing API key and also set it in the docker-compose.yml

# Those are all the languages supported by the best model. The nano model does support more, however it's not as efficient
SUPPORTED_LANGUAGES_BEST_MODEL = (
    'en',
    'es',
    'fr',
    'de',
    'it',
    'pt',
    'nl',
    'hi',
    'ja',
    'zh',
    'fi',
    'ko',
    'pl',
    'ru',
    'tr',
    'uk',
    'vi'
)

# Because translation of large texts can lead to an error the text gets split into chunks
TRANSLATION_TEXT_CHUNK = 500