"""
Test Gemini handwriting extraction with the uploaded image
"""

import os
import sys
from utils.gemini_processor import GeminiTextExtractor

def test_extraction():
    """Test handwriting extraction"""
    
    # Test with handwritten answer image
    test_image = r"d:\Final_MP\AIEXAM (2)\AIEXAM\AIExamEvaluator\attached_assets\image_1747628188981.png"
    
    if not os.path.exists(test_image):
        print(f"ERROR: Image not found: {test_image}")
        return
    
    print(f"Testing with: {os.path.basename(test_image)}")
    print('='*70)
    
    # Initialize extractor
    extractor = GeminiTextExtractor()
    
    if extractor.model is None:
        print("ERROR: Gemini model not available!")
        return
    
    print("Extracting text with Gemini...")
    
    # Extract text
    text = extractor.extract_text_from_image(test_image)
    
    if text:
        print("\n--- EXTRACTED TEXT ---")
        print(text)
        print(f"\n{'='*70}")
        print(f"Total characters: {len(text)}")
    else:
        print("\nERROR: No text extracted!")
    
    print('='*70)

if __name__ == "__main__":
    test_extraction()
