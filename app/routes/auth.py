from flask_restx import Namespace, Resource, fields
from app.services.facade import Facade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace("Users", description="User operations")

# Define the user model for input validation and documentation
user_model = api.model(
    "User",
    {
        "first_name": fields.String(
            required=True, description="First name of the user"
        ),
        "last_name": fields.String(required=True, description="Last name of the user"),
        "email": fields.String(required=True, description="Email of the user"),
        "password": fields.String(
            required=True, format="password", description="Password of the user"
        ),
    },
)

facade = Facade()

@api.route("/")
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, "User successfully created")
    @api.response(400, "Email already registered")
    @api.response(400, "Invalid input data")
    def post(self):
        """Register a new user."""
        try:
            user_data = api.payload

            # Simulate email uniqueness check (to be replaced by real validation with persistence)
            existing_user = facade.get_user_by_email(user_data["email"])
            if existing_user:
                return {"error": "Email already registered"}, 400

            new_user = facade.create_user(user_data)
            return {
                "id": new_user.uuid,
                "message": "The user is successfully registered."
            }, 201
        except ValueError as e:
            return {"error": str(e)}, 400

    @api.response(200, "List of users retrieved successfully")
    @api.response(404, "User not found")
    def get(self):
        """Retrieve a list of all users."""
        try:
            users_list = facade.get_all_users()

            if not users_list:
                return {"message": "No user found"}, 404

            # Get the name of each user
            return [
                {
                    "id": user.uuid,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                }
                for user in users_list
            ], 200
        except ValueError as e:
            return {"error": str(e)}, 400
