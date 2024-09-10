package com.petrov.rag;

import org.springframework.ai.chroma.ChromaApi;
import org.springframework.ai.ollama.api.OllamaApi;
import org.springframework.ai.chat.model.ChatModel;
import org.springframework.ai.ollama.OllamaChatModel;
import org.springframework.ai.vectorstore.VectorStore;
import org.springframework.ai.embedding.EmbeddingModel;
import org.springframework.ai.ollama.api.OllamaOptions;
import org.springframework.ai.ollama.OllamaEmbeddingModel;
import org.springframework.ai.vectorstore.ChromaVectorStore;

import org.springframework.beans.factory.annotation.Value;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import org.springframework.web.client.RestClient;
import org.springframework.http.client.SimpleClientHttpRequestFactory;

@Configuration
public class Config {

    @Value("${spring.ai.ollama.base-url}")
    private String ollamaBaseUrl;

    @Value("${spring.ai.ollama.chat.options.model}")
    private String ollamaChatModel;

    @Value("${spring.ai.ollama.chat.options.temperature}")
    private float ollamaChatTemperature;

    @Value("${spring.ai.ollama.embedding.options.model}")
    private String ollamaEmbeddingModel;

    @Value("${spring.ai.vectorstore.chroma.client.host}")
    private String chromaClientHost;

    @Value("${spring.ai.vectorstore.chroma.client.port}")
    private int chromaClientPort;

    @Value("${spring.ai.vectorstore.chroma.collection-name}")
    private String chromaCollectionName;

    @Bean
    public OllamaApi ollamaApi() {
        return new OllamaApi(ollamaBaseUrl);
    }

    @Bean
    public ChatModel ollamaChatModel(final OllamaApi ollamaApi) {
        return new OllamaChatModel(
            ollamaApi, 
            OllamaOptions.builder()
                .withModel(ollamaChatModel)
                .withTemperature(ollamaChatTemperature)
                .build()
        );
    }

    @Bean
    public EmbeddingModel ollamaEmbeddingModel(final OllamaApi ollamaApi) {
        return new OllamaEmbeddingModel(
            ollamaApi, 
            OllamaOptions.builder()
                .withModel(ollamaEmbeddingModel)
                .build()
        );
    }

    @Bean
    public RestClient.Builder builder() {
        return RestClient.builder().requestFactory(new SimpleClientHttpRequestFactory());
    }

    @Bean
    public ChromaApi chromaApi(RestClient.Builder restClientBuilder) {
        final String chromaUrl = String.format("http://%s:%d", chromaClientHost, chromaClientPort);
        return new ChromaApi(chromaUrl, restClientBuilder);
    }

    @Bean
    public VectorStore chromaVectorStore(final EmbeddingModel embeddingModel, final ChromaApi chromaApi) {
        return new ChromaVectorStore(embeddingModel, chromaApi, chromaCollectionName, false);
    }

}