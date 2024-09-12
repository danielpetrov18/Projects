package com.petrov.ragproject.utility;

import java.util.Map;
import java.util.List;
import java.util.HashMap;
import java.util.ArrayList;

import java.io.IOException;

import com.google.common.hash.Hashing;

import jakarta.annotation.PostConstruct;

import java.nio.charset.StandardCharsets;

import org.apache.logging.log4j.Logger;
import org.apache.logging.log4j.LogManager;

import org.springframework.stereotype.Component;

import org.springframework.beans.factory.annotation.Autowired;

import org.springframework.ai.document.Document;
import org.springframework.ai.vectorstore.VectorStore;
import org.springframework.ai.transformer.splitter.TokenTextSplitter;

import org.springframework.jdbc.core.namedparam.NamedParameterJdbcTemplate;

@Component
public class Loader {
    
    private final VectorStore vectorStore;
    private final MyTikaDocumentReader dataReader;
    private final NamedParameterJdbcTemplate jdbcTemplate;
    private final Logger LOGGER = LogManager.getLogger(this.getClass());

    @Autowired
    public Loader(final VectorStore vectorStore, final MyTikaDocumentReader dataReader, final NamedParameterJdbcTemplate jdbcTemplate) {
        this.vectorStore = vectorStore;
        this.dataReader = dataReader;
        this.jdbcTemplate = jdbcTemplate;
    }

    @PostConstruct
    public void init() {
        processDocuments(); 
    }

    private void processDocuments() {
        List<Document> folderData;
        try {
            folderData = dataReader.extractFilesData();
            LOGGER.debug("** LOADED DATA INTO MEMORY **");
        }
        catch (final IOException ioe) {
            throw new RuntimeException("Failed loading data from folder: " + ioe.getMessage());
        }

        final List<Document> tokens = new TokenTextSplitter().apply(folderData);
        LOGGER.debug("** TOKENIZED DATA **");

        // Relevant for avoiding duplicate data
        addHashToMetadata(tokens);

        final List<Document> nonDuplicates = findNonDuplicates(tokens);
        if(!nonDuplicates.isEmpty()) {
            vectorStore.add(nonDuplicates);
        }
    }
    
    private String computeHash(final String content) {
        return Hashing
                .sha256()
                .hashString(content, StandardCharsets.UTF_8)
                .toString();
    }

    private void addHashToMetadata(final List<Document> tokens) {
        tokens.forEach(token -> {
            final String tokenContent = token.getContent();
            final String hashValue = computeHash(tokenContent);
            token.getMetadata().put("hash", hashValue);
        });
    }

    private List<Document> findNonDuplicates(final List<Document> tokens) {
        final List<Document> nonDuplicates = new ArrayList<>();
        for (final Document token : tokens) {
            final String hash = token.getMetadata().get("hash").toString();
            final Map<String, Object> metadata = new HashMap<>();
            metadata.put("hash", hash);

            final int count = jdbcTemplate.queryForObject(
                "SELECT COUNT(*) FROM vector_store WHERE metadata ->> 'hash' = :hash",
                metadata,
   Integer.class
            );

            if (count == 0) {
                nonDuplicates.add(token);
            }
        }
        return nonDuplicates;
    }

}