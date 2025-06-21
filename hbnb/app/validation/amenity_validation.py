# app/validation/amenity_validation.py

def validate_amenity_data(data):
    if 'name' not in data or not isinstance(data['name'], str) or not data['name'].strip():
        raise ValueError("Amenity name is required and must be a non-empty string")
