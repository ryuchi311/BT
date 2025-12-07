from app import create_app, db
from models import User
from sqlalchemy import text

app = create_app()

with app.app_context():
    try:
        # Print the database URI being used (masking password)
        uri = app.config['SQLALCHEMY_DATABASE_URI']
        print(f"Connecting to database: {uri.split('@')[-1] if '@' in uri else uri}")
        
        # Try a simple query
        result = db.session.execute(text('SELECT 1')).scalar()
        print(f"Connection test successful: {result}")
        
        # Check for users
        user_count = User.query.count()
        print(f"User count: {user_count}")
        
        # List first 5 users to verify data
        users = User.query.limit(5).all()
        for u in users:
            print(f"User: {u.username} (ID: {u.id})")
            
    except Exception as e:
        print(f"Error connecting to database: {e}")
