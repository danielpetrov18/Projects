package com.petrov.rag;

import org.springframework.http.MediaType;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

import org.springframework.beans.factory.annotation.Autowired;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
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

    @GetMapping(path = "/prompt", produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<String> prompt(@RequestParam(value="userPrompt") String userPrompt) {
        final String promptResponse = ragService.promptChatClient(userPrompt);
        System.out.println(String.format("** The user prompted: %s\nThe response was: %s**\n", userPrompt, promptResponse));
        return new ResponseEntity<>(promptResponse, HttpStatus.OK);
    }

}