import sys
import os
# Add parent directory to path to import app and models
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app import app
from models import db, Quest
from datetime import datetime, timedelta

def add_test_youtube_quest():
    """Add a test YouTube quest with verification code"""
    with app.app_context():
        print("Adding test YouTube quest...")
        
        # Check if a YouTube quest already exists
        existing = Quest.query.filter_by(quest_type='youtube', title='Watch Our Tutorial').first()
        
        if existing:
            print(f"✓ YouTube quest already exists (ID: {existing.id})")
            print(f"  Title: {existing.title}")
            print(f"  Verification Code: {existing.verification_code}")
            return
        
        # Create a new YouTube quest
        youtube_quest = Quest(
            title='Watch Our Tutorial',
            description='Watch our YouTube tutorial video and enter the code shown at the end',
            quest_type='youtube',
            points=50,
            icon='youtube',
            action_url='https://www.youtube.com/watch?v=dQw4w9WgXcQ',  # Replace with your actual video
            category='Educational',
            verification_code='QUEST2024',  # The secret code users must enter
            verification_type='auto',
            verification_instructions='Watch the video for 2 minutes, then enter the code shown in the video',
            is_active=True,
            expires_at=datetime.utcnow() + timedelta(days=30)  # Expires in 30 days
        )
        
        db.session.add(youtube_quest)
        db.session.commit()
        
        print(f"✅ Successfully created YouTube quest!")
        print(f"   Quest ID: {youtube_quest.id}")
        print(f"   Title: {youtube_quest.title}")
        print(f"   Points: {youtube_quest.points}")
        print(f"   YouTube URL: {youtube_quest.action_url}")
        print(f"   Verification Code: {youtube_quest.verification_code}")
        print(f"\n📝 To test:")
        print(f"   1. Visit http://127.0.0.1:5000/test-login to log in")
        print(f"   2. Go to quest list and click 'Start' on the YouTube quest")
        print(f"   3. Click 'Start Watch' and wait for 2-minute countdown")
        print(f"   4. Enter code: {youtube_quest.verification_code}")

if __name__ == '__main__':
    print("\n🎬 Creating Test YouTube Quest...\n")
    add_test_youtube_quest()
    print("\n✅ Done!\n")
