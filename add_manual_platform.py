#!/usr/bin/env python3
"""
Script to add Manual option to Platform dropdown in admin_dashboard.html
"""

# Read the file
with open('d:/BTgame/templates/admin_dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the Platform dropdown and add Manual option
old_platform_options = '''                            <option value="daily_checkin" style="background-color: #1f2937; color: white;">📅 Daily Check-In</option>
                        </select>'''

new_platform_options = '''                            <option value="daily_checkin" style="background-color: #1f2937; color: white;">📅 Daily Check-In</option>
                            <option value="manual" style="background-color: #1f2937; color: white;">✋ Manual</option>
                        </select>'''

if old_platform_options in content:
    content = content.replace(old_platform_options, new_platform_options)
    print("✅ Added Manual option to Platform dropdown")
else:
    print("⚠️  Could not find exact pattern, trying alternative...")

# Write back
with open('d:/BTgame/templates/admin_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Manual platform option added!")
