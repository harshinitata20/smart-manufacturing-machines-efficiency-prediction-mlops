import pytest
import pandas as pd
import numpy as np
import tempfile
import os
import sys
from unittest.mock import patch, MagicMock

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture
def sample_data():
    """Create sample manufacturing data for testing"""
    np.random.seed(42)
    data = {
        'Timestamp': pd.date_range('2024-01-01', periods=100, freq='H'),
        'Machine_ID': np.random.randint(1, 50, 100),
        'Operation_Mode': np.random.choice([0, 1], 100),
        'Temperature_C': np.random.uniform(20, 100, 100),
        'Vibration_Hz': np.random.uniform(0, 5, 100),
        'Power_Consumption_kW': np.random.uniform(1, 10, 100),
        'Network_Latency_ms': np.random.uniform(5, 50, 100),
        'Packet_Loss_%': np.random.uniform(0, 5, 100),
        'Quality_Control_Defect_Rate_%': np.random.uniform(0, 10, 100),
        'Production_Speed_units_per_hr': np.random.uniform(50, 500, 100),
        'Predictive_Maintenance_Score': np.random.uniform(0, 1, 100),
        'Error_Rate_%': np.random.uniform(0, 20, 100),
        'Efficiency_Status': np.random.choice([0, 1, 2], 100)
    }
    return pd.DataFrame(data)


@pytest.fixture
def temp_dir():
    """Create temporary directory for test files"""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield temp_dir


@pytest.fixture
def sample_csv_file(sample_data, temp_dir):
    """Create sample CSV file for testing"""
    csv_path = os.path.join(temp_dir, 'test_data.csv')
    sample_data.to_csv(csv_path, index=False)
    return csv_path


@pytest.fixture
def mock_logger():
    """Mock logger for testing"""
    with patch('src.logger.get_logger') as mock_get_logger:
        mock_logger_instance = MagicMock()
        mock_get_logger.return_value = mock_logger_instance
        yield mock_logger_instance