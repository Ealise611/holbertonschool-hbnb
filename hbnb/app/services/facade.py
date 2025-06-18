from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # Placeholder method for creating a user
    def create_user(self, user_data):
        # Logic will be implemented in later tasks
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def update_user(self, user_id, data):
        self.user_repo.update(user_id, data)
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        return self.user_repo.get_all()

    # Placeholder method for fetching a place by ID
    def get_place(self, place_id):
        # Logic will be implemented in later tasks
        pass

    def create_amenity(self, amenity_data):
        # Placeholder for logic to create an amenity
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        # Placeholder for logic to retrieve an amenity by ID
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        # Placeholder for logic to retrieve all amenities
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        # Placeholder for logic to update an amenity
        self.amenity_repo.update(amenity_id, amenity_data)
        return self.amenity_repo.get(amenity_id)