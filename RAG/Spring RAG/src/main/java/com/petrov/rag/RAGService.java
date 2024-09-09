package com.petrov.rag;

import java.io.IOException;

import org.springframework.stereotype.Service;

import org.springframework.ai.chat.prompt.Prompt;
import org.springframework.ai.ollama.OllamaChatModel;
import org.springframework.ai.chat.model.ChatResponse;

import org.springframework.beans.factory.annotation.Autowired;

@Service
public class RAGService {

    private final PdfReader pdfReader;
    // Assuming you want to use Ollama. If not you can choose your desired chat model.
    private final OllamaChatModel chatClient;

    @Autowired
    public RAGService(final PdfReader pdfReader, final OllamaChatModel chatClient) {
        this.pdfReader = pdfReader;
        this.chatClient = chatClient;
    }

    public String extractPdfData() {
        try {
            return pdfReader.extractFilesData();
        } catch(final IOException ioe) {
            return String.format("Failed to extract data from knowledge base - %s!", ioe.getMessage());            
        }
    }

    public String promptChatClient(final String userInput) {
        final ChatResponse chatResponse = chatClient.call(
                new Prompt(
                    userInput
                )
        );
        return chatResponse.getResult().getOutput().getContent();
    }

}