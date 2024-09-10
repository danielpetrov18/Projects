package com.petrov.rag.readers;

import java.util.List;
import java.util.ArrayList;

import java.io.File;
import java.io.IOException;

import org.apache.logging.log4j.Logger;
import org.apache.logging.log4j.LogManager;

import org.springframework.ai.document.Document;

import org.springframework.stereotype.Component;

import org.springframework.core.io.FileSystemResource;

import org.springframework.beans.factory.annotation.Value;

import org.springframework.ai.reader.tika.TikaDocumentReader;

@Component
public class MyTikaDocumentReader implements IDocumentReader {
    
    @Value("${spring.data-folder}")
    private String filesPath;

    private final Logger LOGGER = LogManager.getLogger(this.getClass());

    private final static List<String> SUPPORTED_FILE_TYPES = List.of("pdf",".docx", ".pptx", ".html", ".txt");

    @Override
    public List<Document> extractFilesData() throws IOException {
        final File filesFolder = new File(filesPath);
        if (!filesFolder.exists() || !filesFolder.isDirectory()) {
            throw new IOException(String.format("Folder %s does not exist or is not a directory!", filesFolder.getAbsolutePath()));
        }

        final List<Document> filesData = new ArrayList<>();
        for(final String fileType : SUPPORTED_FILE_TYPES) {
            final File[] files = filesFolder.listFiles((dir, name) -> name.toLowerCase().endsWith(fileType));
            
            for(final File file : files) {
                filesData.addAll(processFile(file));
                LOGGER.debug("** Extracted data from: {} **", file.getName());
            }
        }
        return filesData;
    }

    private List<Document> processFile(final File file) throws IOException {
        final TikaDocumentReader reader = new TikaDocumentReader(new FileSystemResource(file));
        return reader.read();
    }

}