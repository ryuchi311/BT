from app import create_app
from models import db
from sqlalchemy import text

app = create_app()

with app.app_context():
    print("Adding onboarding fields to User table...")
    
    try:
        db.session.execute(text("""
            ALTER TABLE "user" 
            ADD COLUMN email VARCHAR(128)
        """))
        print("✓ Added email to User")
    except Exception as e:
        print(f"email might already exist: {e}")
    
    try:
        db.session.execute(text("""
            ALTER TABLE "user" 
            ADD COLUMN is_onboarded BOOLEAN DEFAULT FALSE
        """))
        print("✓ Added is_onboarded to User")
    except Exception as e:
        print(f"is_onboarded might already exist: {e}")
    
    try:
        db.session.execute(text("""
            ALTER TABLE "user" 
            ADD COLUMN terms_accepted BOOLEAN DEFAULT FALSE
        """))
        print("✓ Added terms_accepted to User")
    except Exception as e:
        print(f"terms_accepted might already exist: {e}")
    
    try:
        db.session.execute(text("""
            ALTER TABLE "user" 
            ADD COLUMN terms_accepted_at TIMESTAMP
        """))
        print("✓ Added terms_accepted_at to User")
    except Exception as e:
        print(f"terms_accepted_at might already exist: {e}")
    
    db.session.commit()
    print("\n✅ Onboarding migration completed successfully!")
