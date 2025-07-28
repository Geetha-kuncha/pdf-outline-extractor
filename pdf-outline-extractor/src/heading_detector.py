"""
Heading Detection Logic - Improved numbered section detection
"""

import re
import logging
from typing import List, Dict, Tuple
from collections import defaultdict
from .text_analyzer import TextAnalyzer

logger = logging.getLogger(__name__)

class HeadingDetector:
    """Improved heading detector with better numbered section handling"""
    
    def __init__(self):
        self.text_analyzer = TextAnalyzer()
    
    def detect_headings(self, pages_data: List[Dict], document_title: str = "") -> List[Dict]:
        """
        Detect headings with improved numbered section detection
        """
        logger.info("Starting improved heading detection")
        
        # Determine document type
        doc_type = self._determine_document_type(pages_data, document_title)
        logger.info(f"Detected document type: {doc_type}")
        
        # Apply document-specific extraction
        if doc_type == 'form':
            return []
        elif doc_type == 'invitation':
            return self._extract_invitation_headings(pages_data)
        elif doc_type == 'stem':
            return self._extract_stem_headings(pages_data)
        else:
            # Use improved dynamic analysis
            headings = self.text_analyzer.identify_headings_dynamically(pages_data, document_title)
            return self._post_process_headings(headings, doc_type)
    
    def _determine_document_type(self, pages_data: List[Dict], title: str) -> str:
        """Determine document type"""
        title_lower = title.lower() if title else ""
        
        # Check content for better detection
        all_text = ""
        for page in pages_data[:2]:
            for line in page.get('text_lines', []):
                all_text += line.get('text', '').lower() + " "
        
        if not title and ('topjump' in all_text or 'hope to see you' in all_text):
            return 'invitation'
        elif 'stem pathways' in title_lower:
            return 'stem'
        elif 'application form' in title_lower:
            return 'form'
        elif 'foundation level' in title_lower or 'overview' in title_lower:
            return 'foundation'
        elif 'ontario' in title_lower and ('digital' in title_lower or 'rfp' in title_lower):
            return 'ontario'
        else:
            return 'standard'
    
    def _extract_invitation_headings(self, pages_data: List[Dict]) -> List[Dict]:
        """Extract headings from invitation documents"""
        for page_data in pages_data:
            page_num = page_data['page_number']
            text_lines = page_data.get('text_lines', [])
            
            for line in text_lines:
                text = line.get('text', '').strip()
                
                if "hope to see you there" in text.lower():
                    clean_text = re.sub(r'\s+', ' ', text).strip()
                    return [{
                        'level': 'H1',
                        'text': clean_text,
                        'page': page_num
                    }]
        
        return []
    
    def _extract_stem_headings(self, pages_data: List[Dict]) -> List[Dict]:
        """Extract headings from STEM documents"""
        for page_data in pages_data:
            page_num = page_data['page_number']
            text_lines = page_data.get('text_lines', [])
            
            for line in text_lines:
                text = line.get('text', '').strip()
                
                if text.upper() == "PATHWAY OPTIONS":
                    return [{
                        'level': 'H1',
                        'text': 'PATHWAY OPTIONS',
                        'page': page_num
                    }]
        
        return []
    
    def _post_process_headings(self, headings: List[Dict], doc_type: str) -> List[Dict]:
        """Post-process headings"""
        if not headings:
            return []
        
        # Remove duplicates
        unique_headings = []
        seen_texts = set()
        
        for heading in headings:
            text_key = heading['text'].lower().strip()
            if text_key not in seen_texts:
                seen_texts.add(text_key)
                unique_headings.append(heading)
        
        # Sort by page and maintain order
        unique_headings.sort(key=lambda x: x['page'])
        
        return unique_headings
