import pytest
import numpy as np
import joblib
import os
import tempfile
from unittest.mock import patch, MagicMock
from sklearn.linear_model import LogisticRegression

from src.model_training import ModelTraining


class TestModelTraining:
    """Test suite for ModelTraining class"""

    def test_init(self, temp_dir):
        """Test ModelTraining initialization"""
        processed_path = os.path.join(temp_dir, 'processed')
        model_path = os.path.join(temp_dir, 'model')
        
        trainer = ModelTraining(processed_path, model_path)
        
        assert trainer.processed_data_path == processed_path
        assert trainer.model_output_path == model_path
        assert trainer.clf is None
        assert os.path.exists(model_path)

    def create_sample_processed_data(self, processed_path):
        """Helper method to create sample processed data"""
        np.random.seed(42)
        
        # Create sample data
        X_train = np.random.rand(80, 14)
        X_test = np.random.rand(20, 14)
        y_train = np.random.randint(0, 3, 80)
        y_test = np.random.randint(0, 3, 20)
        
        # Save data
        os.makedirs(processed_path, exist_ok=True)
        joblib.dump(X_train, os.path.join(processed_path, 'X_train.pkl'))
        joblib.dump(X_test, os.path.join(processed_path, 'X_test.pkl'))
        joblib.dump(y_train, os.path.join(processed_path, 'y_train.pkl'))
        joblib.dump(y_test, os.path.join(processed_path, 'y_test.pkl'))

    @patch('src.model_training.get_logger')
    def test_load_processed_data(self, mock_get_logger, temp_dir):
        """Test loading processed data"""
        processed_path = os.path.join(temp_dir, 'processed')
        model_path = os.path.join(temp_dir, 'model')
        
        self.create_sample_processed_data(processed_path)
        
        trainer = ModelTraining(processed_path, model_path)
        trainer.load_processed_data()
        
        assert trainer.X_train is not None
        assert trainer.X_test is not None
        assert trainer.y_train is not None
        assert trainer.y_test is not None
        assert trainer.X_train.shape == (80, 14)
        assert trainer.X_test.shape == (20, 14)

    @patch('src.model_training.get_logger')
    def test_load_processed_data_missing_files(self, mock_get_logger, temp_dir):
        """Test loading processed data with missing files"""
        processed_path = os.path.join(temp_dir, 'processed')
        model_path = os.path.join(temp_dir, 'model')
        
        trainer = ModelTraining(processed_path, model_path)
        
        with pytest.raises(Exception):
            trainer.load_processed_data()

    @patch('src.model_training.get_logger')
    def test_train_model(self, mock_get_logger, temp_dir):
        """Test model training"""
        processed_path = os.path.join(temp_dir, 'processed')
        model_path = os.path.join(temp_dir, 'model')
        
        self.create_sample_processed_data(processed_path)
        
        trainer = ModelTraining(processed_path, model_path)
        trainer.load_processed_data()
        trainer.train_model()
        
        assert trainer.clf is not None
        assert isinstance(trainer.clf, LogisticRegression)
        assert os.path.exists(os.path.join(model_path, 'logistic_regression_model.pkl'))

    @patch('src.model_training.get_logger')
    def test_evaluate_model(self, mock_get_logger, temp_dir):
        """Test model evaluation"""
        processed_path = os.path.join(temp_dir, 'processed')
        model_path = os.path.join(temp_dir, 'model')
        
        self.create_sample_processed_data(processed_path)
        
        trainer = ModelTraining(processed_path, model_path)
        trainer.load_processed_data()
        trainer.train_model()
        
        # Should not raise any exceptions
        trainer.evaluate_model()

    @patch('src.model_training.get_logger')
    def test_run_complete_pipeline(self, mock_get_logger, temp_dir):
        """Test complete training pipeline"""
        processed_path = os.path.join(temp_dir, 'processed')
        model_path = os.path.join(temp_dir, 'model')
        
        self.create_sample_processed_data(processed_path)
        
        trainer = ModelTraining(processed_path, model_path)
        
        # Should not raise any exceptions
        trainer.run()
        
        # Check that model is trained and saved
        assert trainer.clf is not None
        assert os.path.exists(os.path.join(model_path, 'logistic_regression_model.pkl'))

    @patch('src.model_training.get_logger')
    def test_model_predictions(self, mock_get_logger, temp_dir):
        """Test that trained model can make predictions"""
        processed_path = os.path.join(temp_dir, 'processed')
        model_path = os.path.join(temp_dir, 'model')
        
        self.create_sample_processed_data(processed_path)
        
        trainer = ModelTraining(processed_path, model_path)
        trainer.load_processed_data()
        trainer.train_model()
        
        # Test predictions
        predictions = trainer.clf.predict(trainer.X_test)
        probabilities = trainer.clf.predict_proba(trainer.X_test)
        
        assert predictions is not None
        assert len(predictions) == len(trainer.X_test)
        assert probabilities is not None
        assert probabilities.shape == (len(trainer.X_test), 3)  # 3 classes
        assert all(pred in [0, 1, 2] for pred in predictions)

    @patch('src.model_training.get_logger')
    def test_model_persistence(self, mock_get_logger, temp_dir):
        """Test that saved model can be loaded and used"""
        processed_path = os.path.join(temp_dir, 'processed')
        model_path = os.path.join(temp_dir, 'model')
        
        self.create_sample_processed_data(processed_path)
        
        trainer = ModelTraining(processed_path, model_path)
        trainer.run()
        
        # Load the saved model
        saved_model = joblib.load(os.path.join(model_path, 'logistic_regression_model.pkl'))
        
        # Test that loaded model works
        X_test = joblib.load(os.path.join(processed_path, 'X_test.pkl'))
        predictions = saved_model.predict(X_test)
        
        assert predictions is not None
        assert len(predictions) == len(X_test)