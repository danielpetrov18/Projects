package com.petrov.rag.readers;

import java.util.List;
import java.util.ArrayList;

import java.io.File;
import java.io.IOException;

import org.apache.logging.log4j.Logger;
import org.apache.logging.log4j.LogManager;

import org.springframework.core.io.FileSystemResource;

import org.springframework.stereotype.Component;

import org.springframework.beans.factory.annotation.Value;

import org.springframework.ai.document.Document;
import org.springframework.ai.reader.ExtractedTextFormatter;
import org.springframework.ai.reader.pdf.PagePdfDocumentReader;
import org.springframework.ai.reader.pdf.config.PdfDocumentReaderConfig;

@Component
public class PdfDocumentReader implements IDocumentReader {

   @Value("${spring.data-folder}")
   private String pdfFilesFilepath;

   private final Logger LOGGER = LogManager.getLogger(this.getClass());

   @Override
   public List<Document> extractFilesData() throws IOException {
      final File pdfFolder = new File(pdfFilesFilepath);
      if (!pdfFolder.exists() || !pdfFolder.isDirectory()) {
         throw new IOException(String.format("Folder %s does not exist or is not a directory!", pdfFolder.getAbsolutePath()));
      }

      // Passing a filter to make sure that we only target PDF files
      final File[] files = pdfFolder.listFiles((dir, name) -> name.toLowerCase().endsWith(".pdf"));
      
      List<Document> filesData = new ArrayList<>();
      for(final File file : files) {
         filesData.addAll(processPdfFile(file));
         LOGGER.debug("** Extracted data from: {} **", file.getName());
      }
      return filesData;
  }

   private List<Document> processPdfFile(final File file) throws IOException {
      final PagePdfDocumentReader pdfReader = new PagePdfDocumentReader(new FileSystemResource(file),
              PdfDocumentReaderConfig.builder()
                  .withPageTopMargin(0)
                  .withPagesPerDocument(1)
                  .withPageExtractedTextFormatter(ExtractedTextFormatter.builder()
                      .withNumberOfTopTextLinesToDelete(0)
                      .build())
                  .build());     
                  
      return pdfReader.read();
   }

}