import constants
import assemblyai as aai
from translate import Translator

# Set your AssemblyAI API key
aai.settings.api_key = ''

# Source: https://www.assemblyai.com/docs/guides/automatic-language-detection-workflow
def detect_language(transcriber, audio):
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
  
    language_code, confidence = detect_language(transcriber, audio)
    print(f'Detected language {language_code} with {(confidence*100):.2f}% confidence level ...')
    
    model = determine_model(language_code)
    print(f'Chosen model: {model}')
    
    return transcribe_audio(transcriber, audio, model, language_code)

def translate_text(original_text, from_lang='en', to_lang='en'):
    print(f'Translator translates from {from_lang} to {to_lang}')
    translator = Translator(from_lang=from_lang, to_lang=to_lang)
    translation = translator.translate(original_text)
    return translation

def audio_to_translated_audio(audio, to_code='en'):
    # 1. Convert audio to text
    transcript, from_code = audio_to_text(audio)
    
    if transcript.status == aai.TranscriptStatus.error:
        raise Exception(transcript.error)
    
    audio_text = transcript.text

    # 2. Translate text
    try:
        translated_text = translate_text(audio_text, from_lang=from_code, to_lang=to_code)
        print(f'Translated text: {translated_text}')
    except Exception as e:
        print(f'Error translating text: {e}')
        raise Exception(e)
    
    # 3. Create translated text audio    
    