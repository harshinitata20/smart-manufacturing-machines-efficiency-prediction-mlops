import os
import sys
import subprocess

logger = None

def setup_imports():
    """Setup imports for the pipeline"""
    global logger
    
    # Get the project root directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    src_dir = os.path.join(project_root, 'src')
    
    # Add to Python path
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    if src_dir not in sys.path:
        sys.path.insert(0, src_dir)
    
    # Now import the modules
    try:
        from src.data_processing import DataProcessing
        from src.model_training import ModelTraining
        from src.logger import get_logger
        from src.exception import CustomException
        logger = get_logger(__name__)
        return DataProcessing, ModelTraining, get_logger, CustomException
    except ImportError as e:
        print(f"Import error: {e}")
        print("Running modules directly...")
        return None, None, None, None

def run_data_processing_directly():
    """Run data processing using subprocess"""
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        script_path = os.path.join(project_root, 'src', 'data_processing.py')
        
        print("Running data processing...")
        
        python_exe = r"C:/Users/Harshini/OneDrive/Documents/Desktop/mlops/smart-manufacturing/.venv/Scripts/python.exe"
        env = os.environ.copy()
        env['PYTHONPATH'] = project_root
        
        result = subprocess.run([python_exe, script_path], 
                              capture_output=True, text=True, cwd=project_root, env=env)
        
        if result.returncode == 0:
            print(" Data processing completed successfully")
            return True
        else:
            print(f" Data processing failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"Error running data processing: {e}")
        return False

def run_model_training_directly():
    """Run model training using subprocess"""
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        script_path = os.path.join(project_root, 'src', 'model_training.py')
        
        print("Running model training...")
        
        python_exe = r"C:/Users/Harshini/OneDrive/Documents/Desktop/mlops/smart-manufacturing/.venv/Scripts/python.exe"
        env = os.environ.copy()
        env['PYTHONPATH'] = project_root
        
        result = subprocess.run([python_exe, script_path], 
                              capture_output=True, text=True, cwd=project_root, env=env)
        
        if result.returncode == 0:
            print(" Model training completed successfully")
            print(result.stdout)  # Show the model evaluation results
            return True
        else:
            print(f" Model training failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"Error running model training: {e}")
        return False

class TrainingPipeline:
    def __init__(self, raw_data_path=None, processed_data_path=None, model_output_path=None):
        """
        Initialize the training pipeline with default paths if not provided
        """
        self.raw_data_path = raw_data_path or "artifacts/raw/manufacturing_6G_dataset.csv"
        self.processed_data_path = processed_data_path or "artifacts/processed/"
        self.model_output_path = model_output_path or "artifacts/model/"
        
        print(" Training Pipeline initialized")
        print(f" Raw data path: {self.raw_data_path}")
        print(f" Processed data path: {self.processed_data_path}")
        print(f" Model output path: {self.model_output_path}")

    def validate_paths(self):
        """
        Validate that required paths exist
        """
        try:
            if not os.path.exists(self.raw_data_path):
                raise FileNotFoundError(f"Raw data file not found: {self.raw_data_path}")
            
            # Create directories if they don't exist
            os.makedirs(self.processed_data_path, exist_ok=True)
            os.makedirs(self.model_output_path, exist_ok=True)
            
            print(" Path validation completed successfully")
            return True
            
        except Exception as e:
            print(f" Path validation failed: {e}")
            return False

    def run(self):
        """
        Run the complete training pipeline
        """
        try:
            print("\n" + "=" * 60)
            print("🚀 STARTING COMPLETE TRAINING PIPELINE")
            print("=" * 60)
            
            # Step 1: Validate paths
            print("\n📋 Step 1: Validating paths...")
            if not self.validate_paths():
                raise Exception("Path validation failed")
            
            # Step 2: Data processing
            print("\n🔄 Step 2: Running data processing...")
            if not run_data_processing_directly():
                raise Exception("Data processing failed")
            
            # Step 3: Model training
            print("\n🤖 Step 3: Running model training...")
            if not run_model_training_directly():
                raise Exception("Model training failed")
            
            print("\n" + "=" * 60)
            print("🎉 TRAINING PIPELINE COMPLETED SUCCESSFULLY!")
            print("=" * 60)
            
            print(f"\n📁 Processed data saved to: {self.processed_data_path}")
            print(f"🤖 Model saved to: {self.model_output_path}")
            print("📋 Check logs for detailed results")
            
        except Exception as e:
            print(f"\n❌ TRAINING PIPELINE FAILED: {e}")
            return False

if __name__ == "__main__":
    training_pipeline = TrainingPipeline(
        raw_data_path="artifacts/raw/manufacturing_6G_dataset.csv",
        processed_data_path="artifacts/processed/",
        model_output_path="artifacts/model/"
    )
    training_pipeline.run()