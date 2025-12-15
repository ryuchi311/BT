"""
SQLite Database Migration Script
Adds social media columns to User table
"""

from app import app, db
from sqlalchemy import text, inspect

def column_exists(table_name, column_name):
    """Check if a column exists in a table"""
    inspector = inspect(db.engine)
    columns = [col['name'] for col in inspector.get_columns(table_name)]
    return column_name in columns

def migrate_database():
    with app.app_context():
        print("Starting social media fields migration...")
        
        try:
            with db.engine.begin() as conn:
                print("\n--- Migrating User table ---")
                
                # Check and add twitter_handle column
                if not column_exists('user', 'twitter_handle'):
                    conn.execute(text('ALTER TABLE "user" ADD COLUMN twitter_handle VARCHAR(64)'))
                    print("✓ Added 'twitter_handle' column")
                else:
                    print("  'twitter_handle' column already exists")
                
                # Check and add discord_id column
                if not column_exists('user', 'discord_id'):
                    conn.execute(text('ALTER TABLE "user" ADD COLUMN discord_id VARCHAR(64)'))
                    print("✓ Added 'discord_id' column")
                else:
                    print("  'discord_id' column already exists")
                
                # Check and add facebook_profile column
                if not column_exists('user', 'facebook_profile'):
                    conn.execute(text('ALTER TABLE "user" ADD COLUMN facebook_profile VARCHAR(256)'))
                    print("✓ Added 'facebook_profile' column")
                else:
                    print("  'facebook_profile' column already exists")

                # Check and add instagram_profile column
                if not column_exists('user', 'instagram_profile'):
                    conn.execute(text('ALTER TABLE "user" ADD COLUMN instagram_profile VARCHAR(256)'))
                    print("✓ Added 'instagram_profile' column")
                else:
                    print("  'instagram_profile' column already exists")

                # Check and add youtube_handle column
                if not column_exists('user', 'youtube_handle'):
                    conn.execute(text('ALTER TABLE "user" ADD COLUMN youtube_handle VARCHAR(64)'))
                    print("✓ Added 'youtube_handle' column")
                else:
                    print("  'youtube_handle' column already exists")
            
            print("\n✅ Social media migration completed successfully!")
            
        except Exception as e:
            print(f"\n❌ Migration failed: {str(e)}")
            raise

if __name__ == '__main__':
    migrate_database()
