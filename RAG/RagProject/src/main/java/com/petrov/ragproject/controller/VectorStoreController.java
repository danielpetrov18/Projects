package com.petrov.ragproject.controller;

import com.petrov.ragproject.service.VectorStoreService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping(path = "/api/v1")
public class VectorStoreController {

    private final VectorStoreService service;

    @Autowired
    public VectorStoreController(VectorStoreService service) {
        this.service = service;
    }

}
