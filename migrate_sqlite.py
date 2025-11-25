"""
SQLite Database Migration Script
Adds missing columns to Quest table for SQLite database
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
        print("Starting SQLite database migration...")
        
        try:
            with db.engine.begin() as conn:
                # Check and add category column
                if not column_exists('quest', 'category'):
                    conn.execute(text("ALTER TABLE quest ADD COLUMN category VARCHAR(64)"))
                    print("✓ Added 'category' column")
                else:
                    print("  'category' column already exists")
                
                # Check and add expires_at column
                if not column_exists('quest', 'expires_at'):
                    conn.execute(text("ALTER TABLE quest ADD COLUMN expires_at TIMESTAMP"))
                    print("✓ Added 'expires_at' column")
                else:
                    print("  'expires_at' column already exists")
                
                # Check and add is_active column
                if not column_exists('quest', 'is_active'):
                    conn.execute(text("ALTER TABLE quest ADD COLUMN is_active BOOLEAN DEFAULT 1"))
                    print("✓ Added 'is_active' column")
                else:
                    print("  'is_active' column already exists")
                
                # Check and add platform_config column
                if not column_exists('quest', 'platform_config'):
                    conn.execute(text("ALTER TABLE quest ADD COLUMN platform_config JSON"))
                    print("✓ Added 'platform_config' column")
                else:
                    print("  'platform_config' column already exists")
                
                # Check and add verification_type column
                if not column_exists('quest', 'verification_type'):
                    conn.execute(text("ALTER TABLE quest ADD COLUMN verification_type VARCHAR(50) DEFAULT 'auto'"))
                    print("✓ Added 'verification_type' column")
                else:
                    print("  'verification_type' column already exists")
                
                # Check and add verification_instructions column
                if not column_exists('quest', 'verification_instructions'):
                    conn.execute(text("ALTER TABLE quest ADD COLUMN verification_instructions TEXT"))
                    print("✓ Added 'verification_instructions' column")
                else:
                    print("  'verification_instructions' column already exists")
                
                # Create SystemSetting table if it doesn't exist
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS system_setting (
                        key VARCHAR(128) PRIMARY KEY,
                        value TEXT,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """))
                print("✓ Ensured 'system_setting' table exists")
                
                print("\n--- Migrating Reward table ---")
                
                # Check and add stock column to reward
                if not column_exists('reward', 'stock'):
                    conn.execute(text("ALTER TABLE reward ADD COLUMN stock INTEGER"))
                    print("✓ Added 'stock' column to reward")
                else:
                    print("  'stock' column already exists in reward")
                
                # Check and add category column to reward
                if not column_exists('reward', 'category'):
                    conn.execute(text("ALTER TABLE reward ADD COLUMN category VARCHAR(64)"))
                    print("✓ Added 'category' column to reward")
                else:
                    print("  'category' column already exists in reward")
                
                # Check and add is_active column to reward
                if not column_exists('reward', 'is_active'):
                    conn.execute(text("ALTER TABLE reward ADD COLUMN is_active BOOLEAN DEFAULT 1"))
                    print("✓ Added 'is_active' column to reward")
                else:
                    print("  'is_active' column already exists in reward")
                
                # Check and add created_at column to reward
                if not column_exists('reward', 'created_at'):
                    conn.execute(text("ALTER TABLE reward ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP"))
                    print("✓ Added 'created_at' column to reward")
                else:
                    print("  'created_at' column already exists in reward")
                
                print("\n--- Migrating User table ---")
                
                # Check and add email column to user
                if not column_exists('user', 'email'):
                    conn.execute(text("ALTER TABLE user ADD COLUMN email VARCHAR(128)"))
                    print("✓ Added 'email' column to user")
                else:
                    print("  'email' column already exists in user")
                
                # Check and add is_onboarded column to user
                if not column_exists('user', 'is_onboarded'):
                    conn.execute(text("ALTER TABLE user ADD COLUMN is_onboarded BOOLEAN DEFAULT 0"))
                    print("✓ Added 'is_onboarded' column to user")
                else:
                    print("  'is_onboarded' column already exists in user")
                
                # Check and add terms_accepted column to user
                if not column_exists('user', 'terms_accepted'):
                    conn.execute(text("ALTER TABLE user ADD COLUMN terms_accepted BOOLEAN DEFAULT 0"))
                    print("✓ Added 'terms_accepted' column to user")
                else:
                    print("  'terms_accepted' column already exists in user")
                
                # Check and add terms_accepted_at column to user
                if not column_exists('user', 'terms_accepted_at'):
                    conn.execute(text("ALTER TABLE user ADD COLUMN terms_accepted_at TIMESTAMP"))
                    print("✓ Added 'terms_accepted_at' column to user")
                else:
                    print("  'terms_accepted_at' column already exists in user")

                print("\n--- Migrating UserQuest table ---")
                
                # Check and add proof_data column to user_quest
                if not column_exists('user_quest', 'proof_data'):
                    conn.execute(text("ALTER TABLE user_quest ADD COLUMN proof_data JSON"))
                    print("✓ Added 'proof_data' column to user_quest")
                else:
                    print("  'proof_data' column already exists in user_quest")
                
                # Check and add verification_status column to user_quest
                if not column_exists('user_quest', 'verification_status'):
                    conn.execute(text("ALTER TABLE user_quest ADD COLUMN verification_status VARCHAR(20) DEFAULT 'pending'"))
                    print("✓ Added 'verification_status' column to user_quest")
                else:
                    print("  'verification_status' column already exists in user_quest")
                
                # Check and add admin_notes column to user_quest
                if not column_exists('user_quest', 'admin_notes'):
                    conn.execute(text("ALTER TABLE user_quest ADD COLUMN admin_notes TEXT"))
                    print("✓ Added 'admin_notes' column to user_quest")
                else:
                    print("  'admin_notes' column already exists in user_quest")

                # Check and add admin_notes column to user_quest
                if not column_exists('user_quest', 'admin_notes'):
                    conn.execute(text("ALTER TABLE user_quest ADD COLUMN admin_notes TEXT"))
                    print("✓ Added 'admin_notes' column to user_quest")
                else:
                    print("  'admin_notes' column already exists in user_quest")

                # Check and add submission_text column to user_quest
                if not column_exists('user_quest', 'submission_text'):
                    conn.execute(text("ALTER TABLE user_quest ADD COLUMN submission_text TEXT"))
                    print("✓ Added 'submission_text' column to user_quest")
                else:
                    print("  'submission_text' column already exists in user_quest")

                # Check and add submission_link column to user_quest
                if not column_exists('user_quest', 'submission_link'):
                    conn.execute(text("ALTER TABLE user_quest ADD COLUMN submission_link VARCHAR(512)"))
                    print("✓ Added 'submission_link' column to user_quest")
                else:
                    print("  'submission_link' column already exists in user_quest")

                # Check and add submitted_at column to user_quest
                if not column_exists('user_quest', 'submitted_at'):
                    conn.execute(text("ALTER TABLE user_quest ADD COLUMN submitted_at TIMESTAMP"))
                    print("✓ Added 'submitted_at' column to user_quest")
                else:
                    print("  'submitted_at' column already exists in user_quest")

                # Check and add reviewed_by column to user_quest
                if not column_exists('user_quest', 'reviewed_by'):
                    conn.execute(text("ALTER TABLE user_quest ADD COLUMN reviewed_by INTEGER REFERENCES user(id)"))
                    print("✓ Added 'reviewed_by' column to user_quest")
                else:
                    print("  'reviewed_by' column already exists in user_quest")

                # Check and add reviewed_at column to user_quest
                if not column_exists('user_quest', 'reviewed_at'):
                    conn.execute(text("ALTER TABLE user_quest ADD COLUMN reviewed_at TIMESTAMP"))
                    print("✓ Added 'reviewed_at' column to user_quest")
                else:
                    print("  'reviewed_at' column already exists in user_quest")

                print("\n--- Creating missing tables ---")
                
                # Create UserReward table
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS user_reward (
                        id INTEGER PRIMARY KEY,
                        user_id INTEGER NOT NULL,
                        reward_id INTEGER NOT NULL,
                        claimed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        status VARCHAR(20) DEFAULT 'pending',
                        delivery_info TEXT,
                        FOREIGN KEY(user_id) REFERENCES user(id),
                        FOREIGN KEY(reward_id) REFERENCES reward(id)
                    )
                """))
                print("✓ Ensured 'user_reward' table exists")

                # Create DailyCheckIn table
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS daily_check_in (
                        id INTEGER PRIMARY KEY,
                        user_id INTEGER NOT NULL,
                        quest_id INTEGER NOT NULL,
                        check_in_date DATE NOT NULL,
                        streak_count INTEGER DEFAULT 1,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY(user_id) REFERENCES user(id),
                        FOREIGN KEY(quest_id) REFERENCES quest(id),
                        UNIQUE(user_id, quest_id, check_in_date)
                    )
                """))
                print("✓ Ensured 'daily_check_in' table exists")
            
            print("\n✅ Database migration completed successfully!")
            print("You can now restart your Flask application.")
            
        except Exception as e:
            print(f"\n❌ Migration failed: {str(e)}")
            raise

if __name__ == '__main__':
    migrate_database()
