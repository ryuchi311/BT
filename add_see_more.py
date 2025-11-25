#!/usr/bin/env python3
"""
Script to add "See more..." functionality to quest card descriptions
"""

# Read the file
with open('d:/BTgame/templates/admin_dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the description line and replace it with expandable version
old_description = '''                    <p class="text-sm text-gray-300 line-clamp-2">{{ quest.description or 'No description' }}</p>'''

new_description = '''                    <div class="quest-description-container">
                        <p class="text-sm text-gray-300 quest-description" data-quest-id="{{ quest.id }}">
                            {{ quest.description or 'No description' }}
                        </p>
                        {% if quest.description and quest.description|length > 100 %}
                        <button onclick="toggleDescription({{ quest.id }})" 
                            class="text-blue-400 hover:text-blue-300 text-xs mt-1 see-more-btn-{{ quest.id }}">
                            See more...
                        </button>
                        {% endif %}
                    </div>'''

content = content.replace(old_description, new_description)
print("✅ Updated description HTML")

# Add CSS and JavaScript for the see more functionality
see_more_script = '''
    <style>
        .quest-description {
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
            transition: all 0.3s ease;
        }
        
        .quest-description.expanded {
            -webkit-line-clamp: unset;
        }
    </style>
    
    <script>
        function toggleDescription(questId) {
            const description = document.querySelector(`.quest-description[data-quest-id="${questId}"]`);
            const button = document.querySelector(`.see-more-btn-${questId}`);
            
            if (description.classList.contains('expanded')) {
                description.classList.remove('expanded');
                button.textContent = 'See more...';
            } else {
                description.classList.add('expanded');
                button.textContent = 'See less';
            }
        }
    </script>
'''

# Add before closing body tag
if '</body>' in content and 'toggleDescription' not in content:
    content = content.replace('</body>', see_more_script + '\n</body>')
    print("✅ Added CSS and JavaScript for see more functionality")

# Write back
with open('d:/BTgame/templates/admin_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n✅ 'See more...' functionality added to quest descriptions!")
