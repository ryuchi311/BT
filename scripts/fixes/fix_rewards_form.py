#!/usr/bin/env python3
"""
Script to fix the admin_rewards.html form layout - restore missing fields
"""

# Read the file
with open('d:/BTgame/templates/admin_rewards.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the broken form section
old_form = '''            <div class="grid grid-cols-2 gap-4">
                <div>
                    <label class="block text-sm font-semibold text-gray-300 mb-2">Cost (Points) *</label>
                    <input type="number" name="cost" min="1" required
                        class="w-full bg-white/10 border border-white/20 rounded-lg px-4 py-3 text-white">
                </div>
                <div>
                    <button type="submit"
                        class="flex-1 bg-gradient-to-r from-yellow-600 to-orange-600 hover:from-yellow-700 hover:to-orange-700 text-white px-6 py-3 rounded-lg font-bold transition-all">
                        Create Reward
                    </button>
                    <button type="button" onclick="closeAddModal()"
                        class="bg-white/10 hover:bg-white/20 text-white px-6 py-3 rounded-lg font-semibold transition-colors">
                        Cancel
                    </button>
                </div>'''

new_form = '''            <div class="grid grid-cols-2 gap-4">
                <div>
                    <label class="block text-sm font-semibold text-gray-300 mb-2">Cost (Points) *</label>
                    <input type="number" name="cost" min="1" required
                        class="w-full bg-white/10 border border-white/20 rounded-lg px-4 py-3 text-white">
                </div>
                <div>
                    <label class="block text-sm font-semibold text-gray-300 mb-2">Stock (Leave empty for unlimited)</label>
                    <input type="number" name="stock" min="0"
                        class="w-full bg-white/10 border border-white/20 rounded-lg px-4 py-3 text-white">
                </div>
            </div>
            <div>
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
            </div>
            <div>
                <label class="block text-sm font-semibold text-gray-300 mb-2">Image URL</label>
                <input type="url" name="image_url"
                    class="w-full bg-white/10 border border-white/20 rounded-lg px-4 py-3 text-white">
            </div>
            <div class="flex gap-3 pt-4">
                <button type="submit"
                    class="flex-1 bg-gradient-to-r from-yellow-600 to-orange-600 hover:from-yellow-700 hover:to-orange-700 text-white px-6 py-3 rounded-lg font-bold transition-all">
                    Create Reward
                </button>
                <button type="button" onclick="closeAddModal()"
                    class="bg-white/10 hover:bg-white/20 text-white px-6 py-3 rounded-lg font-semibold transition-colors">
                    Cancel
                </button>
            </div>'''

content = content.replace(old_form, new_form)

# Write back
with open('d:/BTgame/templates/admin_rewards.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Admin rewards form layout fixed!")
