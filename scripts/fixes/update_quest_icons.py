#!/usr/bin/env python3
"""
Script to replace emoji icons with Flaticon SVG icons in admin_dashboard.html
"""

# Read the file
with open('d:/BTgame/templates/admin_dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add Flaticon CSS link in the head section (if not already there)
if 'flaticon' not in content.lower():
    # Add link-stylesheet for Flaticon (using Font Awesome as alternative since Flaticon requires download)
    # We'll use Font Awesome icons which are free and similar
    fa_link = '''    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
'''
    if '<script src="https://cdn.tailwindcss.com"></script>' in content:
        content = content.replace(
            '<script src="https://cdn.tailwindcss.com"></script>',
            fa_link + '    <script src="https://cdn.tailwindcss.com"></script>'
        )
        print("✅ Added Font Awesome icons library")

# Replace emoji icons with Font Awesome icons in quest cards
icon_replacements = [
    # Telegram icon
    (
        '''                        <span class="text-3xl">
                            {% if quest.quest_type == 'telegram' %}✈️
                            {% elif quest.quest_type == 'twitter' %}🐦
                            {% elif quest.quest_type == 'youtube' %}▶️
                            {% else %}🔗{% endif %}
                        </span>''',
        '''                        <span class="text-3xl">
                            {% if quest.quest_type == 'telegram' %}
                                <i class="fab fa-telegram text-blue-400"></i>
                            {% elif quest.quest_type == 'twitter' %}
                                <i class="fab fa-twitter text-sky-400"></i>
                            {% elif quest.quest_type == 'youtube' %}
                                <i class="fab fa-youtube text-red-500"></i>
                            {% elif quest.quest_type == 'daily_checkin' %}
                                <i class="fas fa-calendar-check text-orange-400"></i>
                            {% elif quest.quest_type == 'manual' %}
                                <i class="fas fa-hand-paper text-purple-400"></i>
                            {% else %}
                                <i class="fas fa-link text-green-400"></i>
                            {% endif %}
                        </span>'''
    ),
]

for old, new in icon_replacements:
    if old in content:
        content = content.replace(old, new)
        print("✅ Replaced quest type icons with Font Awesome icons")

# Write back
with open('d:/BTgame/templates/admin_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n✅ Icons updated to use Font Awesome (Flaticon-style)!")
print("Icons now include:")
print("  - Telegram: fab fa-telegram")
print("  - Twitter: fab fa-twitter")
print("  - YouTube: fab fa-youtube")
print("  - Daily Check-in: fas fa-calendar-check")
print("  - Manual: fas fa-hand-paper")
print("  - Website: fas fa-link")
