import sys
from helper_functions import audio_to_translated_audio

if __name__ == "__main__":
  filename = sys.argv[1]	
  extension = sys.argv[2]
  to_code = sys.argv[3]
  out_filepath = sys.argv[4]
  
  audio_to_translated_audio(f'{filename}.{extension}', to_code=to_code, out_filepath=out_filepath)
  