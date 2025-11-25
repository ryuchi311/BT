#!/usr/bin/env python3
"""
Script to add checkIn JavaScript function to quests.html
"""

# Read the file
with open('d:/BTgame/templates/quests.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Add checkIn function before the closing script tag
checkin_function = '''
    function checkIn(questId) {
        // Add loading state to button
        const btn = event.currentTarget;
        const originalText = btn.innerHTML;
        btn.innerHTML = '<span class="relative z-10">...</span>';
        btn.disabled = true;
        btn.classList.add('opacity-75', 'cursor-not-allowed');

        fetch(`/quests/checkin/${questId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    // Show success message with streak
                    alert(`✅ Check-in successful!\\n🔥 ${data.streak} day streak!\\n💰 +${data.points_earned} points`);
                    location.reload();
                } else {
                    alert(data.error || 'Check-in failed');
                    btn.innerHTML = originalText;
                    btn.disabled = false;
                    btn.classList.remove('opacity-75', 'cursor-not-allowed');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred');
                btn.innerHTML = originalText;
                btn.disabled = false;
                btn.classList.remove('opacity-75', 'cursor-not-allowed');
            });
    }
</script>'''

# Replace the closing script tag
content = content.replace('</script>', checkin_function)

# Write back
with open('d:/BTgame/templates/quests.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Check-in JavaScript function added to quests.html!")
