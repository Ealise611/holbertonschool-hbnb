# app/validation/place_validation.py

def validate_place_data(data):
    required_fields = ['title', 'price', 'latitude', 'longitude', 'owner_id']

    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing required field: {field}")

    if not isinstance(data['title'], str) or not data['title'].strip():
        raise ValueError("Title must be a non-empty string")

    if not isinstance(data['price'], (int, float)):
        raise ValueError("Price must be a number")
    if data['price'] < 0:
        raise ValueError("Price must be non-negative")

    if not isinstance(data['latitude'], (int, float)) or not -90 <= data['latitude'] <= 90:
        raise ValueError("Latitude must be between -90 and 90")

    if not isinstance(data['longitude'], (int, float)) or not -180 <= data['longitude'] <= 180:
        raise ValueError("Longitude must be between -180 and 180")

    if 'amenities' in data:
        if not isinstance(data['amenities'], list):
            raise ValueError("Amenities must be a list of amenity IDs")
        for amenity_id in data['amenities']:
            if not isinstance(amenity_id, str) or not amenity_id.strip():
                raise ValueError("Each amenity ID must be a non-empty string")
