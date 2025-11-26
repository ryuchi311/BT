import sys
import os
# Add parent directory to path to import app and models
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from app import app
from models import db
from sqlalchemy import text

def migrate_quest_code():
    """Add verification_code column to Quest table"""
    with app.app_context():
        print("Adding verification_code field to Quest table...")
        
        try:
            # Check if column already exists
            result = db.session.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='quest' AND column_name='verification_code'
            """))
            
            if result.fetchone():
                print("✓ verification_code column already exists")
                return
            
            # Add verification_code column
            db.session.execute(text("""
                ALTER TABLE "quest" 
                ADD COLUMN verification_code VARCHAR(32)
            """))
            
            db.session.commit()
            print("✓ Successfully added verification_code column")
            
        except Exception as e:
            print(f"✗ Error during migration: {e}")
            db.session.rollback()
            raise

if __name__ == '__main__':
    print("\n🔄 Starting quest verification_code migration...\n")
    migrate_quest_code()
    print("\n✅ Quest verification_code migration completed successfully!\n")
