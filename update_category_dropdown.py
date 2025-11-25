#!/usr/bin/env python3
"""
Script to change Category field from text input to dropdown in admin_rewards.html
"""

# Read the file
with open('d:/BTgame/templates/admin_rewards.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the category input with a dropdown
old_category = '''            <div>
                <label class="block text-sm font-semibold text-gray-300 mb-2">Category</label>
                <input type="text" name="category"
                    class="w-full bg-white/10 border border-white/20 rounded-lg px-4 py-3 text-white"
                    placeholder="e.g., Physical, Digital, Voucher">
            </div>'''

new_category = '''            <div>
                <label class="block text-sm font-semibold text-gray-300 mb-2">Category</label>
                <select name="category"
                    class="w-full bg-white/10 border border-white/20 rounded-lg px-4 py-3 text-white">
                    <option value="">Select category...</option>
                    <option value="Physical">📦 Physical Item</option>
                    <option value="Digital">💻 Digital Good</option>
                    <option value="Voucher">🎟️ Voucher/Coupon</option>
                    <option value="Premium">⭐ Premium Access</option>
                    <option value="Merchandise">👕 Merchandise</option>
                    <option value="Other">🎁 Other</option>
                </select>
            </div>'''

content = content.replace(old_category, new_category)

# Write back
with open('d:/BTgame/templates/admin_rewards.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Category field changed to dropdown in admin_rewards.html!")
