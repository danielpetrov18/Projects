import gradio as gr
from helper_functions import audio_to_translated_audio

demo = gr.Interface(
    fn=audio_to_translated_audio,
    inputs=gr.Audio(sources=['microphone'], type='filepath'),
    outputs=gr.Audio(label='Spanish')
)

if __name__ == "__main__":
  audio_to_translated_audio('bg.mp3', to_code='de')