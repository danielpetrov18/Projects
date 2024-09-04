# Audio Translator

Welcome to the Audio Translator project! This application translates audio recordings from one language to another using a combination of speech-to-text, translation, and text-to-speech technologies. It's designed to be simple to deploy using Docker, making it easy to run in various environments.

## Features

- **Speech-to-Text:** Converts spoken audio into written text.
- **Translation:** Translates the text into a target language.
- **Text-to-Speech:** Converts the translated text back into spoken audio.

## Getting Started

To get started with the Audio Translator application, follow these steps:

### Prerequisites

1. **Docker:** Ensure you have Docker installed on your machine. You can download and install Docker from [Docker's official website](https://www.docker.com/get-started).

2. **AssemblyAI API Key:** Sign up on the [AssemblyAI website](https://www.assemblyai.com/) to generate an API key. This API key is required for the speech-to-text and text-to-speech functionalities.

### Setup
1. **Configure API Key:**

    Open the `docker-compose.yml` file and set your AssemblyAI API key:

    ```yaml
    version: '3.9'

    services:
      audio-translator:
        build: .
        container_name: audio-translator
        ports:
          - '7860:7860'
        environment:
          - ASSEMBLY_AI_KEY=your_assemblyai_api_key_here
    ```

3. **Build and Run the Application:**

    Use Docker Compose to build and run the application:

    ```bash
    docker-compose up
    ```

    This will build the Docker image, create a container, and start the application. The service will be available at `http://localhost:7860`.

### Usage

Once the container is up and running, you can interact with the application via the exposed web interface. You can record a short audio using your microphone, then specify the target language, and receive the translated audio.

### Notes

- **File Structure:** Ensure your project directory contains the necessary files, including `Dockerfile`, `docker-compose.yml`, and `requirements.txt`.
- **Dependencies:** The application relies on the following Python packages, which are listed in `requirements.txt`:
  - `gradio`
  - `gTTS`
  - `assemblyai`
  - `translate`
  - `python-dotenv`

### Troubleshooting

- **Error: `Cannot load audio from file: ffprobe not found`**  
  Ensure that `ffmpeg` is installed on your system and properly configured.

- **Error: `ModuleNotFoundError`**  
  Verify that all dependencies are correctly listed in `requirements.txt` and installed in your Docker container.

### Contributing

Feel free to contribute to this project by submitting issues, proposing improvements, or making pull requests.

---

Happy translating! 🚀
