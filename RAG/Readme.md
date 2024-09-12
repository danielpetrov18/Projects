# Project: RAG System with Spring AI and Ollama Models

This project uses **Spring AI**, **vector stores**, and **Ollama** models to enhance **LLMs** (Large Language Models) for document-based question-answering. It leverages the **llama3.1:8b** and **nomic-embed-text:v1.5** models. The system can process various document types (MD, PPTX, DOCX, TXT, PDFs) and uses retrieval-augmented generation (RAG) to search for relevant information in vectorized documents to generate more accurate AI responses.

## Prerequisites

- **Docker** and **Docker Compose** installed on your system.
- A working **Java** environment (JDK 17+).

## Setup

### Step 1: Create the Knowledge Base Folder

1. In the root of the project, create a folder called `knowledge_base`.
2. Upload the files (MD, PPTX, DOCX, TXT, and PDFs) you want to include in your vector store into this folder. These documents will be processed and used by the RAG system to answer user queries.

### Step 2: Run Docker Compose

1. Navigate to the root folder of the project.
2. Run the following command to spin up the necessary services:

    ```bash
    docker-compose up
    ```

### Step 3: Install the Models in Ollama

After running `docker-compose up`, the **Ollama** container will be running. To install the required models:

1. Access the running container:

    ```bash
    docker exec -it ollama /bin/bash
    ```

2. Pull the models:

    ```bash
    ollama pull llama3.1:8b
    ollama pull nomic-embed-text:v1.5
    ```

### Step 4: Sending a Query

Once the models are installed and the services are up, you can make GET requests to interact with the system. Replace `[users query]` with your query.

```bash
http://localhost:8080/api/v1/prompt/?query=[users query]
