#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Check Kostmails for WDI logo and testimonial
"""
import email
from pathlib import Path
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

email_dir = Path("Kostmails")

print("Durchsuche E-Mails nach WDI Logo und Bewertung...\n")

for eml_file in email_dir.glob("*.eml"):
    print(f"\n{'='*60}")
    print(f"Datei: {eml_file.name}")
    print('='*60)
    
    try:
        with open(eml_file, 'rb') as f:
            msg = email.message_from_bytes(f.read())
        
        # Check subject
        subject = msg.get('Subject', '')
        print(f"\nBetreff: {subject}")
        
        # Check sender
        sender = msg.get('From', '')
        print(f"Von: {sender}")
        
        # Check attachments
        attachments = []
        for part in msg.walk():
            if part.get_content_disposition() == 'attachment':
                filename = part.get_filename()
                if filename:
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
                    
                    attachments.append(filename)
                    print(f"\n  Anhang gefunden: {filename}")
                    
                    # Check if it's a WDI logo
                    if 'wdi' in filename.lower() or 'schwerte' in filename.lower():
                        print(f"  *** WDI LOGO GEFUNDEN: {filename} ***")
                        if part.get_content_type().startswith('image/'):
                            image_data = part.get_payload(decode=True)
                            if image_data:
                                logo_path = Path("images/logos/wdi-schwerte.png")
                                with open(logo_path, 'wb') as img_file:
                                    img_file.write(image_data)
                                print(f"  ✓ Logo gespeichert: {logo_path} ({len(image_data)} bytes)")
        
        # Check email body for WDI content
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type == "text/plain":
                    try:
                        body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                    except:
                        pass
                elif content_type == "text/html":
                    try:
                        body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                    except:
                        pass
        else:
            try:
                body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
            except:
                pass
        
        # Search for WDI mentions
        if 'wdi' in body.lower() or 'schwerte' in body.lower():
            print(f"\n  *** WDI INHALT GEFUNDEN ***")
            # Extract relevant part
            lines = body.split('\n')
            for i, line in enumerate(lines):
                if 'wdi' in line.lower() or 'schwerte' in line.lower():
                    print(f"\n  Zeile {i+1}: {line.strip()}")
                    # Show context
                    for j in range(max(0, i-2), min(len(lines), i+5)):
                        if j != i:
                            print(f"    {lines[j].strip()}")
                    break
        
        # Check for testimonials/reviews
        if 'bewertung' in body.lower() or 'referenz' in body.lower() or 'testimonial' in body.lower():
            print(f"\n  *** BEWERTUNG/TESTIMONIAL GEFUNDEN ***")
            # Extract relevant part
            lines = body.split('\n')
            for i, line in enumerate(lines):
                if any(word in line.lower() for word in ['bewertung', 'referenz', 'testimonial', 'zusammenarbeit']):
                    print(f"\n  Relevanter Abschnitt:")
                    for j in range(max(0, i-1), min(len(lines), i+10)):
                        print(f"    {lines[j].strip()}")
                    break
        
        if not attachments and 'wdi' not in body.lower():
            print("  Keine WDI-Inhalte gefunden")
            
    except Exception as e:
        print(f"  Fehler beim Verarbeiten: {e}")

print("\n" + "="*60)
print("Suche abgeschlossen!")
print("="*60)

