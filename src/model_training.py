import os
import sys
import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from src.logger import get_logger
from src.exception import CustomException
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, recall_score, precision_score, f1_score

logger = get_logger(__name__)

class ModelTraining:
    def __init__(self, processed_data_path, model_output_path):
        self.processed_data_path = processed_data_path
        self.model_output_path = model_output_path
        self.clf = None
        self.X_train, self.X_test, self.y_train, self.y_test = None, None, None, None

        os.makedirs(self.model_output_path, exist_ok=True)
        logger.info(f"Model output directory set at: {self.model_output_path}")

    def load_processed_data(self):
        try:
            self.X_train = joblib.load(os.path.join(self.processed_data_path, 'X_train.pkl'))
            self.X_test = joblib.load(os.path.join(self.processed_data_path, 'X_test.pkl'))
            self.y_train = joblib.load(os.path.join(self.processed_data_path, 'y_train.pkl'))
            self.y_test = joblib.load(os.path.join(self.processed_data_path, 'y_test.pkl'))
            logger.info("Processed data loaded successfully.")
        except Exception as e:
            logger.error(f"Error loading processed data: {e}")
            raise CustomException(f"Error loading processed data: {e}", sys)
        
    def train_model(self):
        try:
            self.clf = LogisticRegression(random_state=42, max_iter=1000)
            self.clf.fit(self.X_train, self.y_train)

            joblib.dump(self.clf, os.path.join(self.model_output_path, 'logistic_regression_model.pkl'))
            logger.info("Model trained and saved successfully.")
        except Exception as e:
            logger.error(f"Error during model training: {e}")
            raise CustomException(f"Error during model training: {e}", sys)
    
    def evaluate_model(self):
            try:
                y_pred = self.clf.predict(self.X_test)
                accuracy = accuracy_score(self.y_test, y_pred)
                precision = precision_score(self.y_test, y_pred, average='weighted')
                recall = recall_score(self.y_test, y_pred, average='weighted')
                f1 = f1_score(self.y_test, y_pred, average='weighted')
                report = classification_report(self.y_test, y_pred)
                cm = confusion_matrix(self.y_test, y_pred)

                logger.info(f"Accuracy: {accuracy}")
                logger.info(f"Precision: {precision}")
                logger.info(f"Recall: {recall}")
                logger.info(f"F1 Score: {f1}")
                logger.info(f"Classification Report:\n{report}")
                logger.info(f"Confusion Matrix:\n{cm}")

                # Also print to console
                print(f"\n=== MODEL EVALUATION RESULTS ===")
                print(f"Accuracy: {accuracy:.4f}")
                print(f"Precision: {precision:.4f}")
                print(f"Recall: {recall:.4f}")
                print(f"F1 Score: {f1:.4f}")
                print(f"\nClassification Report:\n{report}")
                print(f"\nConfusion Matrix:\n{cm}")
                print("=" * 35)

                logger.info("Model evaluation completed successfully.")
            except Exception as e:
                logger.error(f"Error during model evaluation: {e}")
                raise CustomException(f"Error during model evaluation: {e}", sys)
    
    def run(self):
        self.load_processed_data()
        self.train_model()
        self.evaluate_model()

if __name__ == "__main__":
    trainer = ModelTraining(
        processed_data_path='artifacts/processed/',
        model_output_path='artifacts/model/'
    )
    trainer.run()
     

        
