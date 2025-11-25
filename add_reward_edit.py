#!/usr/bin/env python3
"""
Script to add Edit functionality to admin_rewards.html
"""

# Read the file
with open('d:/BTgame/templates/admin_rewards.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add Edit button next to Enable/Disable button
old_buttons = '''            <div class="flex gap-2">
                <button onclick="toggleReward({{ reward.id }}, {{ 'true' if reward.is_active else 'false' }})"
                    class="flex-1 {% if reward.is_active %}bg-yellow-600 hover:bg-yellow-700{% else %}bg-green-600 hover:bg-green-700{% endif %} text-white px-3 py-2 rounded-lg text-sm font-semibold transition-colors">
                    {% if reward.is_active %}Disable{% else %}Enable{% endif %}
                </button>
                <button onclick="deleteReward({{ reward.id }})"
                    class="bg-red-600 hover:bg-red-700 text-white px-3 py-2 rounded-lg text-sm font-semibold transition-colors">
                    Delete
                </button>
            </div>'''

new_buttons = '''            <div class="flex gap-2">
                <button onclick="openEditModal({{ reward.id }})"
                    class="flex-1 bg-blue-600 hover:bg-blue-700 text-white px-3 py-2 rounded-lg text-sm font-semibold transition-colors">
                    Edit
                </button>
                <button onclick="toggleReward({{ reward.id }}, {{ 'true' if reward.is_active else 'false' }})"
                    class="flex-1 {% if reward.is_active %}bg-yellow-600 hover:bg-yellow-700{% else %}bg-green-600 hover:bg-green-700{% endif %} text-white px-3 py-2 rounded-lg text-sm font-semibold transition-colors">
                    {% if reward.is_active %}Disable{% else %}Enable{% endif %}
                </button>
                <button onclick="deleteReward({{ reward.id }})"
                    class="bg-red-600 hover:bg-red-700 text-white px-3 py-2 rounded-lg text-sm font-semibold transition-colors">
                    Delete
                </button>
            </div>'''

content = content.replace(old_buttons, new_buttons)
print("✅ Added Edit button")

# 2. Add Edit Modal after Add Modal
edit_modal = '''
<!-- Edit Reward Modal -->
<div id="editRewardModal"
    class="hidden fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm">
    <div
        class="bg-gradient-to-br from-gray-900 to-gray-800 border border-white/20 rounded-2xl p-6 max-w-2xl w-full mx-4">
        <h2 class="text-2xl font-bold text-white mb-6">Edit Reward</h2>
        <form id="editRewardForm" method="POST" class="space-y-4">
            <input type="hidden" id="editRewardId" name="reward_id">
            <div>
                <label class="block text-sm font-semibold text-gray-300 mb-2">Title *</label>
                <input type="text" id="editTitle" name="title" required
                    class="w-full bg-white/10 border border-white/20 rounded-lg px-4 py-3 text-white">
            </div>
            <div>
                <label class="block text-sm font-semibold text-gray-300 mb-2">Description</label>
                <textarea id="editDescription" name="description" rows="2"
                    class="w-full bg-white/10 border border-white/20 rounded-lg px-4 py-3 text-white"></textarea>
            </div>
            <div class="grid grid-cols-2 gap-4">
                <div>
                    <label class="block text-sm font-semibold text-gray-300 mb-2">Cost (Points) *</label>
                    <input type="number" id="editCost" name="cost" min="1" required
                        class="w-full bg-white/10 border border-white/20 rounded-lg px-4 py-3 text-white">
                </div>
                <div>
                    <label class="block text-sm font-semibold text-gray-300 mb-2">Stock (Leave empty for unlimited)</label>
                    <input type="number" id="editStock" name="stock" min="0"
                        class="w-full bg-white/10 border border-white/20 rounded-lg px-4 py-3 text-white">
                </div>
            </div>
            <div>
                <label class="block text-sm font-semibold text-gray-300 mb-2">Category</label>
                <select id="editCategory" name="category"
                    class="w-full bg-white/10 border border-white/20 rounded-lg px-4 py-3 text-white"
                    style="color: white;">
                    <option value="" style="background-color: #1f2937; color: #9ca3af;">Select category...</option>
                    <option value="Physical" style="background-color: #1f2937; color: white;">📦 Physical Item</option>
                    <option value="Digital" style="background-color: #1f2937; color: white;">💻 Digital Good</option>
                    <option value="Voucher" style="background-color: #1f2937; color: white;">🎟️ Voucher/Coupon</option>
                    <option value="Premium" style="background-color: #1f2937; color: white;">⭐ Premium Access</option>
                    <option value="Merchandise" style="background-color: #1f2937; color: white;">👕 Merchandise</option>
                    <option value="Other" style="background-color: #1f2937; color: white;">🎁 Other</option>
                </select>
            </div>
            <div>
                <label class="block text-sm font-semibold text-gray-300 mb-2">Image URL</label>
                <input type="url" id="editImageUrl" name="image_url"
                    class="w-full bg-white/10 border border-white/20 rounded-lg px-4 py-3 text-white">
            </div>
            <div class="flex gap-3 pt-4">
                <button type="submit"
                    class="flex-1 bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white px-6 py-3 rounded-lg font-bold transition-all">
                    Update Reward
                </button>
                <button type="button" onclick="closeEditModal()"
                    class="bg-white/10 hover:bg-white/20 text-white px-6 py-3 rounded-lg font-semibold transition-colors">
                    Cancel
                </button>
            </div>
        </form>
    </div>
</div>

'''

# Insert edit modal before the script tag
content = content.replace('<script>', edit_modal + '<script>')
print("✅ Added Edit Modal")

# 3. Add JavaScript functions for edit functionality
edit_functions = '''
    // Store rewards data for editing
    const rewardsData = {{ rewards | tojson }};

    function openEditModal(rewardId) {
        const reward = rewardsData.find(r => r.id === rewardId);
        if (!reward) return;

        document.getElementById('editRewardId').value = reward.id;
        document.getElementById('editTitle').value = reward.title;
        document.getElementById('editDescription').value = reward.description || '';
        document.getElementById('editCost').value = reward.cost;
        document.getElementById('editStock').value = reward.stock || '';
        document.getElementById('editCategory').value = reward.category || '';
        document.getElementById('editImageUrl').value = reward.image_url || '';
        
        document.getElementById('editRewardForm').action = `/admin/rewards/edit/${rewardId}`;
        document.getElementById('editRewardModal').classList.remove('hidden');
    }

    function closeEditModal() {
        document.getElementById('editRewardModal').classList.add('hidden');
    }

'''

# Add edit functions after openAddModal function
content = content.replace('    function closeAddModal() {', edit_functions + '    function closeAddModal() {')
print("✅ Added Edit JavaScript functions")

# Write back
with open('d:/BTgame/templates/admin_rewards.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n✅ Edit functionality added to Reward Management!")
