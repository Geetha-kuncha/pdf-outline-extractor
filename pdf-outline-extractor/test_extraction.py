#!/usr/bin/env python3
"""
Simple test script to verify PDF extraction works correctly
"""

import sys
import json
from pathlib import Path
from src.pdf_processor import PDFProcessor

def test_extraction():
    """Test the PDF extraction on sample files"""
    processor = PDFProcessor()
    
    # Test files (you would need to have these in an input directory)
    test_files = [
        "file01.pdf",  # LTC application form
        "file02.pdf",  # Foundation Level Extensions
        "file03.pdf",  # Ontario Digital Library RFP
        "file04.pdf",  # STEM Pathways
        "file05.pdf",  # TopJump invitation
    ]
    
    input_dir = Path("input")
    
    for filename in test_files:
        pdf_path = input_dir / filename
        if pdf_path.exists():
            print(f"\nTesting {filename}...")
            try:
                result = processor.extract_outline(pdf_path)
                print(f"Title: '{result['title']}'")
                print(f"Headings found: {len(result['outline'])}")
                
                # Print first few headings
                for i, heading in enumerate(result['outline'][:5]):
                    print(f"  {heading['level']}: {heading['text']} (page {heading['page']})")
                
                if len(result['outline']) > 5:
                    print(f"  ... and {len(result['outline']) - 5} more headings")
                    
            except Exception as e:
                print(f"Error processing {filename}: {e}")
        else:
            print(f"File not found: {pdf_path}")

if __name__ == "__main__":
    test_extraction()
