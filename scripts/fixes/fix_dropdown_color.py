#!/usr/bin/env python3
"""
Script to fix dropdown text color for better readability
"""

# Read the file
with open('d:/BTgame/templates/admin_rewards.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the category dropdown to add better text styling
old_select = '''                <select name="category"
                    class="w-full bg-white/10 border border-white/20 rounded-lg px-4 py-3 text-white">
                    <option value="">Select category...</option>
                    <option value="Physical">📦 Physical Item</option>
                    <option value="Digital">💻 Digital Good</option>
                    <option value="Voucher">🎟️ Voucher/Coupon</option>
                    <option value="Premium">⭐ Premium Access</option>
                    <option value="Merchandise">👕 Merchandise</option>
                    <option value="Other">🎁 Other</option>
                </select>'''

new_select = '''                <select name="category"
                    class="w-full bg-white/10 border border-white/20 rounded-lg px-4 py-3 text-white"
                    style="color: white;">
                    <option value="" style="background-color: #1f2937; color: #9ca3af;">Select category...</option>
                    <option value="Physical" style="background-color: #1f2937; color: white;">📦 Physical Item</option>
                    <option value="Digital" style="background-color: #1f2937; color: white;">💻 Digital Good</option>
                    <option value="Voucher" style="background-color: #1f2937; color: white;">🎟️ Voucher/Coupon</option>
                    <option value="Premium" style="background-color: #1f2937; color: white;">⭐ Premium Access</option>
                    <option value="Merchandise" style="background-color: #1f2937; color: white;">👕 Merchandise</option>
                    <option value="Other" style="background-color: #1f2937; color: white;">🎁 Other</option>
                </select>'''

content = content.replace(old_select, new_select)

# Write back
with open('d:/BTgame/templates/admin_rewards.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Dropdown text color fixed for better readability!")
