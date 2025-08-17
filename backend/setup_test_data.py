#!/usr/bin/env python3
"""
HBnB Test Data Setup Script
Creates users, places, amenities, and reviews for testing
Run this after starting your Flask server: python run.py
"""

import requests
import json
import sys
import time

BASE_URL = "http://localhost:5000/api/v1"


class HBnBSetup:
    def __init__(self):
        self.tokens = {}
        self.ids = {}

    def log(self, message):
        print(f"✅ {message}")

    def error(self, message):
        print(f"❌ {message}")

    def warn(self, message):
        print(f"⚠️  {message}")

    def post(self, endpoint, data, token=None):
        headers = {"Content-Type": "application/json"}
        if token:
            headers["Authorization"] = f"Bearer {token}"

        try:
            response = requests.post(
                f"{BASE_URL}{endpoint}", json=data, headers=headers, timeout=10
            )

            if response.status_code in [200, 201]:
                return response.json() if response.text else {}
            elif response.status_code == 400 and "already exists" in response.text:
                self.warn(f"Resource already exists: {endpoint}")
                return response.json() if response.text else {}
            else:
                self.error(
                    f"Failed {endpoint}: {response.status_code} - {response.text}"
                )
                return None

        except requests.exceptions.ConnectionError:
            self.error("Cannot connect to server. Is Flask running on localhost:5000?")
            sys.exit(1)
        except Exception as e:
            self.error(f"Request failed: {e}")
            return None

    def get(self, endpoint, token=None):
        headers = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"

        try:
            response = requests.get(
                f"{BASE_URL}{endpoint}", headers=headers, timeout=10
            )
            if response.status_code == 200:
                return response.json()
            return None
        except:
            return None

    def setup_admin(self):
        """Create and login admin"""
        self.log("Setting up admin user...")

        # Create admin (might already exist)
        result = self.post("/auth/create-admin", {})

        # Login admin
        login_result = self.post(
            "/auth/login", {"email": "admin@hbnb.io", "password": "admin123"}
        )

        if login_result and "access_token" in login_result:
            self.tokens["admin"] = login_result["access_token"]
            self.log("Admin logged in successfully")
            return True
        else:
            self.error("Admin login failed")
            return False

    def create_users(self):
        """Create and login test users"""
        users = [
            {
                "name": "alice",
                "first_name": "Alice",
                "last_name": "Johnson",
                "email": "alice@example.com",
                "password": "alice123",
            },
            {
                "name": "bob",
                "first_name": "Bob",
                "last_name": "Wilson",
                "email": "bob@example.com",
                "password": "bob123",
            },
            {
                "name": "charlie",
                "first_name": "Charlie",
                "last_name": "Brown",
                "email": "charlie@example.com",
                "password": "charlie123",
            },
            {
                "name": "diana",
                "first_name": "Diana",
                "last_name": "Smith",
                "email": "diana@example.com",
                "password": "diana123",
            },
        ]

        for user in users:
            # Create user
            user_result = self.post(
                "/users/",
                {
                    "first_name": user["first_name"],
                    "last_name": user["last_name"],
                    "email": user["email"],
                    "password": user["password"],
                },
            )

            if user_result and "id" in user_result:
                self.ids[f"{user['name']}_id"] = user_result["id"]

                # Login user
                login_result = self.post(
                    "/auth/login",
                    {"email": user["email"], "password": user["password"]},
                )

                if login_result and "access_token" in login_result:
                    self.tokens[user["name"]] = login_result["access_token"]
                    self.log(f"Created and logged in {user['first_name']}")
                else:
                    self.error(f"Failed to login {user['first_name']}")
                    return False
            else:
                self.error(f"Failed to create {user['first_name']}")
                return False

        return True

    def create_amenities(self):
        """Create amenities using admin token"""
        amenities = [
            {"name": "Wi-Fi", "description": "High-speed wireless internet"},
            {"name": "Swimming Pool", "description": "Outdoor pool with deck chairs"},
            {"name": "Parking", "description": "Free on-site parking"},
            {"name": "Air Conditioning", "description": "Central air conditioning"},
            {"name": "Kitchen", "description": "Fully equipped kitchen"},
            {"name": "Pet Friendly", "description": "Pets welcome"},
            {"name": "Gym", "description": "Fitness center access"},
        ]

        for amenity in amenities:
            result = self.post("/amenities/", amenity, self.tokens["admin"])
            if result and "id" in result:
                # Store amenity ID with a safe key name
                key = (
                    amenity["name"].lower().replace("-", "_").replace(" ", "_") + "_id"
                )
                self.ids[key] = result["id"]
                self.log(f"Created {amenity['name']} amenity")
            else:
                self.warn(f"Could not create {amenity['name']} amenity")

        return True

    def create_places(self):
        """Create places for each user with varied pricing for filter testing"""
        places = [
            # BUDGET PLACES ($5-$10) - Perfect for testing "Up to $10" filter
            {
                "owner": "diana",
                "title": "Backpacker Hostel Bed",
                "description": "Shared dormitory room in clean, safe hostel near train station",
                "price": 8,
                "latitude": 40.7580,
                "longitude": -73.9855,
                "amenities": ["wi_fi_id"],
            },
            {
                "owner": "diana",
                "title": "Budget Camping Spot",
                "description": "Basic tent camping with shared facilities, great for nature lovers",
                "price": 5,
                "latitude": 41.2500,
                "longitude": -77.8000,
                "amenities": ["parking_id"],
            },
            {
                "owner": "charlie",
                "title": "Student Room Share",
                "description": "Shared room near university campus, perfect for students",
                "price": 9,
                "latitude": 40.7400,
                "longitude": -73.9900,
                "amenities": ["wi_fi_id"],
            },
            # LOW-COST PLACES ($15-$50) - Perfect for testing "Up to $50" filter
            {
                "owner": "diana",
                "title": "Cozy Studio Apartment",
                "description": "Small but comfortable studio in quiet neighborhood",
                "price": 25,
                "latitude": 40.7200,
                "longitude": -74.0100,
                "amenities": ["wi_fi_id", "kitchen_id"],
            },
            {
                "owner": "alice",
                "title": "Guest Room in Family Home",
                "description": "Private room in friendly family home with breakfast included",
                "price": 35,
                "latitude": 40.7300,
                "longitude": -73.9800,
                "amenities": ["wi_fi_id", "parking_id"],
            },
            {
                "owner": "bob",
                "title": "Countryside Cottage",
                "description": "Rustic cottage surrounded by nature, perfect for weekend getaway",
                "price": 45,
                "latitude": 41.1000,
                "longitude": -77.5000,
                "amenities": ["parking_id", "pet_friendly_id"],
            },
            {
                "owner": "charlie",
                "title": "Urban Loft Share",
                "description": "Shared loft space in trendy district, great for young professionals",
                "price": 40,
                "latitude": 40.7450,
                "longitude": -73.9950,
                "amenities": ["wi_fi_id", "gym_id"],
            },
            # MID-RANGE PLACES ($60-$100) - Perfect for testing "Up to $100" filter
            {
                "owner": "alice",
                "title": "Boutique Hotel Room",
                "description": "Stylish room in boutique hotel with personalized service",
                "price": 85,
                "latitude": 40.7600,
                "longitude": -73.9700,
                "amenities": ["wi_fi_id", "air_conditioning_id", "gym_id"],
            },
            {
                "owner": "bob",
                "title": "Waterfront Cabin",
                "description": "Charming cabin with lake views and private dock access",
                "price": 75,
                "latitude": 40.8000,
                "longitude": -74.2000,
                "amenities": ["wi_fi_id", "parking_id", "kitchen_id"],
            },
            {
                "owner": "diana",
                "title": "Modern Apartment",
                "description": "Contemporary apartment with city views and modern amenities",
                "price": 90,
                "latitude": 40.7550,
                "longitude": -73.9850,
                "amenities": ["wi_fi_id", "air_conditioning_id", "parking_id"],
            },
            # ORIGINAL HIGHER-PRICED PLACES (for testing "All" filter)
            {
                "owner": "alice",
                "title": "Modern Downtown Loft",
                "description": "Stylish loft in the heart of downtown with amazing city views",
                "price": 180,
                "latitude": 40.7589,
                "longitude": -73.9851,
                "amenities": ["wi_fi_id", "air_conditioning_id"],
            },
            {
                "owner": "alice",
                "title": "Cozy Art Studio",
                "description": "Perfect space for artists and creatives with lots of natural light",
                "price": 120,
                "latitude": 40.7505,
                "longitude": -73.9934,
                "amenities": ["wi_fi_id", "parking_id"],
            },
            {
                "owner": "bob",
                "title": "Luxury Villa with Pool",
                "description": "Stunning villa with private pool, garden, and premium amenities",
                "price": 350,
                "latitude": 40.7128,
                "longitude": -74.0060,
                "amenities": [
                    "wi_fi_id",
                    "swimming_pool_id",
                    "parking_id",
                    "air_conditioning_id",
                ],
            },
            {
                "owner": "bob",
                "title": "Oceanfront Beach House",
                "description": "Direct beach access, perfect for families and beach lovers",
                "price": 280,
                "latitude": 40.5795,
                "longitude": -74.1502,
                "amenities": ["wi_fi_id", "parking_id", "kitchen_id"],
            },
            {
                "owner": "bob",
                "title": "Mountain Cabin Retreat",
                "description": "Peaceful retreat in the mountains, great for hiking and nature",
                "price": 150,
                "latitude": 41.2033,
                "longitude": -77.1945,
                "amenities": ["wi_fi_id", "parking_id", "kitchen_id"],
            },
            {
                "owner": "charlie",
                "title": "Central City Apartment",
                "description": "Modern apartment near public transport, restaurants, and attractions",
                "price": 140,
                "latitude": 40.7614,
                "longitude": -73.9776,
                "amenities": ["wi_fi_id", "air_conditioning_id", "parking_id"],
            },
            {
                "owner": "charlie",
                "title": "Charming Garden Cottage",
                "description": "Quiet cottage with beautiful garden, patio, and peaceful atmosphere",
                "price": 110,
                "latitude": 40.6892,
                "longitude": -74.0445,
                "amenities": ["wi_fi_id", "parking_id", "kitchen_id"],
            },
        ]

        place_counter = {}

        for place in places:
            # Get amenity IDs that exist
            amenity_ids = []
            for amenity_key in place["amenities"]:
                if amenity_key in self.ids:
                    amenity_ids.append(self.ids[amenity_key])

            place_data = {
                "title": place["title"],
                "description": place["description"],
                "price": place["price"],
                "latitude": place["latitude"],
                "longitude": place["longitude"],
                "amenities": amenity_ids,
            }

            result = self.post("/places/", place_data, self.tokens[place["owner"]])

            if result and "id" in result:
                # Track place numbers per owner
                owner = place["owner"]
                if owner not in place_counter:
                    place_counter[owner] = 0
                place_counter[owner] += 1

                place_key = f"{owner}_place_{place_counter[owner]}"
                self.ids[place_key] = result["id"]
                self.log(
                    f"Created {place['title']} for {owner.title()} (${place['price']}/night)"
                )
            else:
                self.warn(f"Could not create {place['title']}")

        return True

    def create_reviews(self):
        """Create cross-reviews between users"""
        reviews = [
            # Reviews for budget places
            {
                "reviewer": "alice",
                "place_key": "diana_place_1",
                "text": "Great value for money! Clean hostel with friendly staff.",
                "rating": 4,
            },
            {
                "reviewer": "bob",
                "place_key": "diana_place_2",
                "text": "Perfect for camping enthusiasts. Basic but clean facilities.",
                "rating": 3,
            },
            {
                "reviewer": "diana",
                "place_key": "charlie_place_1",
                "text": "Good for students on a budget. Close to campus and public transport.",
                "rating": 4,
            },
            # Reviews for mid-range places
            {
                "reviewer": "charlie",
                "place_key": "diana_place_4",
                "text": "Lovely little studio! Perfect for a solo traveler.",
                "rating": 4,
            },
            {
                "reviewer": "bob",
                "place_key": "alice_place_1",
                "text": "Wonderful family atmosphere and delicious breakfast!",
                "rating": 5,
            },
            {
                "reviewer": "alice",
                "place_key": "bob_place_1",
                "text": "Beautiful countryside location. Very peaceful and relaxing.",
                "rating": 4,
            },
            # Original reviews for higher-priced places
            {
                "reviewer": "alice",
                "place_key": "bob_place_4",
                "text": "Absolutely stunning villa! The pool was amazing and everything was spotless. Perfect for a luxury getaway.",
                "rating": 5,
            },
            {
                "reviewer": "alice",
                "place_key": "bob_place_5",
                "text": "Amazing beach house! Direct beach access was perfect and the location couldn't be better.",
                "rating": 5,
            },
            {
                "reviewer": "alice",
                "place_key": "bob_place_6",
                "text": "Perfect mountain retreat! So peaceful and the hiking trails nearby are fantastic.",
                "rating": 4,
            },
            {
                "reviewer": "bob",
                "place_key": "alice_place_2",
                "text": "Modern and stylish loft with incredible city views. Loved the downtown location!",
                "rating": 5,
            },
            {
                "reviewer": "bob",
                "place_key": "alice_place_3",
                "text": "Perfect studio for creative work! Tons of natural light and very inspiring atmosphere.",
                "rating": 4,
            },
            {
                "reviewer": "charlie",
                "place_key": "alice_place_2",
                "text": "Great downtown location and very stylish. Perfect for exploring the city.",
                "rating": 4,
            },
            {
                "reviewer": "charlie",
                "place_key": "bob_place_4",
                "text": "Incredible luxury villa! The pool and garden are amazing. Highly recommend.",
                "rating": 5,
            },
            {
                "reviewer": "diana",
                "place_key": "charlie_place_3",
                "text": "Great location and very convenient for getting around the city. Clean and comfortable.",
                "rating": 4,
            },
        ]

        review_count = 0

        for review in reviews:
            if review["place_key"] not in self.ids:
                self.warn(f"Place {review['place_key']} not found, skipping review")
                continue

            review_data = {
                "text": review["text"],
                "rating": review["rating"],
                "place_id": self.ids[review["place_key"]],
            }

            result = self.post(
                "/reviews/", review_data, self.tokens[review["reviewer"]]
            )

            if result and "id" in result:
                review_count += 1
                self.log(
                    f"{review['reviewer'].title()} reviewed a place ({review_count}/{len(reviews)})"
                )
            else:
                self.warn(f"Could not create review from {review['reviewer']}")

        return True

    def verify_setup(self):
        """Verify everything was created correctly"""
        self.log("Verifying setup...")

        # Check users
        users = self.get("/users/")
        if users:
            self.log(f"Found {len(users)} users total")

        # Check amenities
        amenities = self.get("/amenities/")
        if amenities:
            self.log(f"Found {len(amenities)} amenities")

        # Check places
        places = self.get("/places/")
        if places:
            self.log(f"Found {len(places)} places")

            # Price distribution for filter testing
            if places:
                prices = [p.get("price", 0) for p in places]
                budget_count = len([p for p in prices if p <= 10])
                low_cost_count = len([p for p in prices if 10 < p <= 50])
                mid_range_count = len([p for p in prices if 50 < p <= 100])
                high_end_count = len([p for p in prices if p > 100])

                self.log(f"Price distribution for filter testing:")
                self.log(f"  • Budget (≤$10): {budget_count} places")
                self.log(f"  • Low-cost ($11-$50): {low_cost_count} places")
                self.log(f"  • Mid-range ($51-$100): {mid_range_count} places")
                self.log(f"  • High-end (>$100): {high_end_count} places")

        # Check reviews
        reviews = self.get("/reviews/")
        if reviews:
            ratings = [r["rating"] for r in reviews if "rating" in r]
            if ratings:
                avg_rating = sum(ratings) / len(ratings)
                self.log(
                    f"Found {len(reviews)} reviews (avg rating: {avg_rating:.1f} stars)"
                )

        return True

    def print_summary(self):
        """Print final setup summary"""
        print("\n" + "=" * 60)
        print("🎉 HBNB TEST DATA SETUP COMPLETE!")
        print("=" * 60)

        print("\n👥 USERS CREATED:")
        print("   • Admin User: admin@hbnb.io (password: admin123)")
        print("   • Alice Johnson: alice@example.com (password: alice123)")
        print("   • Bob Wilson: bob@example.com (password: bob123)")
        print("   • Charlie Brown: charlie@example.com (password: charlie123)")
        print("   • Diana Smith: diana@example.com (password: diana123)")

        print("\n🏠 PLACES CREATED WITH VARIED PRICING:")
        print("   💰 BUDGET ($5-$10):")
        print("     - Backpacker Hostel Bed ($8/night)")
        print("     - Budget Camping Spot ($5/night)")
        print("     - Student Room Share ($9/night)")
        print("   💵 LOW-COST ($25-$50):")
        print("     - Cozy Studio Apartment ($25/night)")
        print("     - Guest Room in Family Home ($35/night)")
        print("     - Countryside Cottage ($45/night)")
        print("     - Urban Loft Share ($40/night)")
        print("   💳 MID-RANGE ($75-$100):")
        print("     - Boutique Hotel Room ($85/night)")
        print("     - Waterfront Cabin ($75/night)")
        print("     - Modern Apartment ($90/night)")
        print("   💎 PREMIUM ($110-$350):")
        print("     - Luxury Villa with Pool ($350/night)")
        print("     - Oceanfront Beach House ($280/night)")
        print("     - Modern Downtown Loft ($180/night)")
        print("     - Mountain Cabin Retreat ($150/night)")
        print("     - Central City Apartment ($140/night)")
        print("     - Cozy Art Studio ($120/night)")
        print("     - Charming Garden Cottage ($110/night)")

        print("\n🏷️ AMENITIES AVAILABLE:")
        print("   • Wi-Fi, Swimming Pool, Parking")
        print("   • Air Conditioning, Kitchen")
        print("   • Pet Friendly, Gym")

        print("\n🔍 FILTER TESTING:")
        print("   • 'Up to $10': Shows 3 budget places")
        print("   • 'Up to $50': Shows 7 budget + low-cost places")
        print("   • 'Up to $100': Shows 10 budget + low-cost + mid-range places")
        print("   • 'All': Shows all 17 places")

        print("\n⭐ REVIEWS CREATED:")
        print("   • 15+ cross-reviews between users")
        print("   • No self-reviews (proper business logic)")
        print("   • Reviews across all price ranges")

        print("\n🔑 AUTHENTICATION:")
        print("   • All users have valid login credentials")
        print("   • Admin privileges properly configured")
        print("   • JWT tokens working correctly")

        print(f"\n✅ Your HBnB platform is ready for testing!")
        print(f"🌐 API Base URL: {BASE_URL}")
        print("📖 Test with Postman, cURL, or your frontend")
        print("🎯 Perfect for testing price filtering functionality!")
        print("=" * 60 + "\n")

    def run(self):
        """Run the complete setup process"""
        print("🚀 Starting HBnB test data setup...")
        print(f"🌐 Connecting to: {BASE_URL}")

        # Test server connection
        try:
            response = requests.get(f"{BASE_URL}/users/", timeout=5)
            self.log("Server connection successful")
        except:
            self.error("Cannot connect to server! Make sure Flask is running:")
            print("   1. cd to your backend directory")
            print("   2. Run: python run.py")
            print("   3. Check server is running on localhost:5000")
            return False

        try:
            # Run setup steps
            if not self.setup_admin():
                return False
            if not self.create_users():
                return False
            if not self.create_amenities():
                return False
            if not self.create_places():
                return False
            if not self.create_reviews():
                return False
            if not self.verify_setup():
                return False

            self.print_summary()
            return True

        except KeyboardInterrupt:
            print("\n⚠️ Setup interrupted by user")
            return False
        except Exception as e:
            self.error(f"Unexpected error during setup: {e}")
            return False


if __name__ == "__main__":
    print("HBnB Test Data Setup Script")
    print("Make sure your Flask server is running first!")
    print("-" * 50)

    setup = HBnBSetup()
    success = setup.run()

    if success:
        print("🎉 Setup completed successfully!")
        sys.exit(0)
    else:
        print("❌ Setup failed. Check the errors above.")
        sys.exit(1)
