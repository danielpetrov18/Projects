import gradio as gr
from config import SUPPORTED_LANGUAGES_BEST_MODEL
from audio_processing import audio_to_translated_audio

'''
    The gradio interface takes 3 arguments.
        1. First one is the target function
        2. The input/s (Check out different types of inputs in the gradio docs)
        3. The output/s 
'''
def create_gradio_interface():
    interface = gr.Interface(
        fn=audio_to_translated_audio,
        inputs=[
            # It currently has support only for microphone. Can be extended to file upload.
            gr.Audio(sources=["microphone"], type="filepath", label="Record your audio"),
            gr.Dropdown(choices=SUPPORTED_LANGUAGES_BEST_MODEL, label="Select Target Language")
        ],
        outputs=gr.Audio(label="Translated Audio")
    )
    return interface
