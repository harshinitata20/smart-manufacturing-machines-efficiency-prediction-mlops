import pytest
import pandas as pd
import numpy as np
import os
import tempfile
from unittest.mock import patch, MagicMock

import sys
import os

# Add project root to path  
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from src.data_processing import DataProcessing
except ImportError:
    # Try the fixed version
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
    from data_processing_fixed import DataProcessing


class TestDataProcessing:
    """Test suite for DataProcessing class"""

    def test_init(self, temp_dir):
        """Test DataProcessing initialization"""
        input_path = os.path.join(temp_dir, 'input.csv')
        output_path = os.path.join(temp_dir, 'output')
        
        processor = DataProcessing(input_path, output_path)
        
        assert processor.input_path == input_path
        assert processor.output_path == output_path
        assert processor.df is None
        assert processor.features is None
        assert os.path.exists(output_path)

    def test_load_data_success(self, sample_csv_file, temp_dir):
        """Test successful data loading"""
        output_path = os.path.join(temp_dir, 'output')
        processor = DataProcessing(sample_csv_file, output_path)
        
        df = processor.load_data()
        
        assert df is not None
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 100
        assert 'Timestamp' in df.columns
        assert 'Efficiency_Status' in df.columns

    def test_load_data_file_not_found(self, temp_dir):
        """Test data loading with non-existent file"""
        input_path = os.path.join(temp_dir, 'nonexistent.csv')
        output_path = os.path.join(temp_dir, 'output')
        processor = DataProcessing(input_path, output_path)
        
        with pytest.raises(Exception):
            processor.load_data()

    @patch('src.data_processing.get_logger')
    def test_preprocess_data(self, mock_get_logger, sample_csv_file, temp_dir):
        """Test data preprocessing"""
        output_path = os.path.join(temp_dir, 'output')
        processor = DataProcessing(sample_csv_file, output_path)
        processor.load_data()
        
        processed_df = processor.preprocess_data()
        
        assert processed_df is not None
        assert 'Timestamp' not in processed_df.columns
        assert 'Machine_ID' not in processed_df.columns
        assert 'Year' in processed_df.columns
        assert 'Month' in processed_df.columns
        assert 'Day' in processed_df.columns
        assert 'Hour' in processed_df.columns

    @patch('src.data_processing.get_logger')
    def test_split_and_scale(self, mock_get_logger, sample_csv_file, temp_dir):
        """Test data splitting and scaling"""
        output_path = os.path.join(temp_dir, 'output')
        processor = DataProcessing(sample_csv_file, output_path)
        processor.load_data()
        processor.preprocess_data()
        
        X_train, X_test, y_train, y_test = processor.split_and_scale()
        
        assert X_train is not None
        assert X_test is not None
        assert y_train is not None
        assert y_test is not None
        assert len(X_train) + len(X_test) == 100
        assert len(y_train) == len(X_train)
        assert len(y_test) == len(X_test)
        
        # Check if files are saved
        assert os.path.exists(os.path.join(output_path, 'X_train.pkl'))
        assert os.path.exists(os.path.join(output_path, 'X_test.pkl'))
        assert os.path.exists(os.path.join(output_path, 'y_train.pkl'))
        assert os.path.exists(os.path.join(output_path, 'y_test.pkl'))
        assert os.path.exists(os.path.join(output_path, 'scaler.pkl'))

    @patch('src.data_processing.get_logger')
    def test_run_pipeline(self, mock_get_logger, sample_csv_file, temp_dir):
        """Test complete pipeline run"""
        output_path = os.path.join(temp_dir, 'output')
        processor = DataProcessing(sample_csv_file, output_path)
        
        # Should not raise any exceptions
        processor.run()
        
        # Check if all output files exist
        assert os.path.exists(os.path.join(output_path, 'X_train.pkl'))
        assert os.path.exists(os.path.join(output_path, 'X_test.pkl'))
        assert os.path.exists(os.path.join(output_path, 'y_train.pkl'))
        assert os.path.exists(os.path.join(output_path, 'y_test.pkl'))
        assert os.path.exists(os.path.join(output_path, 'scaler.pkl'))

    def test_data_types_after_preprocessing(self, sample_csv_file, temp_dir):
        """Test data types after preprocessing"""
        output_path = os.path.join(temp_dir, 'output')
        processor = DataProcessing(sample_csv_file, output_path)
        processor.load_data()
        processed_df = processor.preprocess_data()
        
        # Check that categorical columns are properly encoded
        assert processed_df['Operation_Mode'].dtype in [np.int32, np.int64]
        assert processed_df['Efficiency_Status'].dtype in [np.int32, np.int64]
        
        # Check numeric columns
        numeric_cols = ['Temperature_C', 'Vibration_Hz', 'Power_Consumption_kW']
        for col in numeric_cols:
            if col in processed_df.columns:
                assert pd.api.types.is_numeric_dtype(processed_df[col])

    def test_feature_consistency(self, sample_csv_file, temp_dir):
        """Test that features list matches processed data columns"""
        output_path = os.path.join(temp_dir, 'output')
        processor = DataProcessing(sample_csv_file, output_path)
        processor.load_data()
        processor.preprocess_data()
        X_train, _, _, _ = processor.split_and_scale()
        
        expected_features = [
            'Operation_Mode', 'Temperature_C', 'Vibration_Hz',
            'Power_Consumption_kW', 'Network_Latency_ms', 'Packet_Loss_%',
            'Quality_Control_Defect_Rate_%', 'Production_Speed_units_per_hr',
            'Predictive_Maintenance_Score', 'Error_Rate_%', 'Year', 'Month', 'Day', 'Hour'
        ]
        
        assert len(X_train[0]) == len(expected_features)