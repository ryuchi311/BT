#!/usr/bin/env python3
"""
Script to add daily check-in card UI to quests.html
"""

# Read the file
with open('d:/BTgame/templates/quests.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find the line with quest icon display and add daily_checkin case
for i, line in enumerate(lines):
    # Add daily_checkin icon case
    if '{% elif quest.quest_type == \'visit\' %}' in line:
        lines[i] = line.replace(
            '{% elif quest.quest_type == \'visit\' %}',
            '''{% elif quest.quest_type == 'daily_checkin' %}
                    <span class="filter drop-shadow-[0_0_5px_rgba(251,146,60,0.8)]">📅</span>
                    {% elif quest.quest_type == 'visit' %}'''
        )
    
    # Replace the Start button with conditional check-in button
    if '<button onclick="completeQuest(\'{{ quest.id }}\')"' in line:
        # Find the closing button tag
        button_start = i
        button_end = i
        for j in range(i, min(i+10, len(lines))):
            if '</button>' in lines[j]:
                button_end = j
                break
        
        # Replace the button section
        new_button = '''            {% if quest.quest_type == 'daily_checkin' %}
            {% set status = checkin_status.get(quest.id, {'checked_in': False, 'streak': 0}) %}
            {% if status['checked_in'] %}
            <div class="text-center">
                <div class="bg-green-600/20 border border-green-500/30 text-green-300 px-6 py-2.5 rounded-lg font-bold">
                    ✓ Checked In
                </div>
                <div class="text-orange-400 font-bold text-sm mt-1">
                    🔥 {{ status['streak'] }} Day Streak
                </div>
            </div>
            {% else %}
            <div class="text-center">
                <button onclick="checkIn('{{ quest.id }}')"
                    class="relative overflow-hidden bg-gradient-to-r from-orange-600 to-orange-700 hover:from-orange-500 hover:to-orange-600 text-white px-6 py-2.5 rounded-lg font-bold tracking-wider uppercase text-sm transition-all transform hover:-translate-y-0.5 shadow-lg shadow-orange-900/50">
                    <span class="relative z-10">Check In</span>
                </button>
                {% if status['streak'] > 0 %}
                <div class="text-orange-400 font-bold text-sm mt-1">
                    🔥 {{ status['streak'] }} Day Streak
                </div>
                {% endif %}
            </div>
            {% endif %}
            {% else %}
            <button onclick="completeQuest('{{ quest.id }}')"
                class="relative overflow-hidden bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-500 hover:to-blue-600 text-white px-6 py-2.5 rounded-lg font-bold tracking-wider uppercase text-sm transition-all transform hover:-translate-y-0.5 shadow-lg shadow-blue-900/50">
                <span class="relative z-10">Start</span>
                <div
                    class="absolute inset-0 bg-white/20 transform -skew-x-12 -translate-x-full group-hover:animate-shine">
                </div>
            </button>
            {% endif %}
'''
        # Replace lines from button_start to button_end
        lines[button_start:button_end+1] = [new_button]
        break

# Write back
with open('d:/BTgame/templates/quests.html', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("✅ Daily check-in UI added to quests.html!")
