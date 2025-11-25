"""
Migration script to add verification queue fields to UserQuest table
Run this script to update the database schema
"""
import os
from dotenv import load_dotenv
import psycopg2
from psycopg2 import sql

# Load environment variables
load_dotenv()

def run_migration():
    # Get database URL from environment
    database_url = os.getenv('SQLALCHEMY_DATABASE_URI')
    
    if not database_url:
        print("Error: SQLALCHEMY_DATABASE_URI not found in environment variables")
        return
    
    print("Connecting to database...")
    
    try:
        # Connect to PostgreSQL
        conn = psycopg2.connect(database_url)
        cur = conn.cursor()
        
        print("Adding new columns to user_quest table...")
        
        # Add submission_text column
        try:
            cur.execute("""
                ALTER TABLE user_quest 
                ADD COLUMN IF NOT EXISTS submission_text TEXT;
            """)
            print("✓ Added submission_text column")
        except Exception as e:
            print(f"Note: submission_text column may already exist: {e}")
        
        # Add submission_link column
        try:
            cur.execute("""
                ALTER TABLE user_quest 
                ADD COLUMN IF NOT EXISTS submission_link VARCHAR(512);
            """)
            print("✓ Added submission_link column")
        except Exception as e:
            print(f"Note: submission_link column may already exist: {e}")
        
        # Add submitted_at column
        try:
            cur.execute("""
                ALTER TABLE user_quest 
                ADD COLUMN IF NOT EXISTS submitted_at TIMESTAMP;
            """)
            print("✓ Added submitted_at column")
        except Exception as e:
            print(f"Note: submitted_at column may already exist: {e}")
        
        # Add reviewed_by column
        try:
            cur.execute("""
                ALTER TABLE user_quest 
                ADD COLUMN IF NOT EXISTS reviewed_by INTEGER REFERENCES "user"(id);
            """)
            print("✓ Added reviewed_by column")
        except Exception as e:
            print(f"Note: reviewed_by column may already exist: {e}")
        
        # Add reviewed_at column
        try:
            cur.execute("""
                ALTER TABLE user_quest 
                ADD COLUMN IF NOT EXISTS reviewed_at TIMESTAMP;
            """)
            print("✓ Added reviewed_at column")
        except Exception as e:
            print(f"Note: reviewed_at column may already exist: {e}")
        
        # Commit changes
        conn.commit()
        print("\n✅ Migration completed successfully!")
        
        # Close connection
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        if conn:
            conn.rollback()

if __name__ == '__main__':
    print("=" * 50)
    print("UserQuest Verification Queue Migration")
    print("=" * 50)
    run_migration()
