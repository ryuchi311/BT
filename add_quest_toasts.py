#!/usr/bin/env python3
"""
Script to add success/failure toast notifications to quest form submissions
"""

# Read the file
with open('d:/BTgame/templates/admin_dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the form submission and add success toast
# Look for the quest form element
if '<form id="questForm"' in content:
    # Add event listener for form submission success
    form_success_handler = '''
    // Handle form submission with toast notifications
    document.getElementById('questForm').addEventListener('submit', function(e) {
        const isEdit = document.getElementById('questId').value !== '';
        const action = isEdit ? 'updated' : 'created';
        
        // Show loading toast
        showInfo(`${isEdit ? 'Updating' : 'Creating'} quest...`);
        
        // The form will submit normally, but we'll show success on next page load
        sessionStorage.setItem('questAction', action);
    });
    
    // Check for success message on page load
    window.addEventListener('DOMContentLoaded', function() {
        const action = sessionStorage.getItem('questAction');
        if (action) {
            sessionStorage.removeItem('questAction');
            showSuccess(`Quest ${action} successfully!`);
        }
    });
'''
    
    # Add after the existing DOMContentLoaded event listener
    if "document.addEventListener('DOMContentLoaded', function () {" in content:
        # Find the closing of the existing DOMContentLoaded
        insert_pos = content.find('        });', content.find("document.addEventListener('DOMContentLoaded', function () {"))
        if insert_pos != -1:
            insert_pos = content.find('\n', insert_pos) + 1
            content = content[:insert_pos] + form_success_handler + content[insert_pos:]
            print("✅ Added form submission toast handler")
    
# Add toast for delete and toggle operations
replacements = [
    (
        "if (response.ok) location.reload();",
        "if (response.ok) { showSuccess('Quest deleted successfully'); setTimeout(() => location.reload(), 1000); }"
    ),
]

for old, new in replacements:
    if old in content:
        content = content.replace(old, new)
        print(f"✅ Added success toast for operation")

# Write back
with open('d:/BTgame/templates/admin_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n✅ Toast notifications added for quest operations!")
