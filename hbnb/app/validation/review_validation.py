# app/validation/review_validation.py

def validate_review_data(data):
    required_fields = ['text', 'rating', 'user_id', 'place_id']

    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing required field: {field}")

    if not isinstance(data['text'], str) or not data['text'].strip():
        raise ValueError("Review text must be a non-empty string")

    if not isinstance(data['rating'], int) or not (1 <= data['rating'] <= 5):
        raise ValueError("Rating must be an integer between 1 and 5")

    if not isinstance(data['user_id'], str) or not data['user_id'].strip():
        raise ValueError("user_id must be a non-empty string")

    if not isinstance(data['place_id'], str) or not data['place_id'].strip():
        raise ValueError("place_id must be a non-empty string")
