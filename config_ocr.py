"""
OCR Configuration Helper

This file is kept for backward compatibility but OCR.Space has been removed.
The project now uses:
1. Gemini API (primary text extraction)
2. TrOCR (deep learning for handwritten text)
3. PyTesseract (fallback OCR)

To use TrOCR, install dependencies:
    pip install torch transformers
"""

import logging

logger = logging.getLogger(__name__)

def get_ocr_setup_instructions():
    """Return setup instructions for OCR services"""
    return """
    The project uses the following OCR technologies:
    
    1. Gemini API (Primary - Always Active):
       - Configured with API key in gemini_processor.py
       - Used for both handwritten and typed text extraction
    
    2. TrOCR (Deep Learning - Optional):
       - Install dependencies: pip install torch transformers
       - Automatically used for handwritten text if available
    
    3. PyTesseract (Fallback - Always Available):
       - Requires Tesseract OCR to be installed on system
       - Used as fallback when other methods fail
    """
