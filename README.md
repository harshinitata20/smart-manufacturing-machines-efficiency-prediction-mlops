# 🏭 Smart Manufacturing Efficiency Predictor

[![CI/CD Pipeline](https://github.com/username/smart-manufacturing/workflows/CI/badge.svg)](https://github.com/username/smart-manufacturing/actions)
[![Test Coverage](https://img.shields.io/badge/coverage-85%25-green)](https://github.com/username/smart-manufacturing)
[![Docker](https://img.shields.io/badge/docker-ready-blue)](https://hub.docker.com/r/username/smart-manufacturing)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **An enterprise-grade MLOps solution for predicting manufacturing efficiency using machine learning with complete CI/CD pipeline, containerization, and automated deployment.**

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
- [Development](#-development)
- [CI/CD Pipeline](#-cicd-pipeline)
- [Model Information](#-model-information)
- [Project Structure](#-project-structure)
- [Contributing](#-contributing)
- [License](#-license)

## 🎯 Overview

The Smart Manufacturing Efficiency Predictor is a comprehensive machine learning solution that analyzes manufacturing data to predict operational efficiency. Built with MLOps best practices, it features automated training pipelines, containerized deployment, and a user-friendly web interface.

### Key Capabilities:
- **Real-time Efficiency Prediction**: Classify manufacturing operations as Low, Medium, or High efficiency
- **Web Interface**: Interactive dashboard for data input and prediction visualization
- **REST API**: RESTful endpoints for system integration
- **Automated ML Pipeline**: Complete data processing and model training automation
- **Production Ready**: Containerized with CI/CD pipeline and monitoring

## ✨ Features

### 🤖 Machine Learning
- **Logistic Regression Model** with 91.7% accuracy
- **14 Input Features**: Temperature, vibration, power consumption, network metrics, and more
- **Multi-class Classification**: Low/Medium/High efficiency prediction
- **Confidence Scoring**: Probability distribution for predictions

### 🌐 Web Application
- **Interactive Dashboard**: User-friendly interface for predictions
- **Real-time Results**: Instant prediction with confidence scores
- **Sample Data**: Pre-filled examples for testing
- **Responsive Design**: Works on desktop and mobile devices

### 🔧 MLOps Pipeline
- **Automated Training**: Scheduled model retraining
- **Data Processing**: Automated feature engineering and scaling
- **Model Validation**: Performance threshold enforcement
- **Version Control**: Model versioning and artifact management

### 🚀 Production Features
- **Docker Containerization**: Production-ready containers
- **Health Monitoring**: Application health endpoints
- **Logging**: Structured logging for monitoring
- **Security**: Vulnerability scanning and secure deployment

## ⚡ Quick Start

### Using Docker (Recommended)

```bash
# Clone the repository
git clone https://github.com/username/smart-manufacturing.git
cd smart-manufacturing

# Run with Docker Compose
docker-compose up -d

# Access the application
open http://localhost:5000
```

### Local Development

```bash
# Clone and setup
git clone https://github.com/username/smart-manufacturing.git
cd smart-manufacturing

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python application.py
```

## 🛠 Installation

### Prerequisites
- **Python 3.11+**
- **Docker** (optional, for containerized deployment)
- **Git**

### Step-by-Step Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/username/smart-manufacturing.git
   cd smart-manufacturing
   ```

2. **Setup Python Environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/Mac
   # or
   .venv\Scripts\activate     # Windows
   ```

3. **Install Dependencies**
   ```bash
   # Production dependencies
   pip install -r requirements-prod.txt
   
   # Development dependencies (optional)
   pip install -r requirements-dev.txt
   ```

4. **Run Training Pipeline** (First time setup)
   ```bash
   python pipeline/training_pipeline.py
   ```

5. **Start Application**
   ```bash
   python application.py
   ```

## 🎮 Usage

### Web Interface

1. **Open Browser**: Navigate to `http://localhost:5000`
2. **Fill Form**: Enter manufacturing parameters or use "Fill Sample Data"
3. **Get Prediction**: Click "Predict Efficiency" for instant results
4. **View Results**: See efficiency classification and confidence scores

### REST API

#### Health Check
```bash
curl http://localhost:5000/health
```

#### Make Prediction
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "Operation_Mode": 1,
    "Temperature_C": 75.5,
    "Vibration_Hz": 2.8,
    "Power_Consumption_kW": 5.2,
    "Network_Latency_ms": 15.3,
    "Packet_Loss_%": 1.2,
    "Quality_Control_Defect_Rate_%": 3.5,
    "Production_Speed_units_per_hr": 350.0,
    "Predictive_Maintenance_Score": 0.85,
    "Error_Rate_%": 5.2,
    "Year": 2024,
    "Month": 1,
    "Day": 1,
    "Hour": 12
  }'
```

## 📚 API Documentation

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Web interface |
| `POST` | `/predict` | Efficiency prediction API |
| `GET` | `/health` | Application health status |

### Request Format

All prediction requests require JSON with these 14 features:

```json
{
  "Operation_Mode": 0 or 1,           // 0=Idle, 1=Active
  "Temperature_C": float,             // Temperature in Celsius
  "Vibration_Hz": float,              // Vibration frequency
  "Power_Consumption_kW": float,      // Power consumption in kW
  "Network_Latency_ms": float,        // Network latency in ms
  "Packet_Loss_%": float,             // Packet loss percentage
  "Quality_Control_Defect_Rate_%": float, // QC defect rate
  "Production_Speed_units_per_hr": float, // Production speed
  "Predictive_Maintenance_Score": float,  // 0-1 maintenance score
  "Error_Rate_%": float,              // Error rate percentage
  "Year": int,                        // Year (e.g., 2024)
  "Month": int,                       // Month (1-12)
  "Day": int,                         // Day (1-31)
  "Hour": int                         // Hour (0-23)
}
```

### Response Format

```json
{
  "prediction": "Medium Efficiency",
  "confidence": 0.87,
  "class": 1,
  "probabilities": {
    "Low Efficiency": 0.05,
    "Medium Efficiency": 0.87,
    "High Efficiency": 0.08
  }
}
```

## 🔧 Development

### Project Setup

```bash
# Clone repository
git clone https://github.com/username/smart-manufacturing.git
cd smart-manufacturing

# Setup development environment
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install
```

### Running Tests

```bash
# Run all tests
python test_runner.py

# Run specific test suite
pytest tests/test_application.py -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

### Code Quality

```bash
# Format code
black src/ application.py

# Lint code
flake8 src/ application.py

# Type checking (if mypy is installed)
mypy src/
```

### Model Training

```bash
# Run complete training pipeline
python pipeline/training_pipeline.py

# Or run individual components
python src/data_processing.py
python src/model_training.py
```

## 🚀 CI/CD Pipeline

### GitHub Actions Workflows

- **🔄 CI/CD Pipeline** (`.github/workflows/ci-cd.yml`)
  - Code quality checks (Black, Flake8)
  - Automated testing with coverage
  - Security scanning with Trivy
  - Multi-platform Docker builds
  - Automated deployment

- **🤖 Model Retraining** (`.github/workflows/model-retrain.yml`)
  - Weekly scheduled retraining
  - Performance validation
  - Model versioning and releases

### Deployment

#### Docker Deployment
```bash
# Build and run locally
docker build -t smart-manufacturing .
docker run -p 5000:5000 smart-manufacturing

# Using deployment script
./deploy.sh
```

#### Kubernetes Deployment
```bash
# Apply Kubernetes manifests
kubectl apply -f k8s/
```

#### Docker Compose
```bash
# Production deployment
docker-compose up -d

# Development with hot-reload
docker-compose --profile dev up
```

## 🧠 Model Information

### Model Architecture
- **Algorithm**: Logistic Regression
- **Input Features**: 14 engineered features
- **Output Classes**: 3 (Low, Medium, High efficiency)
- **Training Data**: Manufacturing 6G dataset

### Performance Metrics
- **Accuracy**: 91.7%
- **Precision**: 91.6% (weighted avg)
- **Recall**: 91.7% (weighted avg)
- **F1-Score**: 91.6% (weighted avg)

### Model Features
1. `Operation_Mode` - Machine operation status
2. `Temperature_C` - Operating temperature
3. `Vibration_Hz` - Vibration frequency
4. `Power_Consumption_kW` - Power usage
5. `Network_Latency_ms` - Network performance
6. `Packet_Loss_%` - Network packet loss
7. `Quality_Control_Defect_Rate_%` - QC metrics
8. `Production_Speed_units_per_hr` - Production rate
9. `Predictive_Maintenance_Score` - Maintenance indicator
10. `Error_Rate_%` - System error rate
11. `Year` - Temporal feature
12. `Month` - Temporal feature
13. `Day` - Temporal feature
14. `Hour` - Temporal feature

## 📁 Project Structure

```
smart-manufacturing/
├── 📄 README.md                    # This file
├── 📄 requirements.txt             # Base dependencies
├── 📄 requirements-prod.txt        # Production dependencies
├── 📄 requirements-dev.txt         # Development dependencies
├── 📄 Dockerfile                   # Container definition
├── 📄 docker-compose.yml           # Multi-service orchestration
├── 📄 application.py               # Flask web application
├── 📄 setup.py                     # Package setup
├── 🔧 .github/workflows/           # CI/CD pipelines
│   ├── ci-cd.yml                   # Main CI/CD workflow
│   └── model-retrain.yml           # Model retraining workflow
├── 📁 src/                         # Source code
│   ├── data_processing.py          # Data preprocessing pipeline
│   ├── model_training.py           # ML model training
│   ├── logger.py                   # Logging configuration
│   └── exception.py                # Custom exceptions
├── 📁 pipeline/                    # ML pipelines
│   └── training_pipeline.py        # Complete training orchestration
├── 📁 tests/                       # Test suite
│   ├── test_application.py         # Flask app tests
│   ├── test_data_processing.py     # Data pipeline tests
│   └── test_model_training.py      # Model training tests
├── 📁 templates/                   # Web UI templates
│   └── index.html                  # Main web interface
├── 📁 artifacts/                   # Generated artifacts
│   ├── raw/                        # Raw datasets
│   ├── processed/                  # Processed data
│   └── model/                      # Trained models
└── 📁 logs/                        # Application logs
```

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the Repository**
2. **Create Feature Branch**: `git checkout -b feature/amazing-feature`
3. **Make Changes**: Implement your feature
4. **Run Tests**: `python test_runner.py`
5. **Commit Changes**: `git commit -m 'Add amazing feature'`
6. **Push Branch**: `git push origin feature/amazing-feature`
7. **Open Pull Request**

### Development Guidelines

- Follow PEP 8 style guidelines
- Maintain test coverage >80%
- Add tests for new features
- Update documentation
- Use meaningful commit messages

## 📊 Monitoring & Observability

### Health Checks
- **Application Health**: `/health` endpoint
- **Model Status**: Model loading verification
- **Dependencies**: Database and service connectivity

### Logging
- **Structured Logging**: JSON format for easy parsing
- **Log Levels**: DEBUG, INFO, WARNING, ERROR, CRITICAL
- **Request Tracing**: Request ID tracking

### Metrics
- **Prediction Latency**: Response time monitoring
- **Model Performance**: Accuracy tracking over time
- **System Resources**: CPU and memory usage

## 🔒 Security

### Security Features
- **Container Security**: Non-root user execution
- **Dependency Scanning**: Automated vulnerability detection
- **Input Validation**: Request parameter validation
- **Error Handling**: Secure error messages

### Security Practices
- Regular dependency updates
- Secrets management with environment variables
- HTTPS in production
- Access logging and monitoring

## 📈 Performance

### Optimization Features
- **Model Caching**: Pre-loaded models for fast inference
- **Response Compression**: Gzip compression for web responses
- **Connection Pooling**: Efficient database connections
- **Static Asset Optimization**: Minified CSS/JS

### Scaling
- **Horizontal Scaling**: Multi-container deployment
- **Load Balancing**: Nginx or cloud load balancer
- **Auto-scaling**: Kubernetes HPA support
- **Caching**: Redis for session and result caching

## 🆘 Troubleshooting

### Common Issues

**Model Not Loading**
```bash
# Check if artifacts exist
ls artifacts/model/
ls artifacts/processed/

# Retrain model
python pipeline/training_pipeline.py
```

**Port Already in Use**
```bash
# Find process using port 5000
lsof -i :5000  # Linux/Mac
netstat -ano | findstr :5000  # Windows

# Kill process or change port
export FLASK_PORT=5001  # Use different port
```

**Docker Issues**
```bash
# Check Docker status
docker ps
docker logs <container_id>

# Rebuild container
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/username/smart-manufacturing/issues)
- **Documentation**: [Project Wiki](https://github.com/username/smart-manufacturing/wiki)
- **Discussions**: [GitHub Discussions](https://github.com/username/smart-manufacturing/discussions)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Dataset**: Manufacturing 6G Dataset
- **ML Framework**: Scikit-learn
- **Web Framework**: Flask
- **Containerization**: Docker
- **CI/CD**: GitHub Actions

---

## 📊 Project Stats

![GitHub stars](https://img.shields.io/github/stars/username/smart-manufacturing?style=social)
![GitHub forks](https://img.shields.io/github/forks/username/smart-manufacturing?style=social)
![GitHub issues](https://img.shields.io/github/issues/username/smart-manufacturing)
![GitHub pull requests](https://img.shields.io/github/issues-pr/username/smart-manufacturing)

**Built with ❤️ for Smart Manufacturing**

> **Ready for production deployment with enterprise-grade MLOps practices!** 🚀