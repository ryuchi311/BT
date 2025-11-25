#!/usr/bin/env python3
"""
Script to add Font Awesome to base.html so icons work on all pages
"""

# Read the file
with open('d:/BTgame/templates/base.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add Font Awesome CSS link if not already there
if 'font-awesome' not in content.lower() and 'fontawesome' not in content.lower():
    # Add after Tailwind CSS
    fa_link = '    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">\n'
    
    if '<script src="https://cdn.tailwindcss.com"></script>' in content:
        content = content.replace(
            '<script src="https://cdn.tailwindcss.com"></script>',
            fa_link + '    <script src="https://cdn.tailwindcss.com"></script>'
        )
        print("✅ Added Font Awesome to base.html")
    else:
        print("⚠️  Could not find Tailwind script tag")

# Write back
with open('d:/BTgame/templates/base.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Font Awesome library added to base template!")
