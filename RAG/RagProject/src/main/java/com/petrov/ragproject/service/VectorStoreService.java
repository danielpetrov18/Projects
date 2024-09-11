package com.petrov.ragproject.service;

import jakarta.annotation.PostConstruct;
import org.springframework.ai.transformer.splitter.TokenTextSplitter;
import org.springframework.ai.vectorstore.VectorStore;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.namedparam.NamedParameterJdbcTemplate;
import org.springframework.stereotype.Service;

import com.google.common.hash.Hashing;
import com.petrov.ragproject.utility.MyTikaDocumentReader;

import org.apache.logging.log4j.Logger;
import org.apache.logging.log4j.LogManager;

import org.springframework.ai.document.Document;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
public class VectorStoreService {

    private final VectorStore vectorStore;
    private final MyTikaDocumentReader dataReader;
    private final NamedParameterJdbcTemplate jdbcTemplate;

    private final Logger LOGGER = LogManager.getLogger(this.getClass());

    @Autowired
    public VectorStoreService(final VectorStore vectorStore, final MyTikaDocumentReader dataReader, final NamedParameterJdbcTemplate jdbcTemplate) {
        this.vectorStore = vectorStore;
        this.dataReader = dataReader;
        this.jdbcTemplate = jdbcTemplate;
    }

   @PostConstruct
    public void init() {
        try {
            final List<Document> folderData = dataReader.extractFilesData();
            LOGGER.debug("** LOADED DATA **");

            final TokenTextSplitter splitter = new TokenTextSplitter();
            final List<Document> tokens = splitter.apply(folderData);
            LOGGER.debug("** TOKENIZED DATA **");

            // Relevant for avoiding duplicate data
            addHashToMetadata(tokens);

            final List<Document> nonDuplicates = new ArrayList<>();
            for (final Document token : tokens) {
                final String hash = token.getMetadata().get("hash").toString();

                final Map<String, Object> params = new HashMap<>();
                params.put("hash", hash);

                final int count = jdbcTemplate.queryForObject(
                    "SELECT COUNT(*) FROM vector_store WHERE metadata ->> 'hash' = :hash",
                    params,
                    Integer.class
                );

                if (count == 0) {
                    nonDuplicates.add(token);
                }
                else {
                    LOGGER.debug("** DUPLICATE DATA **");
                }
            }

            if(!nonDuplicates.isEmpty()) {
                vectorStore.add(nonDuplicates);
            }
            LOGGER.debug("** NON-DUPLICATE DATA COUNT: {} **", nonDuplicates.size());
        } catch (final IOException ioe) {
            throw new RuntimeException("Failed loading data from folder: " + ioe.getMessage());
        }
    }

    private void addHashToMetadata(final List<Document> tokens) {
        tokens.forEach(token -> {
            final String tokenContent = token.getContent();
            final String hashValue = computeHash(tokenContent);
            token.getMetadata().put("hash", hashValue);
        });
    }

    private String computeHash(final String content) {
        return Hashing
                .sha256()
                .hashString(content, StandardCharsets.UTF_8)
                .toString();
    }

}