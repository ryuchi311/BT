"""
PostgreSQL Database Migration Script
Adds new columns to Quest table and creates SystemSetting table
"""

from app import app, db
from sqlalchemy import text

def migrate_database():
    with app.app_context():
        print("Starting PostgreSQL database migration...")
        
        try:
            with db.engine.begin() as conn:
                # Add category column
                try:
                    conn.execute(text("ALTER TABLE quest ADD COLUMN IF NOT EXISTS category VARCHAR(64)"))
                    print("✓ Added 'category' column")
                except Exception as e:
                    print(f"  Category column: {str(e)}")
                
                # Add expires_at column
                try:
                    conn.execute(text("ALTER TABLE quest ADD COLUMN IF NOT EXISTS expires_at TIMESTAMP"))
                    print("✓ Added 'expires_at' column")
                except Exception as e:
                    print(f"  Expires_at column: {str(e)}")
                
                # Add is_active column with default
                try:
                    conn.execute(text("ALTER TABLE quest ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT TRUE"))
                    print("✓ Added 'is_active' column")
                except Exception as e:
                    print(f"  Is_active column: {str(e)}")
                
                # Create SystemSetting table
                try:
                    conn.execute(text("""
                        CREATE TABLE IF NOT EXISTS system_setting (
                            key VARCHAR(128) PRIMARY KEY,
                            value TEXT,
                            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        )
                    """))
                    print("✓ Created 'system_setting' table")
                except Exception as e:
                    print(f"  SystemSetting table: {str(e)}")
            
            print("\n✅ Database migration completed successfully!")
            print("Your admin dashboard should now work properly.")
            
        except Exception as e:
            print(f"\n❌ Migration failed: {str(e)}")
            raise

if __name__ == '__main__':
    migrate_database()
