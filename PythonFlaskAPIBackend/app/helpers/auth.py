import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify
from app import config


def generate_jwt_token(username, expires_in=160):
    """
    Generate a JWT token for the given username.
    
    Args:
        username: The username to encode in the token.
        expires_in: Token expiration time in seconds (default: 1 hour).
    
    Returns:
        A signed JWT token.
    """
    payload = {
        'username': username,
        'exp': datetime.utcnow() + timedelta(seconds=expires_in),
        'iat': datetime.utcnow()
    }
    token = jwt.encode(payload, config.SECRET_KEY, algorithm='HS256')
    return token


def verify_jwt_token(token):
    """
    Verify and decode a JWT token.
    
    Args:
        token: The JWT token to verify.
    
    Returns:
        Decoded payload (dict) if valid, None if invalid.
    """
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def token_required(f):
    """
    Decorator to protect routes that require a valid JWT token.
    Expects the token in the Authorization header: "Bearer <token>"
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Check for token in Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            # Accept the following common formats:
            # - "Bearer <token>"
            # - "<token>" (raw token)
            parts = auth_header.split()
            if len(parts) == 2 and parts[0].lower() == 'bearer':
                token = parts[1]
            elif len(parts) == 1:
                token = parts[0]
            else:
                return jsonify({'error': 'Invalid token format. Use: Bearer <token>'}), 401
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        payload = verify_jwt_token(token)
        if payload is None:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        # Pass username to the route function
        return f(payload['username'], *args, **kwargs)
    
    return decorated
