package com.petrov.ragproject.utility;

import java.util.List;

import java.io.IOException;

import org.springframework.ai.document.Document;

public interface IDocumentReader {
    List<Document> extractFilesData() throws IOException;
}
