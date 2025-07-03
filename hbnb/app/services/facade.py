from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # USER FACADE
    def create_user(self, user_data):
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
        """Get user by email (case-insensitive)"""
        if not email or not email.strip():
            return None
        
        # Search through all users manually
        all_users = self.user_repo.get_all()
        for user in all_users:
            if user.email.lower() == email.strip().lower():
                return user
        
        return None

    def get_all_users(self):
        return self.user_repo.get_all()

    # AMENITY FACADE
    def create_amenity(self, amenity_data):
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
        '''Create a new place with validation and add amenities'''
        # Get  the owner
        owner = self.get_user(place_data['owner_id'])
        if not owner:
            raise ValueError("Owner not found")

        # Process amenities if provided
        amenities = []
        if 'amenities' in place_data and place_data['amenities']:
            for amenity_id in place_data['amenities']:
                amenity = self.get_amenity(amenity_id)
                if amenity:
                    amenities.append(amenity)

        # Create place data without amenities list for constructor
        place_creation_data = {
            'title': place_data['title'],
            'description': place_data.get('description', ''),
            'price': place_data['price'],
            'latitude': place_data['latitude'],
            'longitude': place_data['longitude'],
            'owner': owner
        }

        place = Place(**place_creation_data)

        # Add amenities to place
        for amenity in amenities:
            place.add_amenity(amenity)

        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        """Retrieve a place by ID with associated owner and amenities"""
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """Retrieve all places"""
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """Update a place's information"""
        place = self.get_place(place_id)
        if not place:
            return None

        # Handle owner change if provided
        if 'owner_id' in place_data:
            owner = self.get_user(place_data['owner_id'])
            if not owner:
                raise ValueError("Owner not found")
            place_data['owner'] = owner
            del place_data['owner_id']

        # Handle amenities update if provided
        if 'amenities' in place_data:
            new_amenities = []
            if place_data['amenities']:  # Check if amenities list is not empty
                for amenity_id in place_data['amenities']:
                    amenity = self.get_amenity(amenity_id)
                    if amenity:
                        new_amenities.append(amenity)
            place.amenities = new_amenities
            del place_data['amenities']
        
        # Update othe fields
        self.place_repo.update(place_id, place_data)
        return self.place_repo.get(place_id)
    
    # REVIEW FACADE
    def create_review(self, review_data):
        """Create a new review with validation"""

        # Get the user who is writing the review
        user = self.get_user(review_data['user_id'])
        if not user:
            raise ValueError("User not found")

        # Get the place being reviewed
        place = self.get_place(review_data['place_id'])
        if not place:
            raise ValueError("Place not found")
        
        # check if own place
        if place.owner.id == review_data['user_id']:
            raise ValueError("You cannot review your own place")

        # Check if user has already reviewed this place
        existing_review = self.get_review_by_user_and_place(
            review_data['user_id'],
            review_data['place_id']
            )
        if existing_review:
            raise ValueError("User has already reviewed this place")

        # Create review using your model's constructor signature (text, rating, place, user)
        review = Review(
            text=review_data['text'],
            rating=review_data['rating'],
            place=place,
            user=user
        )
        
        # Add review to place's reviews list
        place.add_review(review)
        
        # Store the review
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        """Retrieve a review by ID"""
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """Retrieve all reviews"""
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        """Get all reviews for a specific place"""
        reviews = []
        for review in self.review_repo.get_all():
            if review.place.id == place_id:
                reviews.append(review)
        return reviews

    def get_review_by_user_and_place(self, user_id, place_id):
        """Check if a user has already reviewed a place"""
        for review in self.review_repo.get_all():
            if review.user.id == user_id and review.place.id == place_id:
                return review
        return None

    def update_review(self, review_id, review_data):
        """Update a review's information"""
        review = self.get_review(review_id)
        if not review:
            return None

        # Only allow updating text and rating, not user or place
        allowed_fields = ['text', 'rating']
        filtered_data = {k: v for k, v in review_data.items() if k in allowed_fields}
        
        self.review_repo.update(review_id, filtered_data)
        return self.review_repo.get(review_id)

    def delete_review(self, review_id):
        """Delete a review"""
        review = self.get_review(review_id)
        if not review:
            return False

        # Remove review from place's reviews list
        if review.place and hasattr(review.place, 'reviews'):
            if review in review.place.reviews:
                review.place.reviews.remove(review)

        # Delete from repository
        self.review_repo.delete(review_id)
        return True