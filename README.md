# MediAI Healthcare Diagnosis Assistant

MediAI is a Flask application that uses a trained Random Forest model to provide preliminary, symptom-based health information. It includes user accounts, diagnosis history, health tracking, medical resources, and an administrative dashboard.

> **Medical disclaimer:** This educational project does not provide medical advice, diagnosis, or treatment. Its output must not replace consultation with a qualified healthcare professional.

## Features

- Symptom-based machine-learning predictions
- Registration, login, and protected user workflows
- Diagnosis history and health tracking
- Medical resources and informational pages
- Administrative overview

## Technology

- Python and Flask
- Flask-SQLAlchemy and Flask-Login
- pandas and scikit-learn
- SQLite
- Bootstrap-based templates

## Local setup

```bash
git clone https://github.com/Nabiha-Nabz/healthcare_diagnosis.git
cd healthcare_diagnosis
python -m venv .venv
```

Activate the environment, then run:

```bash
pip install -r requirements.txt
python app.py
```

The application starts at `http://127.0.0.1:5000`.

## Model

The trained model is stored at `ml_model/model.pkl`. To rebuild it from the included symptom data, run:

```bash
python ml_model/train_model.py
```

## Responsible use

Do not use this project for emergency decisions, clinical deployment, or handling real patient data without professional review, validation, privacy controls, and applicable regulatory compliance.
