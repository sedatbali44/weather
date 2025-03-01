#!/usr/bin/env python3

import os
import sys

def clean_models():
    print("Cleaning up model definitions...")
    
    # Remove conflicting models.py file
    if os.path.exists('models.py'):
        print("Removing conflicting models.py file...")
        os.rename('models.py', 'models.py.bak')
        print("Renamed models.py to models.py.bak")
    
    # Fix models/location.py if needed
    location_model_path = 'models/location.py'
    if os.path.exists(location_model_path):
        print("Checking location model...")
        with open(location_model_path, 'r') as file:
            content = file.read()
        
        # Make sure we're using the correct imports
        updated_content = content.replace(
            'from api.core.database import Base', 
            'from core.database import Base'
        )
        
        with open(location_model_path, 'w') as file:
            file.write(updated_content)
        
        print("Updated location model imports if needed")
    
    # Fix models/__init__.py if needed
    models_init_path = 'models/__init__.py'
    if os.path.exists(models_init_path):
        print("Checking models __init__.py...")
        with open(models_init_path, 'r') as file:
            content = file.read()
        
        # Make sure we're using the correct relative imports
        updated_content = content.replace(
            'from models.location import Location', 
            'from .location import Location'
        )
        
        with open(models_init_path, 'w') as file:
            file.write(updated_content)
        
        print("Updated models/__init__.py imports if needed")
    
    print("Model cleanup completed!")

if __name__ == "__main__":
    clean_models()