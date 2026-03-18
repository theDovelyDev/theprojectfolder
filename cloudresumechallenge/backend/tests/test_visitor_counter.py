import json
import pytest
from unittest.mock import patch, MagicMock, Mock
import sys
import os

# Mock boto3 BEFORE importing visitor_counter
mock_boto3 = Mock()
mock_dynamodb_resource = MagicMock()
mock_table = MagicMock()

mock_boto3.resource.return_value = mock_dynamodb_resource
mock_dynamodb_resource.Table.return_value = mock_table

sys.modules['boto3'] = mock_boto3

# Add the lambda directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../lambda'))

# Now import visitor_counter (boto3 is already mocked)
from visitor_counter import lambda_handler

@pytest.fixture
def reset_mock():
    """Reset mock state before each test"""
    mock_table.reset_mock()
    # Clear any side effects from previous tests
    mock_table.get_item.side_effect = None
    mock_table.update_item.side_effect = None
    yield mock_table

@pytest.fixture
def mock_env():
    """Mock environment variables"""
    with patch.dict(os.environ, {
        'ALLOWED_ORIGIN': 'https://www.theprojectfolder.com',
        'DYNAMODB_TABLE': 'VisitorCountTable-test'
    }):
        yield

class TestVisitorCounterGET:
    """Tests for GET requests"""
    
    def test_get_returns_visitor_count(self, reset_mock, mock_env):
        """Test GET request returns current visitor count"""
        # Arrange
        reset_mock.get_item.return_value = {
            'Item': {'visitor_count_id': 'global', 'visitorCount': 42}
        }
        
        event = {
            'requestContext': {
                'http': {'method': 'GET'}
            }
        }
        
        # Act
        response = lambda_handler(event, None)
        
        # Assert
        assert response['statusCode'] == 200
        assert json.loads(response['body'])['visitorCount'] == 42
        assert 'Access-Control-Allow-Origin' in response['headers']
        reset_mock.get_item.assert_called_once_with(Key={'visitor_count_id': 'global'})
    
    def test_get_returns_zero_for_new_counter(self, reset_mock, mock_env):
        """Test GET returns 0 when no visitor count exists"""
        # Arrange
        reset_mock.get_item.return_value = {}
        
        event = {
            'requestContext': {
                'http': {'method': 'GET'}
            }
        }
        
        # Act
        response = lambda_handler(event, None)
        
        # Assert
        assert response['statusCode'] == 200
        assert json.loads(response['body'])['visitorCount'] == 0
    
    def test_get_handles_dynamodb_error(self, reset_mock, mock_env):
        """Test GET handles DynamoDB errors gracefully"""
        # Arrange
        reset_mock.get_item.side_effect = Exception("DynamoDB connection failed")
        
        event = {
            'requestContext': {
                'http': {'method': 'GET'}
            }
        }
        
        # Act
        response = lambda_handler(event, None)
        
        # Assert
        assert response['statusCode'] == 500
        assert 'error' in json.loads(response['body'])


class TestVisitorCounterPOST:
    """Tests for POST requests"""
    
    def test_post_increments_counter(self, reset_mock, mock_env):
        """Test POST increments visitor count"""
        # Arrange
        reset_mock.update_item.return_value = {
            'Attributes': {'visitorCount': 43}
        }
        
        event = {
            'requestContext': {
                'http': {'method': 'POST'}
            }
        }
        
        # Act
        response = lambda_handler(event, None)
        
        # Assert
        assert response['statusCode'] == 200
        assert json.loads(response['body'])['visitorCount'] == 43
        reset_mock.update_item.assert_called_once()
    
    def test_post_initializes_new_counter(self, reset_mock, mock_env):
        """Test POST creates counter starting at 1 if it doesn't exist"""
        # Arrange
        reset_mock.update_item.return_value = {
            'Attributes': {'visitorCount': 1}
        }
        
        event = {
            'requestContext': {
                'http': {'method': 'POST'}
            }
        }
        
        # Act
        response = lambda_handler(event, None)
        
        # Assert
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert body['visitorCount'] == 1
        
        # Verify update_item was called with correct expression
        call_args = reset_mock.update_item.call_args
        assert 'if_not_exists' in call_args.kwargs['UpdateExpression']
    
    def test_post_handles_dynamodb_error(self, reset_mock, mock_env):
        """Test POST handles DynamoDB errors gracefully"""
        # Arrange
        reset_mock.update_item.side_effect = Exception("DynamoDB write failed")
        
        event = {
            'requestContext': {
                'http': {'method': 'POST'}
            }
        }
        
        # Act
        response = lambda_handler(event, None)
        
        # Assert
        assert response['statusCode'] == 500
        assert 'error' in json.loads(response['body'])


