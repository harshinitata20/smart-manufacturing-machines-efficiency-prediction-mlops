import pytest
import json
import numpy as np
from unittest.mock import patch, MagicMock

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from application import app


@pytest.fixture
def client():
    """Create test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def sample_prediction_data():
    """Sample data for prediction testing"""
    return {
        'Operation_Mode': 1,
        'Temperature_C': 75.5,
        'Vibration_Hz': 2.8,
        'Power_Consumption_kW': 5.2,
        'Network_Latency_ms': 15.3,
        'Packet_Loss_%': 1.2,
        'Quality_Control_Defect_Rate_%': 3.5,
        'Production_Speed_units_per_hr': 350.0,
        'Predictive_Maintenance_Score': 0.85,
        'Error_Rate_%': 5.2,
        'Year': 2024,
        'Month': 1,
        'Day': 1,
        'Hour': 12
    }


class TestApplication:
    """Test suite for Flask application"""

    def test_health_endpoint(self, client):
        """Test health check endpoint"""
        response = client.get('/health')
        assert response.status_code == 200
        
        data = json.loads(response.data)
        assert 'status' in data
        assert 'model_loaded' in data
        assert 'scaler_loaded' in data

    def test_index_get(self, client):
        """Test GET request to index endpoint"""
        response = client.get('/')
        assert response.status_code == 200
        # Check if HTML is returned
        assert b'Smart Manufacturing Efficiency Predictor' in response.data

    @patch('application.model')
    @patch('application.scaler')
    def test_predict_endpoint_success(self, mock_scaler, mock_model, client, sample_prediction_data):
        """Test successful prediction"""
        # Mock model and scaler
        mock_scaler.transform.return_value = np.array([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]])
        mock_model.predict.return_value = np.array([1])
        mock_model.predict_proba.return_value = np.array([[0.1, 0.8, 0.1]])
        
        response = client.post('/predict', 
                             data=json.dumps(sample_prediction_data),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert 'prediction' in data
        assert 'confidence' in data
        assert 'class' in data
        assert 'probabilities' in data
        assert data['prediction'] == 'Medium Efficiency'
        assert data['class'] == 1

    @patch('application.model', None)
    @patch('application.scaler', None)
    def test_predict_endpoint_model_not_loaded(self, client, sample_prediction_data):
        """Test prediction when model is not loaded"""
        response = client.post('/predict', 
                             data=json.dumps(sample_prediction_data),
                             content_type='application/json')
        
        assert response.status_code == 500
        data = json.loads(response.data)
        assert 'error' in data
        assert data['error'] == 'Model not loaded'

    def test_predict_endpoint_invalid_data(self, client):
        """Test prediction with invalid data"""
        invalid_data = {'invalid': 'data'}
        
        response = client.post('/predict', 
                             data=json.dumps(invalid_data),
                             content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

    @patch('application.model')
    @patch('application.scaler')
    def test_index_post_success(self, mock_scaler, mock_model, client, sample_prediction_data):
        """Test POST request to index endpoint"""
        # Mock model and scaler
        mock_scaler.transform.return_value = np.array([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]])
        mock_model.predict.return_value = np.array([2])
        mock_model.predict_proba.return_value = np.array([[0.1, 0.2, 0.7]])
        
        response = client.post('/', 
                             data=json.dumps(sample_prediction_data),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert 'prediction' in data
        assert 'confidence' in data
        assert 'class' in data
        assert data['prediction'] == 'High Efficiency'
        assert data['class'] == 2

    def test_predict_endpoint_missing_features(self, client):
        """Test prediction with missing features"""
        incomplete_data = {
            'Operation_Mode': 1,
            'Temperature_C': 75.5
            # Missing other required features
        }
        
        response = client.post('/predict', 
                             data=json.dumps(incomplete_data),
                             content_type='application/json')
        
        assert response.status_code == 400

    @patch('application.model')
    @patch('application.scaler')
    def test_label_mapping(self, mock_scaler, mock_model, client, sample_prediction_data):
        """Test that label mapping works correctly"""
        mock_scaler.transform.return_value = np.array([[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]])
        
        # Test each class
        for class_id, expected_label in [(0, 'Low Efficiency'), (1, 'Medium Efficiency'), (2, 'High Efficiency')]:
            mock_model.predict.return_value = np.array([class_id])
            mock_model.predict_proba.return_value = np.array([[0.1, 0.1, 0.8]])
            
            response = client.post('/predict', 
                                 data=json.dumps(sample_prediction_data),
                                 content_type='application/json')
            
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data['prediction'] == expected_label
            assert data['class'] == class_id

    def test_content_type_validation(self, client, sample_prediction_data):
        """Test that endpoints require JSON content type"""
        response = client.post('/predict', 
                             data=sample_prediction_data)  # No JSON content type
        
        # Should handle gracefully or return appropriate error
        assert response.status_code in [400, 500]