from translate import Translator
from exceptions import TranslationError
from config import TRANSLATION_TEXT_CHUNK

def translate_text(original_text, from_lang, to_lang) -> str:
    try:
        translator = Translator(from_lang=from_lang, to_lang=to_lang)
        print(f'Translating text from {from_lang} to {to_lang}')
        # The translation is done in chunks as to avoid errors with larger texts
        translation = ''
        for i in range(0, len(original_text), TRANSLATION_TEXT_CHUNK): 
            chunk = original_text[i:i + TRANSLATION_TEXT_CHUNK]
            translated_chunk = translator.translate(chunk)
            translation += translated_chunk
        return translation
    except Exception as e:
        print(f'Error translating text from {from_lang} to {to_lang}: {e}')
        raise TranslationError(f'Translation error: {e}')
