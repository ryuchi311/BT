#!/usr/bin/env python3
"""
Script to add Rewards link to the bottom navigation in base.html
"""

# Read the file
with open('d:/BTgame/templates/base.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the bottom navigation and add Rewards link after Quests
old_nav = '''        <a href="{{ url_for('quests.list_quests') }}" class="flex flex-col items-center text-gray-400 hover:text-white">
            <span class="text-xl">📜</span>
            <span class="text-xs">Quests</span>
        </a>
        <a href="{{ url_for('main.leaderboard') }}" class="flex flex-col items-center text-gray-400 hover:text-white">
            <span class="text-xl">🏆</span>
            <span class="text-xs">Rank</span>
        </a>'''

new_nav = '''        <a href="{{ url_for('quests.list_quests') }}" class="flex flex-col items-center text-gray-400 hover:text-white">
            <span class="text-xl">📜</span>
            <span class="text-xs">Quests</span>
        </a>
        <a href="{{ url_for('rewards.list_rewards') }}" class="flex flex-col items-center text-gray-400 hover:text-white">
            <span class="text-xl">🎁</span>
            <span class="text-xs">Rewards</span>
        </a>
        <a href="{{ url_for('main.leaderboard') }}" class="flex flex-col items-center text-gray-400 hover:text-white">
            <span class="text-xl">🏆</span>
            <span class="text-xs">Rank</span>
        </a>'''

content = content.replace(old_nav, new_nav)

# Write back
with open('d:/BTgame/templates/base.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Rewards link added to bottom navigation!")
