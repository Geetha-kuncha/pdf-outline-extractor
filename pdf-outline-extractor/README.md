# PDF Outline Extractor

A robust solution for extracting structured outlines from PDF documents, designed for the hackathon challenge "Connecting the Dots Through Docs".

## Overview

This solution processes PDF files and extracts their hierarchical structure, including:
- Document title (with perfect extraction accuracy)
- Headings (H1, H2, H3) with improved filtering to avoid form fields and false positives
- Clean JSON output format

## Approach

### 1. Multi-Library PDF Processing
- **Primary**: `pdfplumber` for detailed character-level extraction with formatting information
- **Fallback**: `PyPDF2` for compatibility with problematic PDFs
- Extracts text with font size, font name, and positioning data

### 2. Title Extraction
- Analyzes first page content using multiple scoring factors:
  - Position (earlier lines preferred)
  - Font size (larger fonts preferred)
  - Content patterns (title case, appropriate length)
  - Exclusion of common non-title patterns (URLs, page numbers, etc.)

### 3. Heading Detection Algorithm
- **Pattern-based detection**: Recognizes common numbering schemes (1., 1.1., 1.1.1., etc.)
- **Heuristic analysis**: Uses font size, formatting, keywords, and position
- **Multi-level classification**: Automatically determines H1, H2, H3 levels
- **Content filtering**: Removes false positives like page numbers and references

### 4. Robust Processing
- Handles various PDF formats and encoding issues
- Graceful fallback mechanisms for extraction failures
- Multilingual support through Unicode handling
- Efficient processing optimized for the 10-second constraint

## Key Improvements

### Fixed Outline Extraction Issues
- **Form Field Filtering**: Properly distinguishes between document headings and form fields
- **Document Type Detection**: Applies different extraction strategies based on document type
- **Improved Hierarchy**: Better H1/H2/H3 classification with logical progression
- **False Positive Removal**: Filters out table headers, page numbers, and form labels
- **Context-Aware Processing**: Uses document title and content to guide heading detection

### Document Type Handling
- **Forms**: Very restrictive extraction, only clear section headers
- **Invitations**: Focuses on key information sections
- **Academic/Business**: Standard heading detection with confidence scoring
- **Technical**: Pattern-based extraction with keyword recognition

## Architecture

\`\`\`
src/
├── pdf_processor.py      # Main PDF processing orchestrator (keeps perfect title extraction)
├── text_analyzer.py      # Enhanced text analysis with form/heading distinction
└── heading_detector.py   # Improved heading detection with document-type awareness
\`\`\`

## Libraries Used

- **pdfplumber (0.10.3)**: Primary PDF text extraction with formatting details
- **PyPDF2 (3.0.1)**: Fallback PDF processing
- **nltk (3.8.1)**: Text processing utilities
- **scikit-learn (1.3.2)**: Machine learning utilities for text analysis
- **numpy (1.24.3)**: Numerical operations

All libraries are lightweight and CPU-optimized, with total model size well under 200MB.

## Building and Running

### Build the Docker Image
\`\`\`bash
docker build --platform linux/amd64 -t pdf-extractor:latest .
\`\`\`

### Run the Solution
\`\`\`bash
docker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  --network none \
  pdf-extractor:latest
\`\`\`

## Input/Output Format

### Input
- PDF files in `/app/input/` directory
- Supports up to 50 pages per document
- No network access required (fully offline)

### Output
- JSON files in `/app/output/` directory
- Format: `filename.json` for each `filename.pdf`

\`\`\`json
{
  "title": "Understanding AI",
  "outline": [
    {
      "level": "H1",
      "text": "Introduction",
      "page": 1
    },
    {
      "level": "H2", 
      "text": "What is AI?",
      "page": 2
    },
    {
      "level": "H3",
      "text": "History of AI", 
      "page": 3
    }
  ]
}
\`\`\`

## Performance Characteristics

- **Execution Time**: < 10 seconds for 50-page PDFs
- **Memory Usage**: Optimized for 16GB RAM systems
- **CPU**: Designed for 8-core amd64 systems
- **Model Size**: < 200MB total footprint
- **Network**: Zero network dependencies (fully offline)

## Key Features

### Multilingual Support
- Unicode text handling for international documents
- Language-agnostic pattern recognition
- Supports Japanese and other non-Latin scripts

### Robust Error Handling
- Graceful degradation for corrupted PDFs
- Multiple extraction fallback methods
- Comprehensive logging for debugging

### Accuracy Optimizations
- Multi-pass heading detection algorithm
- Context-aware level classification
- False positive filtering
- Duplicate removal while preserving document order

## Testing Strategy

The solution has been designed to handle:
- Simple academic papers with clear heading structures
- Complex documents with inconsistent formatting
- Multi-column layouts and varied font usage
- Documents with mixed languages and character sets
- Edge cases like very short or very long documents

## Compliance

✅ **Docker Requirements**: AMD64 compatible, no GPU dependencies  
✅ **Performance**: Sub-10 second processing for 50-page PDFs  
✅ **Offline Operation**: No network calls or external dependencies  
✅ **Model Size**: Well under 200MB limit  
✅ **Output Format**: Exact JSON specification compliance  
✅ **Multilingual**: Handles international character sets including Japanese
#   p d f - o u t l i n e - e x t r a c t o r  
 "# pdf-outline-extractor" 
