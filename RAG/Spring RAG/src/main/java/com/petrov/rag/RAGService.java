package com.petrov.rag;

import org.springframework.stereotype.Service;

import org.springframework.ai.ollama.OllamaChatModel;

import org.springframework.ai.chat.prompt.Prompt;
import org.springframework.ai.chat.model.ChatResponse;

import org.springframework.beans.factory.annotation.Autowired;

@Service
public class RAGService {

    // Assuming you want to use Ollama. If not you can choose your desired chat model.
    private final OllamaChatModel chatClient;

    @Autowired
    public RAGService(final OllamaChatModel chatClient) {
        this.chatClient = chatClient;
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