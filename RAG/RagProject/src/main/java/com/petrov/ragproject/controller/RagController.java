package com.petrov.ragproject.controller;

import com.petrov.ragproject.utility.Loader;

import org.springframework.http.MediaType;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;

import com.petrov.ragproject.service.RagService;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import org.springframework.beans.factory.annotation.Autowired;

@RestController
@RequestMapping(path = "/api/v1")
public class RagController {

    private final Loader dataLoader;
    private final RagService service;

    @Autowired
    public RagController(final Loader dataLoader, final RagService service) {
        this.dataLoader = dataLoader;
        this.service = service;
    }

    @GetMapping(path = "/prompt", produces = MediaType.APPLICATION_JSON_VALUE)
    public ResponseEntity<String> promptChatClient(@RequestParam(required = true, name = "query") final String query) {
        try {
            final String chatClientResponse = service.promptChatClient(query);
            return new ResponseEntity<>(chatClientResponse, HttpStatus.OK);
        } catch(final Exception e) {
            return new ResponseEntity<>("Something went wrong in the chat client: " + e.getMessage(), HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

}