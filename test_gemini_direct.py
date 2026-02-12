"""
Direct test of Gemini API with handwriting extraction
"""

import os
import sys
from utils.gemini_processor import GeminiTextExtractor

def test_all_images():
    """Test handwriting extraction on all images"""
    
    # Get all images in attached_assets
    assets_dir = r"d:\Final_MP\AIEXAM (2)\AIEXAM\AIExamEvaluator\attached_assets"
    
    if not os.path.exists(assets_dir):
        print(f"ERROR: Directory not found: {assets_dir}")
        return
    
    # Get all PNG files
    images = [f for f in os.listdir(assets_dir) if f.endswith('.png')]
    
    if not images:
        print(f"No PNG images found in {assets_dir}")
        return
    
    print(f"Found {len(images)} images to test:")
    for i, img in enumerate(images, 1):
        print(f"{i}. {img}")
    
    print('\n' + '='*70)
    
    # Initialize extractor
    extractor = GeminiTextExtractor()
    
    if extractor.model is None:
        print("ERROR: Gemini model not available!")
        return
    
    # Test each image
    for img in images:
        img_path = os.path.join(assets_dir, img)
        print(f"\n\nTesting: {img}")
        print('='*70)
        
        # Extract text
        text = extractor.extract_text_from_image(img_path)
        
        if text:
            print("\n--- EXTRACTED TEXT ---")
            print(text)
            print(f"\n{'='*70}")
            print(f"Total characters: {len(text)}")
        else:
            print("\nERROR: No text extracted!")
        
        print('='*70)
        
        # Ask if user wants to continue
        if img != images[-1]:
            response = input("\nPress Enter to test next image, or 'q' to quit: ")
            if response.lower() == 'q':
                break

if __name__ == "__main__":
    test_all_images()
