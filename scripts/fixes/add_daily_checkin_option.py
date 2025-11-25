#!/usr/bin/env python3
"""
Script to add daily_checkin option to admin dashboard platform dropdown
"""

# Read the file
with open('d:/BTgame/templates/admin_dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add daily_checkin option to platform dropdown
old_options = '''                            <option value="">Select...</option>
                            <option value="telegram">✈️ Telegram</option>
                            <option value="twitter">🐦 Twitter</option>
                            <option value="youtube">▶️ YouTube</option>
                            <option value="visit">🔗 Website</option>'''

new_options = '''                            <option value="">Select...</option>
                            <option value="telegram">✈️ Telegram</option>
                            <option value="twitter">🐦 Twitter</option>
                            <option value="youtube">▶️ YouTube</option>
                            <option value="visit">🔗 Website</option>
                            <option value="daily_checkin">📅 Daily Check-In</option>'''

content = content.replace(old_options, new_options)

# Write back
with open('d:/BTgame/templates/admin_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Daily Check-In option added to admin dashboard!")
