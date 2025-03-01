#!/usr/bin/env python3

import os
import re

def fix_file(file_path, replacements):
    with open(file_path, 'r') as file:
        content = file.read()
    
    for old, new in replacements:
        content = content.replace(old, new)
    
    with open(file_path, 'w') as file:
        file.write(content)
    
    print(f"Fixed imports in {file_path}")

# Fix models/__init__.py
models_init_path = 'models/__init__.py'
if os.path.exists(models_init_path):
    fix_file(models_init_path, [
        ('from models.location import Location', 'from .location import Location')
    ])

# Fix models/location.py
location_model_path = 'models/location.py'
if os.path.exists(location_model_path):
    fix_file(location_model_path, [
        ('from api.core.database import Base', 'from core.database import Base')
    ])

# Fix main.py
main_py_path = 'main.py'
if os.path.exists(main_py_path):
    fix_file(main_py_path, [
        ('from api.locations import router as locations_router', 'from api.locations import router as locations_router'),
        ('from api.weather import router as weather_router', 'from api.weather import router as weather_router')
    ])

print("Import fixes completed. Please restart your application.")