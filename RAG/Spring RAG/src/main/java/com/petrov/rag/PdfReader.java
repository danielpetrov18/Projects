package com.petrov.rag;

import java.io.File;
import java.io.IOException;

import org.springframework.stereotype.Component;

import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.text.PDFTextStripper;
import org.apache.pdfbox.pdmodel.PDDocumentInformation;

import org.springframework.beans.factory.annotation.Value;

@Component
public class PdfReader {

   @Value("${spring.data.pdf-data}")
   private String pdfFilesFilepath;

   public String extractFilesData() throws IOException {
      final File pdfFolder = new File(pdfFilesFilepath);
      if (!pdfFolder.exists() || !pdfFolder.isDirectory()) {
         throw new IOException(String.format("Folder %s does not exist or is not a directory!", pdfFolder.getAbsolutePath()));
      }

      // Passing a filter to make sure that we only target PDF files
      final File[] files = pdfFolder.listFiles((dir, name) -> name.toLowerCase().endsWith(".pdf"));
      
      String filesData = "";
      for(final File file : files) {
          filesData += processPdfFile(file);
      }
      return filesData;
  }

   private String processPdfFile(final File file) {
      String fileContents = "";
      final StringBuilder strBuilder = new StringBuilder();

      try (PDDocument document = PDDocument.load(file)) {
          final PDFTextStripper pdfStripper = new PDFTextStripper();
          fileContents += pdfStripper.getText(document);

          final PDDocumentInformation docInfo = document.getDocumentInformation();
          strBuilder.append(String.format("Extracted text from PDF %s\n", file.getName()));
          strBuilder.append(String.format("Title: %s\n", docInfo.getTitle()));
          strBuilder.append(String.format("Page count: %d\n", document.getNumberOfPages()));
          strBuilder.append(String.format("Subject: %s\n", docInfo.getSubject()));
          strBuilder.append(String.format("Author: %s\n", docInfo.getAuthor()));

          System.out.println(strBuilder.toString());
      } catch (IOException e) {
          System.err.println("Error processing file: " + file.getName());
          e.printStackTrace();
      }

      return fileContents;
  }

}