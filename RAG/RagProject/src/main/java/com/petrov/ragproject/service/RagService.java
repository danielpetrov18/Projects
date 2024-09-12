package com.petrov.ragproject.service;

import java.util.Map;
import java.util.List;

import java.util.stream.Collectors;

import org.apache.logging.log4j.Logger;
import org.apache.logging.log4j.LogManager;

import org.springframework.stereotype.Service;

import org.springframework.ai.document.Document;

import org.springframework.ai.chat.messages.Message;

import org.springframework.ai.chat.client.ChatClient;

import org.springframework.ai.vectorstore.VectorStore;
import org.springframework.ai.vectorstore.SearchRequest;

import org.springframework.beans.factory.annotation.Autowired;

import org.springframework.ai.chat.prompt.Prompt;
import org.springframework.ai.chat.prompt.PromptTemplate;
import org.springframework.ai.chat.prompt.SystemPromptTemplate;

@Service
public class RagService {

    private final ChatClient chatClient;
    private final VectorStore vectorStore;
    
    private final static int TOP_K = 5;
    private final static float SIMILARITY_THRESHOLD = 0.15f;
    private final Logger LOGGER = LogManager.getLogger(this.getClass());

    private final static String SYSTEM_TEXT = """
    You are a highly knowledgeable assistant designed to answer questions using the documents provided. 
    Always base your answers solely on the relevant information from the DOCUMENTS section.
    
    Your goals are to:
    - Provide precise, clear, and concise answers.
    - Avoid speculation or relying on any information outside the DOCUMENTS.
    - If the DOCUMENTS do not provide enough information to answer accurately, 
      state: "I do not have enough information to answer."

    INSTRUCTIONS:
    1. Carefully read the QUESTION and DOCUMENTS.
    2. Provide an answer based only on the DOCUMENTS.
    3. If DOCUMENTS lack sufficient information, clearly state so.
    4. Structure your response logically and explain step-by-step when necessary.
    5. If there are multiple relevant documents, synthesize the information.
    6. Do not add any personal opinions or information outside of the DOCUMENTS.
    """;

    private final static String USER_TEXT = """
    QUESTION:
    {input}

    DOCUMENTS:
    {documents}

    REMINDERS:
    - The answer must be based only on the information found in the DOCUMENTS.
    - If the DOCUMENTS do not provide enough information to answer the question, say: "I do not have enough information to answer."
    - Avoid adding any extra information that is not found in the DOCUMENTS.
    """;

    @Autowired
    public RagService(final ChatClient chatClient, final VectorStore vectorStore) {
        this.chatClient = chatClient;
        this.vectorStore = vectorStore;
    }
    
    public String promptChatClient(final String userInput) {
        LOGGER.debug("** USER INPUT: {} **", userInput);

        // Perform similarity search (context to be used in the prompt for the chat client)
        final String relevantData = findRelevantData(userInput);

        final Message systemMsg = new SystemPromptTemplate(SYSTEM_TEXT).createMessage();
        final Message userMsg = new PromptTemplate(USER_TEXT)
                                            .createMessage(Map.of("input", userInput, "documents", relevantData));
        
        return chatClient
                    .prompt(
                        new Prompt(
                                List.of(
                                    systemMsg, userMsg
                                )))
                    .call()
                    .content();
    }

    private String findRelevantData(final String prompt) {
        final List<Document> relevantDocuments = vectorStore.similaritySearch(
                                                                        SearchRequest
                                                                            .defaults()
                                                                            .withQuery(prompt)
                                                                            .withTopK(TOP_K)
                                                                            .withSimilarityThreshold(SIMILARITY_THRESHOLD)
                                                                        );                                    
        return relevantDocuments
                    .stream()
                    .map(document -> document.getContent().replace("\n", ""))
                    .collect(Collectors.joining(" "));
    }

}