class TestCORS:
    """Tests for CORS handling"""
    
    def test_options_preflight_request(self, reset_mock, mock_env):
        """Test OPTIONS preflight request returns correct CORS headers"""
        # Arrange
        event = {
            'requestContext': {
                'http': {'method': 'OPTIONS'}
            }
        }
        
        # Act
        response = lambda_handler(event, None)
        
        # Assert
        assert response['statusCode'] == 200
        assert response['headers']['Access-Control-Allow-Origin'] == 'https://www.theprojectfolder.com'
        assert 'GET, POST, OPTIONS' in response['headers']['Access-Control-Allow-Methods']
        assert 'Content-Type' in response['headers']['Access-Control-Allow-Headers']
    
    def test_cors_headers_present_on_get(self, reset_mock, mock_env):
        """Test CORS headers are present on GET response"""
        # Arrange
        reset_mock.get_item.return_value = {'Item': {'visitorCount': 10}}
        event = {
            'requestContext': {
                'http': {'method': 'GET'}
            }
        }
        
        # Act
        response = lambda_handler(event, None)
        
        # Assert
        assert 'Access-Control-Allow-Origin' in response['headers']
        assert 'Access-Control-Allow-Methods' in response['headers']
    
    def test_cors_headers_present_on_post(self, reset_mock, mock_env):
        """Test CORS headers are present on POST response"""
        # Arrange
        reset_mock.update_item.return_value = {'Attributes': {'visitorCount': 11}}
        event = {
            'requestContext': {
                'http': {'method': 'POST'}
            }
        }
        
        # Act
        response = lambda_handler(event, None)
        
        # Assert
        assert 'Access-Control-Allow-Origin' in response['headers']


class TestMethodHandling:
    """Tests for HTTP method handling"""
    
    def test_unsupported_method_returns_405(self, reset_mock, mock_env):
        """Test unsupported HTTP methods return 405 Method Not Allowed"""
        # Arrange
        event = {
            'requestContext': {
                'http': {'method': 'DELETE'}
            }
        }
        
        # Act
        response = lambda_handler(event, None)
        
        # Assert
        assert response['statusCode'] == 405
        assert 'error' in json.loads(response['body'])
    
    def test_missing_method_defaults_to_get(self, reset_mock, mock_env):
        """Test missing method defaults to GET"""
        # Arrange
        reset_mock.get_item.return_value = {'Item': {'visitorCount': 5}}
        event = {
            'requestContext': {
                'http': {}  # Empty http object
            }
        }
        
        # Act
        response = lambda_handler(event, None)
        
        # Assert
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert body['visitorCount'] == 5
        reset_mock.get_item.assert_called_once()


class TestResponseFormat:
    """Tests for response formatting"""
    
    def test_response_has_correct_content_type(self, reset_mock, mock_env):
        """Test responses have application/json content type"""
        # Arrange
        reset_mock.get_item.return_value = {'Item': {'visitorCount': 100}}
        event = {
            'requestContext': {
                'http': {'method': 'GET'}
            }
        }
        
        # Act
        response = lambda_handler(event, None)
        
        # Assert
        assert response['headers']['Content-Type'] == 'application/json'
    
    def test_visitor_count_is_integer(self, reset_mock, mock_env):
        """Test visitor count is returned as integer"""
        # Arrange
        reset_mock.get_item.return_value = {'Item': {'visitor_count_id': 'global', 'visitorCount': 50}}
        event = {
            'requestContext': {
                'http': {'method': 'GET'}
            }
        }
    
        # Act
        response = lambda_handler(event, None)
        body = json.loads(response['body'])
    
        # Assert
        assert 'visitorCount' in body
        assert isinstance(body['visitorCount'], int)
        assert body['visitorCount'] == 50