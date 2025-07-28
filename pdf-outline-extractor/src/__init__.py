"""
PDF Outline Extractor Package
"""

__version__ = "1.0.0"
__author__ = "PDF Outline Extractor"
__description__ = "Extract structured outlines from PDF documents"

# Make sure all modules can be imported
from .text_analyzer import TextAnalyzer
from .heading_detector import HeadingDetector
from .pdf_processor import PDFProcessor

__all__ = ['TextAnalyzer', 'HeadingDetector', 'PDFProcessor']
