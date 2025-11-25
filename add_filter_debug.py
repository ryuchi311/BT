#!/usr/bin/env python3
"""
Script to add console logging to filter function for debugging
"""

# Read the file
with open('d:/BTgame/templates/quests.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and update the filterQuests function to add logging
old_filter_func = '''    // Category Filter Functionality
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
    }'''

new_filter_func = '''    // Category Filter Functionality
    function filterQuests(category) {
        console.log('Filtering by category:', category);
        const questCards = document.querySelectorAll('.quest-card');
        const filterBtns = document.querySelectorAll('.filter-btn');
        
        console.log('Found', questCards.length, 'quest cards');
        
        // Update active button
        filterBtns.forEach(btn => {
            if (btn.dataset.category === category) {
                btn.classList.add('active');
            } else {
                btn.classList.remove('active');
            }
        });
        
        // Filter quest cards
        let visibleCount = 0;
        questCards.forEach(card => {
            const cardCategory = card.dataset.category;
            console.log('Card category:', cardCategory, 'Filter:', category);
            
            if (category === 'all' || cardCategory === category) {
                card.classList.remove('hidden');
                visibleCount++;
                // Re-trigger animation
                card.style.animation = 'none';
                setTimeout(() => {
                    card.style.animation = '';
                }, 10);
            } else {
                card.classList.add('hidden');
            }
        });
        
        console.log('Visible cards:', visibleCount);
    }'''

if old_filter_func in content:
    content = content.replace(old_filter_func, new_filter_func)
    print("✅ Added console logging to filter function")
else:
    print("⚠️  Filter function not found or already updated")

# Write back
with open('d:/BTgame/templates/quests.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Debug logging added!")
