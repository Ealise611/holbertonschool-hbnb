from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity'),
    'description': fields.String(required=False, description='Description of the amenity')
})

@api.route('/')
class AmenityList(Resource):
    @jwt_required()
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity - ADMIN ONLY"""
        current_user = get_jwt_identity()
        
        # check if user is admin
        if not current_user.get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403
        
        amenity_data = api.payload
        
        #check for duplicate amenity name
        existing_amenity = facade.get_amenity_by_name(amenity_data['name'])
        if existing_amenity:
            return {'error': 'Amenity already exists'}, 400

        try:
            new_amenity = facade.create_amenity(amenity_data)
            return {
                'id': new_amenity.id,
                'name': new_amenity.name,
                'description': new_amenity.description
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'Invalid input data'}, 400

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities - PUBLIC ACCESS"""
        amenities = facade.get_all_amenities()
        return [
            {
                'id': amenity.id,
                'name': amenity.name,
                'description': amenity.description
            }
            for amenity in amenities
        ], 200

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID - PUBLIC ACCESS"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return {
            'id': amenity.id,
            'name': amenity.name,
            'description': amenity.description
        }, 200

    @jwt_required()
    @api.expect(amenity_model, validate=True)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information - ADMIN ONLY"""
        current_user = get_jwt_identity()
        
        # check for admin rights
        if not current_user.get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403
        
        # Gets the amenity to check if it exists
        amenity = facade.get_amenity(amenity_id)  # ✅ Add this line
        if not amenity:
            return {'error': 'Amenity not found'}, 404
            
        data = api.payload
        
        # Checks for duplicate names
        if 'name' in data and data['name'] != amenity.name:
            existing_amenity = facade.get_amenity_by_name(data['name'])
            if existing_amenity:
                return {'error': 'Amenity name already exists'}, 400

        try:
            updated_amenity = facade.update_amenity(amenity_id, data)

            return {
                'id': updated_amenity.id,
                'name': updated_amenity.name,
                'description': updated_amenity.description
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'Invalid input data'}, 400
