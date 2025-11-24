from flask import Blueprint, request, jsonify
import jwt
from marshmallow import ValidationError
from app.config import SECRET_KEY
from app.services.services import LoginService, UserService
from app.schemas.schemas import UserSchema, UserLoginSchema
from app.helpers.auth import token_required, generate_jwt_token
from app.helpers.db_connection import get_db_connection

user_bp = Blueprint('users', __name__)
user_schema = UserSchema()
login_schema = UserLoginSchema()


@user_bp.route('/login', methods=['POST'])
def login():
    """
    User login endpoint to get JWT token
    ---
    tags:
      - Auth
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
              example: "admin"
            password:
              type: string
              example: "password123"
    responses:
      200:
        description: Login successful, JWT token returned
        example:
          token: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
      400:
        description: Invalid credentials or validation error
    """
    try:
        data = login_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({'error': 'Validation failed', 'messages': err.messages}), 400
    
    if LoginService.validate_user(data['username'], data['password']) and data.get('username') and data.get('password'):
        token = generate_jwt_token(data['username'])
        return jsonify({'token': token, 'message': 'Login successful'}), 200
    
    return jsonify({'error': 'Invalid username or password'}), 401

@user_bp.route('/refresh-token', methods=['POST'])
def refresh_token():
    """Issue a new token if the current token is valid and not expired."""
    
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        return jsonify({'error': 'Authorization header missing'}), 401

    try:
        token = auth_header.split(" ")[1]  # "Bearer <token>"
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        
        username = decoded.get("username")
        if not username:
            return jsonify({'error': 'Invalid token payload'}), 401

        # Generate fresh token
        new_token = generate_jwt_token(username)
        return jsonify({'token': new_token}), 200

    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token'}), 401


@user_bp.route('/users', methods=['GET'])
@token_required
def get_users(current_user):
    """
    Get all users (protected)
    ---
    tags:
      - Users
    security:
      - Bearer: []
    responses:
      200:
        description: List of all users
        example:
          - id: 1
            name: "John"
            email: "john@example.com"
      401:
        description: Unauthorized - missing or invalid token
    """
    users = UserService.get_all_users()
    return jsonify(users), 200

@user_bp.route('/users/<int:user_id>', methods=['GET'])
@token_required
def get_user(current_user, user_id):
    """
    Get a user by ID (protected)
    ---
    tags:
      - Users
    security:
      - Bearer: []
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: User ID
    responses:
      200:
        description: User found
        example:
          id: 1
          name: "John"
          email: "john@example.com"
      404:
        description: User not found
      401:
        description: Unauthorized - missing or invalid token
    """
    user = UserService.get_user_by_id(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user), 200

@user_bp.route('/users', methods=['POST'])
@token_required
def create_user(current_user):
    """
    Create a new user (protected)
    ---
    tags:
      - Users
    security:
      - Bearer: []
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - name
            - email
          properties:
            name:
              type: string
              example: "John"
            email:
              type: string
              example: "john@example.com"
    responses:
      201:
        description: User created successfully
        example:
          id: 1
          name: "John"
          email: "john@example.com"
      400:
        description: Invalid data or validation error
      401:
        description: Unauthorized - missing or invalid token
    """
    try:
        data = user_schema.load(request.get_json())
    except ValidationError as err:
        print(err.messages)
        return jsonify({'error': 'Validation failed', 'messages': err.messages}), 400
    
    new_user = UserService.create_user(data['name'], data['email'])
    return jsonify(new_user), 201

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
@token_required
def update_user(current_user, user_id):
    """
    Update an existing user (protected)
    ---
    tags:
      - Users
    security:
      - Bearer: []
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: User ID
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              example: "John Updated"
            email:
              type: string
              example: "john.updated@example.com"
    responses:
      200:
        description: User updated successfully
        example:
          id: 1
          name: "John Updated"
          email: "john.updated@example.com"
      400:
        description: Invalid data or validation error
      404:
        description: User not found
      401:
        description: Unauthorized - missing or invalid token
    """
    try:
        data = user_schema.load(request.get_json(), partial=True)
    except ValidationError as err:
        return jsonify({'error': 'Validation failed', 'messages': err.messages}), 400
    
    # Check if user exists first
    if not UserService.get_user_by_id(user_id):
        return jsonify({'error': 'User not found'}), 404

    updated_user = UserService.update_user(user_id, data.get('name'), data.get('email'))
    return jsonify(updated_user), 200

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
@token_required
def delete_user(current_user, user_id):
    """
    Delete a user (protected)
    ---
    tags:
      - Users
    security:
      - Bearer: []
    parameters:
      - name: user_id
        in: path
        type: integer
        required: true
        description: User ID
    responses:
      200:
        description: User deleted successfully
      404:
        description: User not found
      401:
        description: Unauthorized - missing or invalid token
    """
    if not UserService.get_user_by_id(user_id):
        return jsonify({'error': 'User not found'}), 404
        
    UserService.delete_user(user_id)
    return jsonify({'message': 'User deleted'}), 200


@user_bp.route('/health', methods=['GET'])
def health():
    """Health-check endpoint for DB connectivity. Returns 200 when DB is reachable."""
    try:
        conn = get_db_connection()
        if not conn:
            raise Exception('unable to obtain DB connection')
        cursor = conn.cursor()
        cursor.execute('SELECT 1')
        cursor.fetchone()
        cursor.close()
        conn.close()
        return jsonify({"db": "ok"}), 200
    except Exception as e:
        return jsonify({"db": "error", "error": str(e)}), 500
