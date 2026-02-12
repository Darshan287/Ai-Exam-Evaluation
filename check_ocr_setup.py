
#!/usr/bin/env python3
"""
OCR Setup Checker

Run this script to check which OCR services are properly configured.
"""

import os
import sys

def check_google_vision():
    """Check if Google Vision API is set up"""
    try:
        credentials_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        if credentials_path and os.path.exists(credentials_path):
            from google.cloud import vision
            client = vision.ImageAnnotatorClient()
            return True, "Google Vision API is properly configured"
        else:
            return False, "GOOGLE_APPLICATION_CREDENTIALS not set or file not found"
    except ImportError:
        return False, "Google Cloud Vision library not installed (pip install google-cloud-vision)"
    except Exception as e:
        return False, f"Google Vision API error: {str(e)}"

def check_azure_vision():
    """Check if Azure Computer Vision is set up"""
    endpoint = os.getenv('AZURE_VISION_ENDPOINT')
    key = os.getenv('AZURE_VISION_KEY')
    
    if endpoint and key:
        return True, "Azure Computer Vision API is configured"
    else:
        missing = []
        if not endpoint:
            missing.append('AZURE_VISION_ENDPOINT')
        if not key:
            missing.append('AZURE_VISION_KEY')
        return False, f"Missing environment variables: {', '.join(missing)}"

def check_trocr():
    """Check if TrOCR is available"""
    try:
        import torch
        import transformers
        return True, "TrOCR dependencies (torch, transformers) are installed"
    except ImportError as e:
        return False, f"TrOCR dependencies not installed: {str(e)}"

def main():
    print("=== OCR Services Setup Check ===\n")
    
    services = [
        ("Google Vision API", check_google_vision),
        ("Azure Computer Vision", check_azure_vision),
        ("TrOCR (Deep Learning)", check_trocr)
    ]
    
    configured_count = 0
    
    for service_name, check_func in services:
        is_configured, message = check_func()
        status = "✅ CONFIGURED" if is_configured else "❌ NOT CONFIGURED"
        print(f"{service_name}: {status}")
        print(f"   {message}\n")
        
        if is_configured:
            configured_count += 1
    
    print("\n📝 Note: The system uses multiple OCR methods:")
    print("   1. Gemini API (primary, always available)")
    print("   2. TrOCR (deep learning for handwritten text, if dependencies installed)")
    print("   3. PyTesseract (fallback, always available)")
    
    if configured_count == 0:
        print("\n⚠️  No cloud OCR services are configured.")
        print("   The system will use Gemini API and Tesseract OCR for text extraction.")

if __name__ == "__main__":
    main()
