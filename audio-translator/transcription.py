import assemblyai as aai
from exceptions import TranscriptionError
from config import ASSEMBLY_AI_KEY, SUPPORTED_LANGUAGES_BEST_MODEL

aai.settings.api_key = ASSEMBLY_AI_KEY

def detect_audio_language(transcriber, audio):
    try:
        config = aai.TranscriptionConfig(
            audio_end_at=60000,
            language_detection=True,
            speech_model=aai.SpeechModel.nano
        )
        transcript = transcriber.transcribe(audio, config=config)
        return [transcript.json_response["language_code"], transcript.json_response["language_confidence"]]
    except Exception as e:
        print(f'Error detecting audio language: {e}')
        raise TranscriptionError(f'Transcription error: {e}')

def determine_model(language_code):
    try:
        if language_code in SUPPORTED_LANGUAGES_BEST_MODEL:
            return aai.SpeechModel.best
        return aai.SpeechModel.nano
    except Exception as e:
        print(f'Error determining model for language {language_code}: {e}')
        raise TranscriptionError(f'Transcription error: {e}')

def transcribe_audio(transcriber, audio, model, code):
    try:
        config = aai.TranscriptionConfig(
            language_code=code,
            speech_model=model
        )
        transcript = transcriber.transcribe(audio, config=config)
        return transcript, code
    except Exception as e:
        print(f'Error transcribing audio with model {model} and code {code}: {e}')
        raise TranscriptionError(f'Transcription error: {e}')

def audio_to_text(audio):
    try:
        transcriber = aai.Transcriber()
        language_code, confidence = detect_audio_language(transcriber, audio)
        print(f'Detected language {language_code} with {(confidence*100):.2f}% confidence')
        model = determine_model(language_code)
        print(f'Chosen model: {model}')
        return transcribe_audio(transcriber, audio, model, language_code)
    except Exception as e:
        print(f'Error processing audio to text: {e}')
        raise TranscriptionError(f'Transcription error: {e}')
