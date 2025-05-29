from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_login import login_user, current_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from cryptography.fernet import Fernet
from extensions import db, login_manager
from models import User, Symptom, Diagnosis
import pandas as pd
import pickle
import bcrypt
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///healthcare.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Encryption key
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Load ML model
with open('ml_model/model.pkl', 'rb') as f:
    model = pickle.load(f)

# Sample symptoms data
symptoms_df = pd.read_csv('ml_model/symptoms.csv')
SYMPTOMS = symptoms_df['symptom'].tolist()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('symptoms'))
        
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        
        user = User.query.filter_by(email=email).first()
        
        if user and bcrypt.checkpw(password, user.password):
            login_user(user)
            session['is_admin'] = user.is_admin
            flash('Login successful!', 'success')
            return redirect(url_for('symptoms'))
        else:
            flash('Invalid email or password', 'danger')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('symptoms'))
        
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'danger')
            return redirect(url_for('register'))
        
        hashed = bcrypt.hashpw(password, bcrypt.gensalt())
        new_user = User(name=name, email=email, password=hashed)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/symptoms', methods=['GET', 'POST'])
@login_required
def symptoms():
    if request.method == 'POST':
        symptoms = request.form.getlist('symptoms')
        additional_info = request.form['additional_info']
        
        if not symptoms:
            flash('Please select at least one symptom', 'warning')
            return redirect(url_for('symptoms'))
        
        try:
            # Encrypt and save symptoms
            encrypted_symptoms = cipher_suite.encrypt(','.join(symptoms).encode())
            encrypted_info = cipher_suite.encrypt(additional_info.encode())
            
            new_symptom = Symptom(
                user_id=current_user.id,
                symptoms=encrypted_symptoms,
                additional_info=encrypted_info
            )
            db.session.add(new_symptom)
            db.session.commit()
            
            # Predict diagnosis
            diagnosis_result = predict_diagnosis(symptoms)
            
            # Encrypt and save diagnosis
            encrypted_result = cipher_suite.encrypt(diagnosis_result.encode())
            new_diagnosis = Diagnosis(
                symptom_id=new_symptom.id,
                result=encrypted_result
            )
            db.session.add(new_diagnosis)
            db.session.commit()
            
            return redirect(url_for('results', diagnosis_id=new_diagnosis.id))
        except Exception as e:
            db.session.rollback()
            flash('Error saving your diagnosis. Please try again.', 'danger')
            return redirect(url_for('symptoms'))
    
    return render_template('symptoms.html', symptoms=SYMPTOMS)


def predict_diagnosis(symptoms):
    # Create feature vector
    features = [1 if symptom in symptoms else 0 for symptom in SYMPTOMS]
    
    # Predict
    prediction = model.predict([features])[0]
    probability = model.predict_proba([features])[0].max()
    
    return f"{prediction} (confidence: {probability:.2%})"

@app.route('/results/<int:diagnosis_id>')
@login_required
def results(diagnosis_id):
    try:
        diagnosis = Diagnosis.query.get_or_404(diagnosis_id)
        if diagnosis.symptom.user_id != current_user.id and not current_user.is_admin:
            flash('You are not authorized to view this diagnosis', 'danger')
            return redirect(url_for('symptoms'))
        
        result = cipher_suite.decrypt(diagnosis.result).decode()
        return render_template('results.html', result=result)
    except Exception as e:
        flash('Error loading diagnosis results. Please try again.', 'danger')
        return redirect(url_for('symptoms'))
    

@app.route('/history')
@login_required
def history():
    try:
        user_symptoms = Symptom.query.filter_by(user_id=current_user.id)\
                          .order_by(Symptom.created_at.desc()).all()
        history = []
        
        for symptom in user_symptoms:
            diagnosis = Diagnosis.query.filter_by(symptom_id=symptom.id).first()
            if diagnosis:
                try:
                    result = cipher_suite.decrypt(diagnosis.result).decode()
                    symptoms = cipher_suite.decrypt(symptom.symptoms).decode()
                    history.append({
                        'date': symptom.created_at.strftime('%Y-%m-%d %H:%M'),
                        'result': result,
                        'symptoms': symptoms.split(',')
                    })
                except Exception as e:
                    continue
        
        return render_template('history.html', history=history)
    except Exception as e:
        flash('Error loading history. Please try again.', 'danger')
        return redirect(url_for('symptoms'))
    

@app.route('/admin')
@login_required
def admin():
    if not current_user.is_admin:
        flash('You are not authorized to access this page', 'danger')
        return redirect(url_for('symptoms'))
    
    # Get stats
    total_users = User.query.count()
    total_diagnoses = Diagnosis.query.count()
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    
    return render_template('admin.html', 
                         total_users=total_users,
                         total_diagnoses=total_diagnoses,
                         recent_users=recent_users)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('home'))

@app.route('/about')
def about():
    return render_template('about.html')

# Add these new routes to your existing app.py

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/medical-resources')
@login_required
def medical_resources():
    return render_template('medical_resources.html')

@app.route('/health-tracking')
@login_required
def tracking():
    return render_template('tracking.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)