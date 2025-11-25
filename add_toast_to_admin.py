#!/usr/bin/env python3
"""
Script to add toast notifications to admin_dashboard.html
"""

# Read the file
with open('d:/BTgame/templates/admin_dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Read the toast component
with open('d:/BTgame/templates/toast_component.html', 'r', encoding='utf-8') as f:
    toast_component = f.read()

# Add toast container before closing body tag
if '</body>' in content and 'toast-container' not in content:
    content = content.replace('</body>', f'{toast_component}\n</body>')
    print("✅ Toast component added to admin_dashboard.html")
else:
    print("⚠️  Toast already exists or </body> not found")

# Replace alert() calls with toast notifications
replacements = [
    ("alert('Quest created successfully')", "showSuccess('Quest created successfully')"),
    ("alert('Quest updated successfully')", "showSuccess('Quest updated successfully')"),
    ("alert('Quest deleted successfully')", "showSuccess('Quest deleted successfully')"),
    ("alert('Error creating quest')", "showError('Error creating quest')"),
    ("alert('Error updating quest')", "showError('Error updating quest')"),
    ("alert('Error deleting quest')", "showError('Error deleting quest')"),
    ("alert('Error toggling quest')", "showError('Error toggling quest')"),
    ("alert('Error: ' + err)", "showError('Error: ' + err)"),
]

for old, new in replacements:
    if old in content:
        content = content.replace(old, new)
        print(f"✅ Replaced: {old}")

# Write back
with open('d:/BTgame/templates/admin_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n✅ Toast notifications added to admin dashboard!")
