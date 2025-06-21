from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review

from app.validation.user_validation import validate_user_data
from app.validation.place_validation import validate_place_data
from app.validation.review_validation import validate_review_data
from app.validation.amenity_validation import validate_amenity_data


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # USER FACADE
    def create_user(self, user_data):
        validate_user_data(user_data)
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def update_user(self, user_id, data):
        user = self.get_user(user_id)
        if not user:
            return None  # User not found
        self.user_repo.update(user_id, data)
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        if not email or not email.strip():
            return None

        all_users = self.user_repo.get_all()
        for user in all_users:
            if user.email.lower() == email.strip().lower():
                return user

        return None

    def get_all_users(self):
        return self.user_repo.get_all()

    # AMENITY FACADE
    def create_amenity(self, amenity_data):
        validate_amenity_data(amenity_data)
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        self.amenity_repo.update(amenity_id, amenity_data)
        return self.amenity_repo.get(amenity_id)

    # PLACE FACADE
    def create_place(self, place_data):
        validate_place_data(place_data)

        owner = self.get_user(place_data['owner_id'])
        if not owner:
            raise ValueError("Owner not found")

        amenities = []
        if 'amenities' in place_data and place_data['amenities']:
            for amenity_id in place_data['amenities']:
                amenity = self.get_amenity(amenity_id)
                if amenity:
                    amenities.append(amenity)

        place_creation_data = {
            'title': place_data['title'],
            'description': place_data.get('description', ''),
            'price': place_data['price'],
            'latitude': place_data['latitude'],
            'longitude': place_data['longitude'],
            'owner': owner
        }

        place = Place(**place_creation_data)

        for amenity in amenities:
            place.add_amenity(amenity)

        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.get_place(place_id)
        if not place:
            return None

        if 'owner_id' in place_data:
            owner = self.get_user(place_data['owner_id'])
            if not owner:
                raise ValueError("Owner not found")
            place_data['owner'] = owner
            del place_data['owner_id']

        if 'amenities' in place_data:
            new_amenities = []
            if place_data['amenities']:
                for amenity_id in place_data['amenities']:
                    amenity = self.get_amenity(amenity_id)
                    if amenity:
                        new_amenities.append(amenity)
            place.amenities = new_amenities
            del place_data['amenities']

        self.place_repo.update(place_id, place_data)
        return self.place_repo.get(place_id)

    # REVIEW FACADE
    def create_review(self, review_data):
        validate_review_data(review_data)

        user = self.get_user(review_data['user_id'])
        if not user:
            raise ValueError("User not found")

        place = self.get_place(review_data['place_id'])
        if not place:
            raise ValueError("Place not found")

        existing_review = self.get_review_by_user_and_place(review_data['user_id'], review_data['place_id'])
        if existing_review:
            raise ValueError("User has already reviewed this place")

        review = Review(
            text=review_data['text'],
            rating=review_data['rating'],
            place=place,
            user=user
        )

        place.add_review(review)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        reviews = []
        for review in self.review_repo.get_all():
            if review.place.id == place_id:
                reviews.append(review)
        return reviews

    def get_review_by_user_and_place(self, user_id, place_id):
        for review in self.review_repo.get_all():
            if review.user.id == user_id and review.place.id == place_id:
                return review
        return None

    def update_review(self, review_id, review_data):
        review = self.get_review(review_id)
        if not review:
            return None

        allowed_fields = ['text', 'rating']
        filtered_data = {k: v for k, v in review_data.items() if k in allowed_fields}

        self.review_repo.update(review_id, filtered_data)
        return self.review_repo.get(review_id)

    def delete_review(self, review_id):
        review = self.get_review(review_id)
        if not review:
            return False

        if review.place and hasattr(review.place, 'reviews'):
            if review in review.place.reviews:
                review.place.reviews.remove(review)

        self.review_repo.delete(review_id)
        return True
