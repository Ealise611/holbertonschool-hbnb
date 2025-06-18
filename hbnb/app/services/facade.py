from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place


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
        self.user_repo.update(user_id, data)
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

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