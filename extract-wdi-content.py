#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extract WDI logo and testimonial from email
"""
import email
from pathlib import Path
import sys
import re

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

email_dir = Path("Kostmails")
logos_dir = Path("images/logos")
logos_dir.mkdir(parents=True, exist_ok=True)

# Find WDI email
wdi_email = None
for eml_file in email_dir.glob("*.eml"):
    try:
        with open(eml_file, 'rb') as f:
            msg = email.message_from_bytes(f.read())
        
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type == "text/html":
                    try:
                        body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                    except:
                        pass
        
        if 'wdi.de' in body.lower() or 'ralf.rauch' in body.lower():
            wdi_email = eml_file
            print(f"WDI E-Mail gefunden: {eml_file.name}\n")
            
            # Extract logo
            for part in msg.walk():
                if part.get_content_disposition() == 'attachment':
                    filename = part.get_filename()
                    if filename:
                        # Decode filename
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
                        
                        print(f"Anhang: {filename}")
                        
                        # Check if it's an image
                        if part.get_content_type().startswith('image/'):
                            image_data = part.get_payload(decode=True)
                            if image_data:
                                # Save as WDI logo
                                logo_path = logos_dir / "wdi-schwerte.png"
                                with open(logo_path, 'wb') as img_file:
                                    img_file.write(image_data)
                                print(f"✓ Logo gespeichert: {logo_path} ({len(image_data)} bytes)")
            
            # Extract testimonial text
            print("\n--- BEWERTUNGSTEXT ---")
            # Clean HTML and extract text
            body_clean = re.sub(r'<[^>]+>', ' ', body)
            body_clean = re.sub(r'\s+', ' ', body_clean)
            
            # Find testimonial section
            lines = body.split('\n')
            testimonial_started = False
            testimonial_lines = []
            
            for i, line in enumerate(lines):
                if 'zufrieden' in line.lower() or 'zusammenarbeit' in line.lower():
                    testimonial_started = True
                
                if testimonial_started:
                    # Remove HTML tags
                    line_clean = re.sub(r'<[^>]+>', '', line)
                    line_clean = re.sub(r'&nbsp;', ' ', line_clean)
                    line_clean = re.sub(r'&#8230;', '...', line_clean)
                    line_clean = line_clean.strip()
                    
                    if line_clean and len(line_clean) > 10:
                        testimonial_lines.append(line_clean)
                    
                    # Stop after a few lines
                    if len(testimonial_lines) > 10:
                        break
            
            # Also try to find in HTML content directly
            if 'Wir sind' in body or 'zufrieden' in body.lower():
                # Extract between certain markers
                match = re.search(r'Wir sind[^<]*zufrieden[^<]*Zusammenarbeit[^<]*', body_clean, re.IGNORECASE | re.DOTALL)
                if match:
                    testimonial_text = match.group(0)
                    testimonial_text = re.sub(r'\s+', ' ', testimonial_text)
                    testimonial_text = testimonial_text[:500]  # Limit length
                    print(f"\n{testimonial_text}\n")
            
            # Print full relevant section
            print("\n--- VOLLSTÄNDIGER RELEVANTER ABSCHNITT ---")
            for i, line in enumerate(lines):
                if 'ralf.rauch' in line.lower() or 'wdi.de' in line.lower():
                    # Print context
                    for j in range(max(0, i), min(len(lines), i+30)):
                        line_clean = re.sub(r'<[^>]+>', '', lines[j])
                        line_clean = re.sub(r'&nbsp;', ' ', line_clean)
                        line_clean = re.sub(r'&#8230;', '...', line_clean)
                        line_clean = line_clean.strip()
                        if line_clean:
                            print(line_clean)
                    break
            
            break
            
    except Exception as e:
        print(f"Fehler: {e}")

if not wdi_email:
    print("WDI E-Mail nicht gefunden!")

