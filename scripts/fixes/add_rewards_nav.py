#!/usr/bin/env python3
"""
Script to add Rewards button to Quick Actions bottom navigation
"""

# Read the file
with open('d:/BTgame/templates/admin_dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the bottom navigation section to add Rewards button
old_nav = '''                <a href="{{ url_for('admin.verification_queue') }}"
                    class="flex-1 max-w-xs bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white px-4 py-3 rounded-xl font-bold text-sm md:text-base transition-all transform active:scale-95 shadow-lg flex items-center justify-center gap-2">
                    <span class="text-xl">📋</span>
                    <span class="hidden sm:inline">Verification Queue</span>
                    <span class="sm:hidden">Queue</span>
                </a>
                <button id="addQuestBtnBottom"'''

new_nav = '''                <a href="{{ url_for('admin.verification_queue') }}"
                    class="flex-1 max-w-xs bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white px-4 py-3 rounded-xl font-bold text-sm md:text-base transition-all transform active:scale-95 shadow-lg flex items-center justify-center gap-2">
                    <span class="text-xl">📋</span>
                    <span class="hidden sm:inline">Verification Queue</span>
                    <span class="sm:hidden">Queue</span>
                </a>
                <a href="{{ url_for('admin.manage_rewards') }}"
                    class="flex-1 max-w-xs bg-gradient-to-r from-yellow-600 to-orange-600 hover:from-yellow-700 hover:to-orange-700 text-white px-4 py-3 rounded-xl font-bold text-sm md:text-base transition-all transform active:scale-95 shadow-lg flex items-center justify-center gap-2">
                    <span class="text-xl">🎁</span>
                    <span class="hidden sm:inline">Rewards</span>
                    <span class="sm:hidden">Rewards</span>
                </a>
                <button id="addQuestBtnBottom"'''

content = content.replace(old_nav, new_nav)

# Write back
with open('d:/BTgame/templates/admin_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Rewards button added to Quick Actions bottom navigation!")
