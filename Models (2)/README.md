# Oral Cancer Detection Web Application

A web application for detecting oral cancer using machine learning models with a user-friendly interface.

## Features

- Upload and analyze oral tissue images
- AI-powered detection of potential oral cancer
- Confidence scoring and detailed results
- Responsive design for use on various devices
- Educational resources about oral cancer

## Requirements

- Python 3.8 or higher
- Flask web framework
- Machine learning libraries (NumPy, TensorFlow, etc.)
- Web browser

## Installation

1. Clone the repository or download the source code.

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up the application:
   ```
   cd oral_cancer_detection_app
   ```

## Running the Application

Start the development server:

```
python app.py
```

Access the application in your web browser at:
```
http://127.0.0.1:8080
```

## Integrating the Real Model

Currently, the application uses a placeholder model that generates random predictions. To integrate the real oral cancer detection model:

1. Extract the model code from the Jupyter notebooks (`oral_cancer_detection_pso.ipynb` or `oral_cancer_detection_AI_Biruni.ipynb`).

2. Update the `models/model_interface.py` file to load and use your trained model.

3. Implement proper preprocessing of images to match the model's input requirements.

## Deployment

For production deployment:

1. Use a production WSGI server like Gunicorn:
   ```
   gunicorn app:app -b 0.0.0.0:8080
   ```

2. Consider deploying on cloud platforms like:
   - Heroku
   - AWS Elastic Beanstalk
   - Google Cloud Run
   - Microsoft Azure

## Project Structure

```
oral_cancer_detection_app/
├── app.py                  # Main Flask application
├── models/                 # Model-related code
│   ├── __init__.py
│   └── model_interface.py  # Interface to ML models
├── static/                 # Static assets
│   └── css/
│       └── style.css       # Custom CSS
├── templates/              # HTML templates
│   ├── index.html          # Home page
│   └── about.html          # About page
├── uploads/                # Directory for uploaded images
└── requirements.txt        # Python dependencies
```

## Important Notes

- This application is for educational and research purposes only
- It should not be used as a replacement for professional medical diagnosis
- Always consult healthcare professionals for medical concerns