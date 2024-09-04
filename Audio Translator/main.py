import gradio as gr
from gradio_interface import create_gradio_interface

if __name__ == '__main__':
    translator_app = create_gradio_interface()
    
    try:
        translator_app.launch(server_name='0.0.0.0', server_port=7860)
    except gr.Error as gre:
        print(f'Gradio error: {gre}')
    except Exception as e:
        print(f'Unexpected error: {e}')