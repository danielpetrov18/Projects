from gtts import gTTS
from uuid import uuid4
from pathlib import Path
import assemblyai as aai
from translation import translate_text
from transcription import audio_to_text
from exceptions import AudioGenerationError, TranscriptionError, TranslationError

def text_to_audio(text, lang, out_filepath):
    try:
        tts = gTTS(text=text, lang=lang, lang_check=True)
        tts.save(savefile=out_filepath)
    except Exception as e:
        print(f'Error generating audio for text in language {lang}: {e}')
        raise AudioGenerationError(f'Error generating audio for text in language {lang}: {e}')

def audio_to_translated_audio(audio, to_lang_code):
    try:
        transcript, from_lang_code = audio_to_text(audio)
        if transcript.status == aai.TranscriptStatus.error:
            raise TranscriptionError(f'Transcription error: {transcript.error}')
        
        # The results of both translation .txt and .mp3 files is going to be saved in this folder
        output_dir = Path('results')
        output_dir.mkdir(parents=True, exist_ok=True)
        
        out_filepath = output_dir / f'{str(uuid4())}-{from_lang_code}-{to_lang_code}' # Without extension
        
        translated_text = translate_text(transcript.text, from_lang=from_lang_code, to_lang=to_lang_code)
        with open(f'{out_filepath}.txt', 'w', encoding='utf-8') as f:
            f.write(f'Original text:\n{transcript.text}\nTranslation:\n{translated_text}')
        
        out_filepath = out_filepath.with_suffix('.mp3')
        text_to_audio(translated_text, to_lang_code, out_filepath)
        return out_filepath
    except (TranscriptionError, TranslationError, AudioGenerationError) as e:
        print(f'Error in audio to translated audio process: {e}')
        raise AudioGenerationError(f'Error in audio to translated audio process: {e}')
    except Exception as e:
        print(f'Unexpected error in audio to translated audio process: {e}')
        raise AudioGenerationError(f'Unexpected error in audio to translated audio process: {e}')
