import os
import sys
from sqlalchemy import text

# Add the current directory to the path so we can import our modules
sys.path.append(os.getcwd())

from core.database import engine, Base, get_db
from models import Location

def update_database_schema():
    print("Starting database schema update...")
    
    # Drop and recreate tables (in development only)
    # In production, you should use proper migrations with Alembic
    print("Recreating database tables...")
    
    try:
        # Drop existing tables
        Base.metadata.drop_all(bind=engine)
        
        # Create tables with new schema
        Base.metadata.create_all(bind=engine)
        
        print("Database schema updated successfully!")
    except Exception as e:
        print(f"Error updating database schema: {e}")
        return False
    
    return True

if __name__ == "__main__":
    # Run the schema update
    update_database_schema()