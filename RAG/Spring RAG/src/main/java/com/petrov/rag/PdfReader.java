package com.petrov.rag;

import java.io.File;

import org.apache.pdfbox.pdmodel.PDDocument;
import org.apache.pdfbox.text.PDFTextStripper;

import org.springframework.stereotype.Component;

@Component
public class PdfReader {

    private final PDDocument pdfDocument;


    File file = new File("sample.pdf");
    PDDocument document = PDDocument.load(file);
    PDFTextStripper stripper = new PDFTextStripper();
    String text = stripper.getText(document);
    document.close();

}
