#!/usr/bin/env python3
"""
Script to fix the rewards data in admin_rewards.html template
"""

# Read the file
with open('d:/BTgame/templates/admin_rewards.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the rewards | tojson with rewards_data | tojson
if 'const rewardsData = {{ rewards | tojson }};' in content:
    content = content.replace(
        'const rewardsData = {{ rewards | tojson }};',
        'const rewardsData = {{ rewards_data | tojson }};'
    )
    print("✅ Fixed rewards data serialization")
else:
    print("⚠️  Pattern not found, checking alternative...")

# Write back
with open('d:/BTgame/templates/admin_rewards.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Template fixed!")
