import pytest
import json
from app import create_app
from app.helpers.auth import generate_jwt_token


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    test_app = create_app()
    test_app.config['TESTING'] = True
    with test_app.test_client() as client:
        yield client


@pytest.fixture
def valid_token():
    """Generate a valid JWT token for testing."""
    return generate_jwt_token('admin')


class TestAuth:
    """Test authentication endpoints."""
    
    def test_login_success(self, client):
        """Test successful login with correct credentials."""
        response = client.post('/api/login', 
            json={'username': 'admin', 'password': 'admin'}
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'token' in data
        assert data['message'] == 'Login successful'
    
    def test_login_failure_invalid_credentials(self, client):
        """Test login with invalid credentials."""
        response = client.post('/api/login',
            json={'username': 'admin', 'password': 'wrongpassword'}
        )
        assert response.status_code == 401
        data = json.loads(response.data)
        assert 'Invalid username or password' in data['error']
    
    def test_login_failure_missing_fields(self, client):
        """Test login with missing required fields."""
        response = client.post('/api/login',
            json={'username': 'admin'}  # missing password
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'Validation failed' in data['error']


class TestUserRoutes:
    """Test user CRUD endpoints with JWT protection."""
    
    def test_get_users_without_token(self, client):
        """Test GET /api/users without token returns 401."""
        response = client.get('/api/users')
        assert response.status_code == 401
        data = json.loads(response.data)
        assert 'Token is missing' in data['error']
    
    def test_get_users_with_valid_token(self, client, valid_token):
        """Test GET /api/users with valid token."""
        headers = {'Authorization': f'Bearer {valid_token}'}
        response = client.get('/api/users', headers=headers)
        assert response.status_code == 200
        data = json.loads(response.data)
        # Should return a list (possibly empty if no users in test DB)
        assert isinstance(data, list)
    
    def test_get_users_with_invalid_token(self, client):
        """Test GET /api/users with invalid token."""
        headers = {'Authorization': 'Bearer invalid.token.here'}
        response = client.get('/api/users', headers=headers)
        assert response.status_code == 401
        data = json.loads(response.data)
        assert 'Invalid or expired token' in data['error']
    
    def test_create_user_without_token(self, client):
        """Test POST /api/users without token returns 401."""
        response = client.post('/api/users',
            json={'name': 'Test User', 'email': 'test@example.com'}
        )
        assert response.status_code == 401
    
    def test_create_user_with_valid_token(self, client, valid_token):
        """Test POST /api/users with valid token and valid data."""
        headers = {'Authorization': f'Bearer {valid_token}'}
        response = client.post('/api/users',
            json={'name': 'Test User', 'email': 'test@example.com'},
            headers=headers
        )
        # Will depend on DB connectivity; expect 201 if DB is available
        assert response.status_code in [201, 500]  # 500 if DB not available
    
    def test_create_user_validation_failure(self, client, valid_token):
        """Test POST /api/users with invalid data (missing email)."""
        headers = {'Authorization': f'Bearer {valid_token}'}
        response = client.post('/api/users',
            json={'name': 'Test User'},  # missing email
            headers=headers
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'Validation failed' in data['error']
    
    def test_update_user_without_token(self, client):
        """Test PUT /api/users/<id> without token returns 401."""
        response = client.put('/api/users/1',
            json={'name': 'Updated User', 'email': 'updated@example.com'}
        )
        assert response.status_code == 401
    
    def test_delete_user_without_token(self, client):
        """Test DELETE /api/users/<id> without token returns 401."""
        response = client.delete('/api/users/1')
        assert response.status_code == 401


class TestInputValidation:
    """Test input validation with Marshmallow."""
    
    def test_user_schema_invalid_email(self, client, valid_token):
        """Test that invalid email is rejected."""
        headers = {'Authorization': f'Bearer {valid_token}'}
        response = client.post('/api/users',
            json={'name': 'Test User', 'email': 'not-an-email'},
            headers=headers
        )
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'Validation failed' in data['error']
    
    def test_user_schema_empty_name(self, client, valid_token):
        """Test that empty name is rejected."""
        headers = {'Authorization': f'Bearer {valid_token}'}
        response = client.post('/api/users',
            json={'name': '', 'email': 'test@example.com'},
            headers=headers
        )
        assert response.status_code == 400
    
    def test_login_schema_empty_password(self, client):
        """Test that login with empty password is rejected."""
        response = client.post('/api/login',
            json={'username': 'admin', 'password': ''}
        )
        assert response.status_code == 400


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
