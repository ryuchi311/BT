#!/usr/bin/env python3
"""
Script to update category filters with Font Awesome icons and mobile-friendly design
"""

# Read the file
with open('d:/BTgame/templates/quests.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the filter buttons with icon-based design
old_filters = '''<!-- Category Filters -->
<div class="mb-6 flex flex-wrap gap-3 justify-center">
    <button onclick="filterQuests('all')" 
        class="filter-btn active px-6 py-2.5 rounded-lg font-bold text-sm transition-all transform hover:scale-105"
        data-category="all">
        🎯 All Quests
    </button>
    <button onclick="filterQuests('Social')" 
        class="filter-btn px-6 py-2.5 rounded-lg font-bold text-sm transition-all transform hover:scale-105"
        data-category="Social">
        📱 Social
    </button>
    <button onclick="filterQuests('Engagement')" 
        class="filter-btn px-6 py-2.5 rounded-lg font-bold text-sm transition-all transform hover:scale-105"
        data-category="Engagement">
        💬 Engagement
    </button>
    <button onclick="filterQuests('Educational')" 
        class="filter-btn px-6 py-2.5 rounded-lg font-bold text-sm transition-all transform hover:scale-105"
        data-category="Educational">
        📚 Educational
    </button>
    <button onclick="filterQuests('Reward')" 
        class="filter-btn px-6 py-2.5 rounded-lg font-bold text-sm transition-all transform hover:scale-105"
        data-category="Reward">
        🎁 Reward
    </button>
</div>'''

new_filters = '''<!-- Category Filters -->
<div class="mb-6 flex flex-wrap gap-2 justify-center">
    <button onclick="filterQuests('all')" 
        class="filter-btn active flex flex-col items-center gap-1 px-4 py-3 rounded-xl font-bold text-xs transition-all transform hover:scale-105"
        data-category="all">
        <i class="fas fa-th text-xl"></i>
        <span class="hidden sm:inline">All</span>
    </button>
    <button onclick="filterQuests('Social')" 
        class="filter-btn flex flex-col items-center gap-1 px-4 py-3 rounded-xl font-bold text-xs transition-all transform hover:scale-105"
        data-category="Social">
        <i class="fas fa-users text-xl"></i>
        <span class="hidden sm:inline">Social</span>
    </button>
    <button onclick="filterQuests('Engagement')" 
        class="filter-btn flex flex-col items-center gap-1 px-4 py-3 rounded-xl font-bold text-xs transition-all transform hover:scale-105"
        data-category="Engagement">
        <i class="fas fa-comments text-xl"></i>
        <span class="hidden sm:inline">Engage</span>
    </button>
    <button onclick="filterQuests('Educational')" 
        class="filter-btn flex flex-col items-center gap-1 px-4 py-3 rounded-xl font-bold text-xs transition-all transform hover:scale-105"
        data-category="Educational">
        <i class="fas fa-graduation-cap text-xl"></i>
        <span class="hidden sm:inline">Learn</span>
    </button>
    <button onclick="filterQuests('Reward')" 
        class="filter-btn flex flex-col items-center gap-1 px-4 py-3 rounded-xl font-bold text-xs transition-all transform hover:scale-105"
        data-category="Reward">
        <i class="fas fa-gift text-xl"></i>
        <span class="hidden sm:inline">Reward</span>
    </button>
</div>'''

content = content.replace(old_filters, new_filters)
print("✅ Updated filter buttons with Font Awesome icons")

# Write back
with open('d:/BTgame/templates/quests.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n✅ Filter buttons updated with icons and mobile-friendly design!")
print("Features:")
print("  - Icon-based design (Font Awesome)")
print("  - Mobile: Shows only icons")
print("  - Desktop: Shows icons + labels")
print("  - Compact and touch-friendly")
