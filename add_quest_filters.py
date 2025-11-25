#!/usr/bin/env python3
"""
Script to add category filter buttons to Quest Log (quests.html)
"""

# Read the file
with open('d:/BTgame/templates/quests.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add filter buttons after the header, before the quest grid
filter_buttons = '''
<!-- Category Filters -->
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
</div>

'''

# Insert filter buttons before the quest grid
if '<div class="space-y-4">' in content and 'filter-btn' not in content:
    content = content.replace(
        '<div class="space-y-4">',
        filter_buttons + '<div class="space-y-4" id="questsContainer">'
    )
    print("✅ Added category filter buttons")

# Add data-category attribute to quest cards
old_quest_div = '''    <div class="group relative bg-white/5 backdrop-blur-md border border-white/10 rounded-xl p-5 transition-all duration-300 hover:bg-white/10 hover:scale-[1.02] hover:shadow-[0_0_20px_rgba(59,130,246,0.3)] animate-fade-in"
        data-delay="{{ loop.index0 * 100 }}">'''

new_quest_div = '''    <div class="quest-card group relative bg-white/5 backdrop-blur-md border border-white/10 rounded-xl p-5 transition-all duration-300 hover:bg-white/10 hover:scale-[1.02] hover:shadow-[0_0_20px_rgba(59,130,246,0.3)] animate-fade-in"
        data-delay="{{ loop.index0 * 100 }}"
        data-category="{{ quest.category or 'Uncategorized' }}">'''

content = content.replace(old_quest_div, new_quest_div)
print("✅ Added category data attribute to quest cards")

# Add CSS and JavaScript for filtering
filter_script = '''
<style>
    .filter-btn {
        background: rgba(255, 255, 255, 0.1);
        color: #9ca3af;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .filter-btn:hover {
        background: rgba(255, 255, 255, 0.15);
        color: white;
    }
    
    .filter-btn.active {
        background: linear-gradient(to right, #9333ea, #3b82f6);
        color: white;
        border-color: transparent;
        box-shadow: 0 0 20px rgba(147, 51, 234, 0.5);
    }
    
    .quest-card.hidden {
        display: none;
    }
</style>

<script>
    function filterQuests(category) {
        const questCards = document.querySelectorAll('.quest-card');
        const filterBtns = document.querySelectorAll('.filter-btn');
        
        // Update active button
        filterBtns.forEach(btn => {
            if (btn.dataset.category === category) {
                btn.classList.add('active');
            } else {
                btn.classList.remove('active');
            }
        });
        
        // Filter quest cards
        questCards.forEach(card => {
            const cardCategory = card.dataset.category;
            
            if (category === 'all' || cardCategory === category) {
                card.classList.remove('hidden');
                // Re-trigger animation
                card.style.animation = 'none';
                setTimeout(() => {
                    card.style.animation = '';
                }, 10);
            } else {
                card.classList.add('hidden');
            }
        });
    }
</script>
'''

# Add before closing body tag or before existing script
if '</script>' in content and 'filterQuests' not in content:
    # Find the last </script> tag
    last_script_pos = content.rfind('</script>')
    if last_script_pos != -1:
        insert_pos = content.find('\n', last_script_pos) + 1
        content = content[:insert_pos] + filter_script + content[insert_pos:]
        print("✅ Added filter JavaScript and CSS")

# Write back
with open('d:/BTgame/templates/quests.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n✅ Category filters added to Quest Log!")
print("Users can now filter by:")
print("  - All Quests")
print("  - Social")
print("  - Engagement")
print("  - Educational")
print("  - Reward")
