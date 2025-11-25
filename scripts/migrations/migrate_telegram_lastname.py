from app import app
from models import db
from sqlalchemy import text

def migrate_telegram_lastname():
    """Add last_name column to User table"""
    with app.app_context():
        print("Adding last_name field to User table...")
        
        try:
            # Check if column already exists
            result = db.session.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='user' AND column_name='last_name'
            """))
            
            if result.fetchone():
                print("✓ last_name column already exists")
                return
            
            # Add last_name column
            db.session.execute(text("""
                ALTER TABLE "user" 
                ADD COLUMN last_name VARCHAR(64)
            """))
            
            db.session.commit()
            print("✓ Successfully added last_name column")
            
        except Exception as e:
            print(f"✗ Error during migration: {e}")
            db.session.rollback()
            raise

if __name__ == '__main__':
    print("\n🔄 Starting Telegram last_name migration...\n")
    migrate_telegram_lastname()
    print("\n✅ Telegram last_name migration completed successfully!\n")
