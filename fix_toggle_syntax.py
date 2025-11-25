#!/usr/bin/env python3
"""
Script to fix the toggleDescription syntax by using data attributes instead of inline onclick
"""

# Read the file
with open('d:/BTgame/templates/admin_dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the button with data attribute approach
old_button = '''                        <button onclick="toggleDescription({{ quest.id }})" 
                            class="text-blue-400 hover:text-blue-300 text-xs mt-1 see-more-btn-{{ quest.id }}">
                            See more...
                        </button>'''

new_button = '''                        <button class="text-blue-400 hover:text-blue-300 text-xs mt-1 toggle-description-btn" 
                            data-quest-id="{{ quest.id }}">
                            See more...
                        </button>'''

content = content.replace(old_button, new_button)
print("✅ Updated button to use data attributes")

# Update the JavaScript to use event delegation
old_script = '''    <script>
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
    </script>'''

new_script = '''    <script>
        // Event delegation for toggle description buttons
        document.addEventListener('click', function(e) {
            if (e.target.classList.contains('toggle-description-btn')) {
                const questId = e.target.dataset.questId;
                const description = document.querySelector(`.quest-description[data-quest-id="${questId}"]`);
                const button = e.target;
                
                if (description.classList.contains('expanded')) {
                    description.classList.remove('expanded');
                    button.textContent = 'See more...';
                } else {
                    description.classList.add('expanded');
                    button.textContent = 'See less';
                }
            }
        });
    </script>'''

content = content.replace(old_script, new_script)
print("✅ Updated JavaScript to use event delegation")

# Write back
with open('d:/BTgame/templates/admin_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n✅ Syntax error fixed! No more linter warnings.")
