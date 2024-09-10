package com.petrov.rag;

import org.springframework.http.MediaType;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

import java.io.IOException;

import org.springframework.beans.factory.annotation.Autowired;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping(path = "/api/v1")
public class RAGController {

    private final RAGService ragService;

    @Autowired
    public RAGController(RAGService chatClient) {
        this.ragService = chatClient;
    }

    @GetMapping(path = "/data", produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<?> getData() {
        try {
            return new ResponseEntity<>(ragService.getData(), HttpStatus.OK);
        } catch(final IOException ioe) {
            return new ResponseEntity<>(ioe.getMessage(), HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

}