#!/usr/bin/env python3
"""
Script to add success toast for reward form submissions
"""

# Read the file
with open('d:/BTgame/templates/admin_rewards.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add form submission handler for add reward form
add_form_handler = '''
    // Handle Add Reward form submission
    document.querySelector('#addRewardModal form').addEventListener('submit', function(e) {
        showInfo('Creating reward...');
        sessionStorage.setItem('rewardAction', 'created');
    });
    
    // Handle Edit Reward form submission
    document.getElementById('editRewardForm').addEventListener('submit', function(e) {
        showInfo('Updating reward...');
        sessionStorage.setItem('rewardAction', 'updated');
    });
    
    // Check for success message on page load
    window.addEventListener('DOMContentLoaded', function() {
        const action = sessionStorage.getItem('rewardAction');
        if (action) {
            sessionStorage.removeItem('rewardAction');
            showSuccess(`Reward ${action} successfully!`);
        }
    });
'''

# Add before the closing script tag
if '</script>' in content and 'rewardAction' not in content:
    content = content.replace('</script>', add_form_handler + '\n</script>')
    print("✅ Added reward form submission handlers")

# Write back
with open('d:/BTgame/templates/admin_rewards.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Toast notifications added for reward operations!")
