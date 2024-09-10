package com.petrov.rag;

import java.util.List;

import java.io.IOException;

import org.springframework.stereotype.Service;

import org.springframework.ai.document.Document;
import org.springframework.ai.chat.model.ChatModel;

import com.petrov.rag.readers.MyTikaDocumentReader;

import org.springframework.ai.vectorstore.VectorStore;
import org.springframework.ai.embedding.EmbeddingModel;
import org.springframework.beans.factory.annotation.Autowired;;

@Service
public class RAGService {
    
    private final ChatModel chatModel; 
    private final VectorStore vectorStore;
    private final EmbeddingModel embeddingModel;
    private final MyTikaDocumentReader dataReader;

    @Autowired
    public RAGService(final ChatModel chatModel, final VectorStore vectorStore, 
            final EmbeddingModel embeddingModel, final MyTikaDocumentReader dataReader) {
        this.chatModel = chatModel;
        this.vectorStore = vectorStore;
        this.embeddingModel = embeddingModel;
        this.dataReader = dataReader;
    }

    public List<Document> getData() throws IOException {
        return dataReader.extractFilesData();
    }

    // @PostConstruct
    // public void init() {
    //     String pdfData = "";
    //     try {
    //         pdfData = extractPdfData();
    //     } catch(final IOException ioe) {
    //         throw new RuntimeException(String.format("Failed to extract data from knowledge base - %s!", ioe.getMessage()));          
    //     }
    //     model.call(new EmbeddingRequest(List.of("Hi", "Hello"), OllamaOptions.builder().withModel))
    //     // TODO: store into vector db
    // }
    
    // public String promptChatClient(final String userInput) {
    //     final ChatResponse chatResponse = chatClient.call(
    //             new Prompt(
    //                 userInput
    //             )
    //     );
    //     return chatResponse.getResult().getOutput().getContent();
    // }

    // private String extractPdfData() throws IOException {
    //     return pdfReader.extractFilesData();
    // }

}