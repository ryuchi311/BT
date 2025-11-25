#!/usr/bin/env python3
"""
Script to add toast notifications to admin_rewards.html
"""

# Read the file
with open('d:/BTgame/templates/admin_rewards.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Read the toast component
with open('d:/BTgame/templates/toast_component.html', 'r', encoding='utf-8') as f:
    toast_component = f.read()

# Add toast container before closing body tag or before {% endblock %}
if '{% endblock %}' in content and 'toast-container' not in content:
    content = content.replace('{% endblock %}', f'{toast_component}\n{{% endblock %}}')
    print("✅ Toast component added to admin_rewards.html")
else:
    print("⚠️  Toast already exists or endblock not found")

# Replace alert() calls with toast notifications
replacements = [
    ("alert('Error toggling reward')", "showError('Error toggling reward')"),
    ("alert('Error deleting reward')", "showError('Error deleting reward')"),
    ("alert('Error: ' + err)", "showError('Error: ' + err)"),
]

for old, new in replacements:
    if old in content:
        content = content.replace(old, new)
        print(f"✅ Replaced: {old}")

# Add success messages after reload
# Replace location.reload() with toast + reload
if 'if (data.success) location.reload();' in content:
    content = content.replace(
        'if (data.success) location.reload();',
        "if (data.success) { showSuccess('Reward updated successfully'); setTimeout(() => location.reload(), 1000); }"
    )
    print("✅ Added success toast for reward updates")

# Write back
with open('d:/BTgame/templates/admin_rewards.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("\n✅ Toast notifications added to admin rewards!")
