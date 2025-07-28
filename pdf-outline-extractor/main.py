#!/usr/bin/env python3
"""
PDF Outline Extractor - Main Entry Point
Processes all PDFs in input and generates JSON outlines in output
"""

import os
import sys
import json
import logging
from pathlib import Path
from src.pdf_processor import PDFProcessor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main function to process all PDFs in input directory"""
    input_dir = Path("input")
    output_dir = Path("output")
    
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Initialize PDF processor
    processor = PDFProcessor()
    
    # Find all PDF files in input directory
    pdf_files = list(input_dir.glob("*.pdf"))
    
    if not pdf_files:
        logger.warning("No PDF files found in input directory")
        return
    
    logger.info(f"Found {len(pdf_files)} PDF files to process")
    
    # Process each PDF file
    for pdf_path in pdf_files:
        try:
            logger.info(f"Processing: {pdf_path.name}")
            
            # Extract outline
            outline_data = processor.extract_outline(pdf_path)
            
            # Generate output filename
            output_filename = pdf_path.stem + ".json"
            output_path = output_dir / output_filename
            
            # Save JSON output
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(outline_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Successfully processed {pdf_path.name} -> {output_filename}")
            logger.info(f"Title: {outline_data['title']}")
            logger.info(f"Headings found: {len(outline_data['outline'])}")
            
            # Log outline for debugging
            for heading in outline_data['outline']:
                logger.info(f"  {heading['level']}: {heading['text']} (page {heading['page']})")
            
        except Exception as e:
            logger.error(f"Error processing {pdf_path.name}: {str(e)}")
            # Create empty output to avoid breaking the pipeline
            error_output = {
                "title": "Error: Could not process document",
                "outline": []
            }
            output_filename = pdf_path.stem + ".json"
            output_path = output_dir / output_filename
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(error_output, f, indent=2)

if __name__ == "__main__":
    main()