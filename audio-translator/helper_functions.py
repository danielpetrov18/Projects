import constants
from gtts import gTTS
import assemblyai as aai
from playsound import playsound
from translate import Translator

aai.settings.api_key = ''

# Source: https://www.assemblyai.com/docs/guides/automatic-language-detection-workflow
def detect_audio_language(transcriber, audio):
    config = aai.TranscriptionConfig(
        audio_end_at=60000,  # first 60 seconds (in milliseconds)
        language_detection=True,
        speech_model=aai.SpeechModel.nano  # Supports more languages than Best and is cheaper
    )
    transcript = transcriber.transcribe(audio, config=config)
    return [transcript.json_response["language_code"], transcript.json_response["language_confidence"]]

def determine_model(language_code):
    if language_code in constants.SUPPORTED_LANGUAGES_BEST_MODEL:
        return aai.SpeechModel.best
    return aai.SpeechModel.nano

def transcribe_audio(transcriber, audio, model, code):
    config = aai.TranscriptionConfig(
        language_code=code,
        speech_model=model
    )
    transcript = transcriber.transcribe(audio, config=config)
    return transcript, code

def audio_to_text(audio):
    transcriber = aai.Transcriber()
  
    language_code, confidence = detect_audio_language(transcriber, audio)
    print(f'Detected language {language_code} with {(confidence*100):.2f}% confidence ...')
    
    model = determine_model(language_code)
    print(f'Chosen model: {model}')
    
    return transcribe_audio(transcriber, audio, model, language_code)

def translate_text(original_text, from_lang, to_lang):
    translator = Translator(from_lang=from_lang, to_lang=to_lang)
    print(f'Translator translates from {from_lang} to {to_lang}')
    
    translation = ''
    for i in range(0, len(original_text), constants.TRANSLATION_TEXT_CHUNK): # From start to end with a step size of 500
        chunk = original_text[i:i + constants.TRANSLATION_TEXT_CHUNK]
        translated_chunk = translator.translate(chunk)
        translation += translated_chunk
    
    return translation

def text_to_audio(text, lang, out_filepath):
    tts = gTTS(text=text, lang=lang, lang_check=True)
    tts.save(savefile=out_filepath)

def audio_to_translated_audio(audio, to_code, out_filepath='translated.mp3'):
    # 1. Convert audio to text
    try:
        transcript, from_code = audio_to_text(audio)
    except Exception as e:
        print(f'Error transcribing audio: {e}')
        exit(1)
        
    if transcript.status == aai.TranscriptStatus.error:
        raise Exception(transcript.error)
    
    # 2. Translate text
    try:
        translated_text = translate_text(transcript.text, from_lang=from_code, to_lang=to_code)
        print(f'Translated text: {translated_text}')
    except Exception as e:
        print(f'Error translating text: {e}')
        raise Exception(e)
    
    # 3. Create translated text audio   
    try: 
        text_to_audio(translated_text, to_code, out_filepath)   
        playsound(out_filepath)	
    except AssertionError as ae:
        print(f'Error: {ae}')
        exit(1)
    except ValueError as ve:
        print(f'Error: {ve}')
        exit(1)
    except RuntimeError as re:
        print(f'Error: {re}')
        exit(1)
    except Exception as e:
        print(f'Error: {e}')
        exit(1)
        