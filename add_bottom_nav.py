#!/usr/bin/env python3
"""
Script to add bottom navigation to admin_dashboard.html
"""

# Read the original file
with open('d:/BTgame/templates/admin_dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add bottom padding to body tag
content = content.replace(
    '<body class="bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 min-h-screen p-4 md:p-8">',
    '<body class="bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 min-h-screen p-4 md:p-8 pb-24">'
)

# 2. Add event listener for bottom button before closing script tag
event_listener_code = '''            // Bottom navigation button
            const addQuestBtnBottom = document.getElementById('addQuestBtnBottom');
            if (addQuestBtnBottom) {
                addQuestBtnBottom.addEventListener('click', openAddModal);
            }
        });
    </script>'''

content = content.replace('        });\n    </script>', event_listener_code)

# 3. Add bottom navigation HTML before closing body tag
bottom_nav_html = '''
    <!-- Quick Actions Bottom Navigation -->
    <div class="fixed bottom-0 left-0 right-0 bg-gradient-to-t from-gray-900 via-gray-900/95 to-transparent backdrop-blur-lg border-t border-white/10 z-50">
        <div class="max-w-7xl mx-auto px-4 py-3">
            <div class="flex items-center justify-center gap-3">
                <a href="{{ url_for('admin.verification_queue') }}"
                    class="flex-1 max-w-xs bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-700 hover:to-purple-700 text-white px-4 py-3 rounded-xl font-bold text-sm md:text-base transition-all transform active:scale-95 shadow-lg flex items-center justify-center gap-2">
                    <span class="text-xl">📋</span>
                    <span class="hidden sm:inline">Verification Queue</span>
                    <span class="sm:hidden">Queue</span>
                </a>
                <button id="addQuestBtnBottom"
                    class="flex-1 max-w-xs bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white px-4 py-3 rounded-xl font-bold text-sm md:text-base transition-all transform active:scale-95 shadow-lg flex items-center justify-center gap-2">
                    <span class="text-xl">➕</span>
                    <span class="hidden sm:inline">Add New Quest</span>
                    <span class="sm:hidden">Add Quest</span>
                </button>
            </div>
        </div>
    </div>
</body>'''

content = content.replace('</body>', bottom_nav_html)

# Write the modified content
with open('d:/BTgame/templates/admin_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Bottom navigation added successfully!")
