#!/usr/bin/env python3
"""
Script to replace emoji icons with Font Awesome icons in quests.html (Quest Log)
"""

# Read the file
with open('d:/BTgame/templates/quests.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace emoji icons with Font Awesome icons
old_icons = '''                    {% if quest.quest_type == 'telegram' %}
                    <span class="filter drop-shadow-[0_0_5px_rgba(56,189,248,0.8)]">✈️</span>
                    {% elif quest.quest_type == 'twitter' %}
                    <span class="filter drop-shadow-[0_0_5px_rgba(56,189,248,0.8)]">🐦</span>
                    {% elif quest.quest_type == 'youtube' %}
                    <span class="filter drop-shadow-[0_0_5px_rgba(239,68,68,0.8)]">▶️</span>
                    {% elif quest.quest_type == 'daily_checkin' %}
                    <span class="filter drop-shadow-[0_0_5px_rgba(251,146,60,0.8)]">📅</span>
                    {% elif quest.quest_type == 'visit' %}
                    <span class="filter drop-shadow-[0_0_5px_rgba(34,197,94,0.8)]">🔗</span>
                    {% endif %}'''

new_icons = '''                    {% if quest.quest_type == 'telegram' %}
                    <i class="fab fa-telegram text-4xl text-blue-400 filter drop-shadow-[0_0_10px_rgba(56,189,248,0.8)]"></i>
                    {% elif quest.quest_type == 'twitter' %}
                    <i class="fab fa-twitter text-4xl text-sky-400 filter drop-shadow-[0_0_10px_rgba(56,189,248,0.8)]"></i>
                    {% elif quest.quest_type == 'youtube' %}
                    <i class="fab fa-youtube text-4xl text-red-500 filter drop-shadow-[0_0_10px_rgba(239,68,68,0.8)]"></i>
                    {% elif quest.quest_type == 'daily_checkin' %}
                    <i class="fas fa-calendar-check text-4xl text-orange-400 filter drop-shadow-[0_0_10px_rgba(251,146,60,0.8)]"></i>
                    {% elif quest.quest_type == 'manual' %}
                    <i class="fas fa-hand-paper text-4xl text-purple-400 filter drop-shadow-[0_0_10px_rgba(168,85,247,0.8)]"></i>
                    {% elif quest.quest_type == 'visit' %}
                    <i class="fas fa-link text-4xl text-green-400 filter drop-shadow-[0_0_10px_rgba(34,197,94,0.8)]"></i>
                    {% endif %}'''

content = content.replace(old_icons, new_icons)
print("✅ Replaced quest type icons with Font Awesome icons")

# Write back
with open('d:/BTgame/templates/quests.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n✅ Quest Log icons updated to use Font Awesome!")
print("Icons now include:")
print("  - Telegram: fab fa-telegram (Blue with glow)")
print("  - Twitter: fab fa-twitter (Sky blue with glow)")
print("  - YouTube: fab fa-youtube (Red with glow)")
print("  - Daily Check-in: fas fa-calendar-check (Orange with glow)")
print("  - Manual: fas fa-hand-paper (Purple with glow)")
print("  - Website: fas fa-link (Green with glow)")
