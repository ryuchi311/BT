"""
Migration script to add new columns to the existing Reward table
"""
from app import app, db
from sqlalchemy import text

with app.app_context():
    # Add new columns to reward table
    with db.engine.connect() as conn:
        try:
            # Add stock column
            conn.execute(text('ALTER TABLE reward ADD COLUMN IF NOT EXISTS stock INTEGER'))
            print("✅ Added 'stock' column")
        except Exception as e:
            print(f"⚠️  stock column: {e}")
        
        try:
            # Add is_active column
            conn.execute(text('ALTER TABLE reward ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT TRUE'))
            print("✅ Added 'is_active' column")
        except Exception as e:
            print(f"⚠️  is_active column: {e}")
        
        try:
            # Add category column
            conn.execute(text('ALTER TABLE reward ADD COLUMN IF NOT EXISTS category VARCHAR(64)'))
            print("✅ Added 'category' column")
        except Exception as e:
            print(f"⚠️  category column: {e}")
        
        try:
            # Add created_at column
            conn.execute(text('ALTER TABLE reward ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP'))
            print("✅ Added 'created_at' column")
        except Exception as e:
            print(f"⚠️  created_at column: {e}")
        
        conn.commit()
    
    print("\n✅ Reward table migration complete!")
    print("Please restart your Flask app for changes to take effect.")
