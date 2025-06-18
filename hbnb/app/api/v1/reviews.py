from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('reviews', description='Review operations')

# Define the models for related entities
user_model = api.model('ReviewUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the reviewer'),
    'last_name': fields.String(description='Last name of the reviewer'),
    'email': fields.String(description='Email of the reviewer')
})

place_model = api.model('ReviewPlace', {
    'id': fields.String(description='Place ID'),
    'title': fields.String(description='Title of the place'),
    'latitude': fields.Float(description='Latitude of the place'),
    'longitude': fields.Float(description='Longitude of the place')
})

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Review text/comment'),
    'rating': fields.Integer(required=True, description='Rating from 1 to 5', min=1, max=5),
    'user_id': fields.String(required=True, description='ID of the user writing the review'),
    'place_id': fields.String(required=True, description='ID of the place being reviewed')
})

# Update model for PUT requests (excludes user_id and place_id)
review_update_model = api.model('ReviewUpdate', {
    'text': fields.String(required=False, description='Updated review text'),
    'rating': fields.Integer(required=False, description='Updated rating from 1 to 5', min=1, max=5)
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(400, 'User not found')
    @api.response(400, 'Place not found')
    @api.response(400, 'User has already reviewed this place')
    def post(self):
        """Submit a new review"""
        review_data = api.payload

        try:
            new_review = facade.create_review(review_data)
            return {
                'id': new_review.id,
                'text': new_review.text,
                'rating': new_review.rating,
                'user_id': new_review.user.id,
                'place_id': new_review.place.id
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'Invalid input data'}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        return [
            {
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user': {
                    'id': review.user.id,
                    'first_name': review.user.first_name,
                    'last_name': review.user.last_name
                },
                'place': {
                    'id': review.place.id,
                    'title': review.place.title
                }
            }
            for review in reviews
        ], 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        
        return {
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user': {
                'id': review.user.id,
                'first_name': review.user.first_name,
                'last_name': review.user.last_name,
                'email': review.user.email
            },
            'place': {
                'id': review.place.id,
                'title': review.place.title,
                'latitude': review.place.latitude,
                'longitude': review.place.longitude
            }
        }, 200

    @api.expect(review_update_model, validate=True)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information"""
        review_data = api.payload
        
        try:
            updated_review = facade.update_review(review_id, review_data)
            if not updated_review:
                return {'error': 'Review not found'}, 404
            
            return {
                'id': updated_review.id,
                'text': updated_review.text,
                'rating': updated_review.rating,
                'user_id': updated_review.user.id,
                'place_id': updated_review.place.id
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'Invalid input data'}, 400

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        success = facade.delete_review(review_id)
        if not success:
            return {'error': 'Review not found'}, 404
        
        return {'message': 'Review deleted successfully'}, 200

@api.route('/places/<place_id>')
class PlaceReviews(Resource):
    @api.response(200, 'Place reviews retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        # Check if place exists
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404
        
        reviews = facade.get_reviews_by_place(place_id)
        return [
            {
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user': {
                    'id': review.user.id,
                    'first_name': review.user.first_name,
                    'last_name': review.user.last_name
                }
            }
            for review in reviews
        ], 200