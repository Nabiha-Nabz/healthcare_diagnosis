#Healthcare Diagnosis System

Python
Flask
License

A full-stack web application designed to assist users in diagnosing common health conditions based on symptoms using machine learning. It integrates a secure and user-friendly interface with a trained Random Forest model to deliver accurate and fast medical insights.
Features

    🩺 AI-powered symptom analysis and diagnosis

    🔐 Secure user authentication with bcrypt encryption

    📊 Health metrics tracking and visualization

    📝 Medical history recording

    🔍 Comprehensive medical resources

    👨‍⚕️ Admin dashboard for system management

Prerequisites

Before you begin, ensure you have met the following requirements:

    Python 3.9 or higher installed

    pip package manager

    MySQL or SQLite database

    Git (optional)

    Installation

Follow these steps to set up the project:

    Clone the repository (or download the source code):

bash

git clone https://github.com/yourusername/healthcare_diagnosis.git
cd healthcare_diagnosis

    Create and activate a virtual environment (recommended):

bash

python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

    Install dependencies:

bash

pip install -r requirements.txt

    Set up the database:

bash

python -c "from app import app, db; with app.app_context(): db.create_all()"

    Train the machine learning model:

bash

python train_model.py

Configuration

Create a .env file in the project root with the following environment variables:
ini

SECRET_KEY=your_secret_key_here
DATABASE_URI=sqlite:///healthcare.db  # or your MySQL URI

Running the Application

To start the development server:
bash

python app.py

For production deployment, use Gunicorn:
bash

gunicorn -w 4 -b 0.0.0.0:5000 app:app

The application will be available at http://localhost:5000.

Project Structure

healthcare_diagnosis/
├── app.py                # Main application entry point
├── models.py             # Database models
├── extensions.py         # Flask extensions initialization
├── train_model.py        # Machine learning model training script
├── requirements.txt      # Python dependencies
├── .env                  # Environment configuration
├── static/               # Static files (CSS, JS, images)
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── index.html        # Home page
│   ├── login.html        # Login page
│   ├── register.html     # Registration page
│   ├── symptoms.html     # Symptom input page
│   ├── results.html      # Diagnosis results page
│   ├── history.html      # Medical history page
│   ├── admin.html        # Admin dashboard
│   ├── about.html        # About page
│   ├── contact.html      # Contact page
│   ├── services.html     # Services page
│   ├── tracking.html     # Health tracking page
│   └── medical_resources.html # Resources page
└── ml_model/
    ├── model.pkl         # Trained ML model
    └── symptoms.csv      # List of symptoms


Usage

    Register a new account or log in with existing credentials

    Select symptoms from the comprehensive list

    Add any additional information about your condition

    Submit to receive an AI-powered diagnosis

    View your diagnosis history in the dashboard

    Track health metrics over time in the tracking section

Admin Features

Admin users (with is_admin=True in the database) can access:

    User management

    System statistics

    Diagnosis overview

Deployment

For production deployment, consider:

    Using a production-grade WSGI server like Gunicorn or uWSGI

    Setting up a reverse proxy with Nginx or Apache

    Using a proper database like MySQL or PostgreSQL

    Configuring proper SSL/TLS encryption

    Setting up monitoring and logging

Contributing

Contributions are welcome! Please follow these steps:

    Fork the repository

    Create a new branch (git checkout -b feature-branch)

    Commit your changes (git commit -am 'Add new feature')

    Push to the branch (git push origin feature-branch)

    Create a new Pull Request

License

This project is licensed under the MIT License - see the LICENSE file for details.
Disclaimer

This application provides preliminary health information and is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.
