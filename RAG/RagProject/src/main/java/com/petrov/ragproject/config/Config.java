package com.petrov.ragproject.config;

import javax.sql.DataSource;

import org.springframework.ai.chat.model.ChatModel;
import org.springframework.ai.chat.client.ChatClient;

import org.springframework.jdbc.core.JdbcTemplate;

import org.springframework.boot.jdbc.DataSourceBuilder;

import org.springframework.ai.embedding.EmbeddingModel;

import org.springframework.ai.vectorstore.VectorStore;
import org.springframework.ai.vectorstore.PgVectorStore;

import org.springframework.beans.factory.annotation.Value;

import org.springframework.ai.ollama.api.OllamaApi;
import org.springframework.ai.ollama.OllamaChatModel;
import org.springframework.ai.ollama.api.OllamaOptions;
import org.springframework.ai.ollama.OllamaEmbeddingModel;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

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

    @Value("${spring.datasource.url}")
    private String dbUrl;

    @Value("${spring.datasource.username}")
    private String dbUsername;

    @Value("${spring.datasource.password}")
    private String dbPassword;

    @Bean
    public OllamaApi ollamaApi() {
        return new OllamaApi(ollamaBaseUrl);
    }

    @Bean
    public ChatModel ollamaChatModel(final OllamaApi ollamaApi) {
        return new OllamaChatModel(
            ollamaApi, 
            OllamaOptions.builder().withModel(ollamaChatModel).withTemperature(ollamaChatTemperature).build()
        );
    }

    @Bean
    public ChatClient chatClient(final ChatModel ollamaChatModel) {
        return ChatClient.create(ollamaChatModel);
    }   

    @Bean
    public EmbeddingModel ollamaEmbeddingModel(final OllamaApi ollamaApi) {
        return new OllamaEmbeddingModel(
            ollamaApi, 
            OllamaOptions.builder().withModel(ollamaEmbeddingModel).build()
        );
    }

    @Bean
    public DataSource dataSource() {
        return DataSourceBuilder
                .create()
                    .url(dbUrl)
                    .username(dbUsername)
                    .password(dbPassword)
                .build();
    }

    @Bean
    public JdbcTemplate jdbcTemplate(final DataSource dataSource) {
        return new JdbcTemplate(dataSource);
    }

    @Bean
    public VectorStore vectorStore(final JdbcTemplate jdbcTemplate, final EmbeddingModel embeddingModel) {
        return new PgVectorStore(jdbcTemplate, embeddingModel);
    }

}