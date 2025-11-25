#!/usr/bin/env python3
"""
Script to add Rewards link to the main navigation in base.html
"""

# Read the file
with open('d:/BTgame/templates/base.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the navigation section and add Rewards link
# Looking for the Quests link to add Rewards after it
old_nav = '''                <a href="/quests"
                    class="text-gray-300 hover:text-white transition-colors duration-200 font-semibold">Quests</a>'''

new_nav = '''                <a href="/quests"
                    class="text-gray-300 hover:text-white transition-colors duration-200 font-semibold">Quests</a>
                <a href="/rewards"
                    class="text-gray-300 hover:text-white transition-colors duration-200 font-semibold">🎁 Rewards</a>'''

if old_nav in content:
    content = content.replace(old_nav, new_nav)
    print("✅ Rewards link added to navigation!")
else:
    print("⚠️  Could not find navigation section, trying alternative...")
    # Alternative: look for the nav container
    if '<nav class="flex space-x-8">' in content or 'class="flex space-x-' in content:
        print("Found nav container, please check manually")
    else:
        print("Navigation structure may be different")

# Write back
with open('d:/BTgame/templates/base.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Navigation updated!")
