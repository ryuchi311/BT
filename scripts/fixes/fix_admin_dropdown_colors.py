#!/usr/bin/env python3
"""
Script to fix dropdown text colors in admin_dashboard.html for better readability
"""

# Read the file
with open('d:/BTgame/templates/admin_dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix Platform dropdown
old_platform = '''                        <select name="platform" id="questPlatform" required
                            class="w-full bg-white/10 border border-white/20 rounded-lg px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-purple-500">
                            <option value="">Select...</option>
                            <option value="telegram">✈️ Telegram</option>
                            <option value="twitter">🐦 Twitter</option>
                            <option value="youtube">▶️ YouTube</option>
                            <option value="visit">🔗 Website</option>
                            <option value="daily_checkin">📅 Daily Check-In</option>
                        </select>'''

new_platform = '''                        <select name="platform" id="questPlatform" required
                            class="w-full bg-white/10 border border-white/20 rounded-lg px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
                            style="color: white;">
                            <option value="" style="background-color: #1f2937; color: #9ca3af;">Select...</option>
                            <option value="telegram" style="background-color: #1f2937; color: white;">✈️ Telegram</option>
                            <option value="twitter" style="background-color: #1f2937; color: white;">🐦 Twitter</option>
                            <option value="youtube" style="background-color: #1f2937; color: white;">▶️ YouTube</option>
                            <option value="visit" style="background-color: #1f2937; color: white;">🔗 Website</option>
                            <option value="daily_checkin" style="background-color: #1f2937; color: white;">📅 Daily Check-In</option>
                        </select>'''

content = content.replace(old_platform, new_platform)
print("✅ Fixed Platform dropdown")

# Fix Category dropdown
old_category = '''                        <select name="category" id="questCategory" required
                            class="w-full bg-white/10 border border-white/20 rounded-lg px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-purple-500">
                            <option value="">Select...</option>
                            <option value="Social">📱 Social</option>
                            <option value="Engagement">💬 Engagement</option>
                            <option value="Educational">📚 Educational</option>
                            <option value="Reward">🎁 Reward</option>
                        </select>'''

new_category = '''                        <select name="category" id="questCategory" required
                            class="w-full bg-white/10 border border-white/20 rounded-lg px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-purple-500"
                            style="color: white;">
                            <option value="" style="background-color: #1f2937; color: #9ca3af;">Select...</option>
                            <option value="Social" style="background-color: #1f2937; color: white;">📱 Social</option>
                            <option value="Engagement" style="background-color: #1f2937; color: white;">💬 Engagement</option>
                            <option value="Educational" style="background-color: #1f2937; color: white;">📚 Educational</option>
                            <option value="Reward" style="background-color: #1f2937; color: white;">🎁 Reward</option>
                        </select>'''

content = content.replace(old_category, new_category)
print("✅ Fixed Category dropdown")

# Write back
with open('d:/BTgame/templates/admin_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n✅ Dropdown colors fixed for better readability!")
