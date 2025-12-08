
from app import create_app
from models import db
from sqlalchemy import text, inspect

app = create_app()
with app.app_context():
    conn = db.engine.connect()
    inspector = inspect(db.engine)
    
    tables = inspector.get_table_names()
    
    for table_name in tables:
        fks = inspector.get_foreign_keys(table_name)
        for fk in fks:
            if fk['referred_table'] == 'users':
                print(f"Fixing FK {fk['name']} on table {table_name}...")
                
                # Drop
                try:
                    conn.execute(text(f"ALTER TABLE {table_name} DROP CONSTRAINT {fk['name']}"))
                    print(f"  Dropped {fk['name']}")
                except Exception as e:
                    print(f"  Error dropping {fk['name']}: {e}")
                    continue
                
                # Add new
                # constrained_columns is a list, usually length 1
                col = fk['constrained_columns'][0]
                new_fk_name = fk['name'] # Keep same name? Or usually names are auto-generated.
                # If we keep same name, it's fine.
                
                try:
                    sql = f"ALTER TABLE {table_name} ADD CONSTRAINT {new_fk_name} FOREIGN KEY ({col}) REFERENCES \"user\" (id)"
                    conn.execute(text(sql))
                    print(f"  Added new constraint {new_fk_name} referencing 'user'.")
                except Exception as e:
                    print(f"  Error adding {new_fk_name}: {e}")
                    # Try to restore?
                    
    conn.commit()
    print("All fixes applied.")
