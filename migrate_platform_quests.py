from app import create_app
from models import db
from sqlalchemy import text

app = create_app()

with app.app_context():
    print("Adding new columns to Quest and UserQuest tables...")
    
    # Add columns to Quest table
    try:
        db.session.execute(text("""
            ALTER TABLE quest 
            ADD COLUMN platform_config JSON
        """))
        print("✓ Added platform_config to Quest")
    except Exception as e:
        print(f"platform_config might already exist: {e}")
    
    try:
        db.session.execute(text("""
            ALTER TABLE quest 
            ADD COLUMN verification_type VARCHAR(50) DEFAULT 'auto'
        """))
        print("✓ Added verification_type to Quest")
    except Exception as e:
        print(f"verification_type might already exist: {e}")
    
    try:
        db.session.execute(text("""
            ALTER TABLE quest 
            ADD COLUMN verification_instructions TEXT
        """))
        print("✓ Added verification_instructions to Quest")
    except Exception as e:
        print(f"verification_instructions might already exist: {e}")
    
    # Add columns to UserQuest table
    try:
        db.session.execute(text("""
            ALTER TABLE user_quest 
            ADD COLUMN proof_data JSON
        """))
        print("✓ Added proof_data to UserQuest")
    except Exception as e:
        print(f"proof_data might already exist: {e}")
    
    try:
        db.session.execute(text("""
            ALTER TABLE user_quest 
            ADD COLUMN verification_status VARCHAR(20) DEFAULT 'pending'
        """))
        print("✓ Added verification_status to UserQuest")
    except Exception as e:
        print(f"verification_status might already exist: {e}")
    
    try:
        db.session.execute(text("""
            ALTER TABLE user_quest 
            ADD COLUMN admin_notes TEXT
        """))
        print("✓ Added admin_notes to UserQuest")
    except Exception as e:
        print(f"admin_notes might already exist: {e}")
    
    db.session.commit()
    print("\n✅ Migration completed successfully!")
