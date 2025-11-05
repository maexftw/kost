#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extract logo images from .eml email files
"""
import os
import email
import base64
import sys
from pathlib import Path

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Paths - using absolute path
base_dir = Path(__file__).parent.parent.parent.parent
email_dir = base_dir / "Kostmails"
logos_dir = Path("images/logos")
logos_dir.mkdir(parents=True, exist_ok=True)

print(f"Looking for emails in: {email_dir}")
print(f"Email dir exists: {email_dir.exists()}")
if email_dir.exists():
    eml_files = list(email_dir.glob("*.eml"))
    print(f"Found {len(eml_files)} .eml files")

# Mapping of email attachments to logo filenames
logo_mapping = {
    "Logo_Boss-Steinlen-1400x142.png": "boss-steinlen.png",
    "Logo_paratos_protection_weiß.png": "paratos.png",
    "logo.png": "paratos.png",  # Fallback
}

print("\nExtracting logos from email attachments...")

for eml_file in email_dir.glob("*.eml"):
    print(f"\nProcessing: {eml_file.name}")
    
    try:
        with open(eml_file, 'rb') as f:
            msg = email.message_from_bytes(f.read())
        
        # Check all parts
        for part in msg.walk():
            if part.get_content_disposition() == 'attachment':
                filename = part.get_filename()
                if filename:
                    print(f"  Found attachment: {filename}")
                    
                    # Decode filename if needed
                    if filename.startswith('=?'):
                        import email.header
                        try:
                            decoded_header = email.header.decode_header(filename)
                            if decoded_header and decoded_header[0][0]:
                                filename = decoded_header[0][0]
                                if isinstance(filename, bytes):
                                    filename = filename.decode('utf-8', errors='ignore')
                        except:
                            pass
                    
                    # Check if this is a logo we need
                    target_name = None
                    for key, value in logo_mapping.items():
                        if key.lower() in filename.lower():
                            target_name = value
                            break
                    
                    # Also check for paratos logos
                    if 'paratos' in filename.lower() or 'logo.png' == filename.lower():
                        if not target_name:  # Only if not already matched
                            target_name = "paratos.png"
                    
                    if target_name:
                        # Extract the image
                        if part.get_content_type().startswith('image/'):
                            image_data = part.get_payload(decode=True)
                            if image_data:
                                target_path = logos_dir / target_name
                                with open(target_path, 'wb') as img_file:
                                    img_file.write(image_data)
                                print(f"  [OK] Saved as: {target_path}")
                            else:
                                print(f"  [ERROR] No image data found")
                    else:
                        print(f"  [SKIP] Skipping (not a logo)")
                        
    except Exception as e:
        print(f"  [ERROR] Error processing {eml_file.name}: {e}")

print("\n[OK] Logo extraction complete!")
print(f"Check {logos_dir} for extracted logos.")

