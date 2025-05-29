# ml_model/train_model.py
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle

# Sample symptom-disease mapping data
data = {
    'symptom': ['fever', 'cough', 'headache', 'sore throat', 'fatigue', 
                'nausea', 'chest pain', 'shortness of breath', 'dizziness'],
    'disease': ['flu', 'flu', 'migraine', 'strep throat', 'anemia',
                'food poisoning', 'heart disease', 'asthma', 'vertigo']
}

# Create all possible symptom combinations
symptoms = data['symptom']
diseases = data['disease']

# Generate feature vectors and labels
X = []
y = []

for i, disease in enumerate(diseases):
    # Create feature vector for each disease with its main symptom
    features = [1 if symptom == symptoms[i] else 0 for symptom in symptoms]
    X.append(features)
    y.append(disease)
    
    # Add some variations with additional symptoms
    for j in range(len(symptoms)):
        if j != i:
            new_features = features.copy()
            new_features[j] = 1
            X.append(new_features)
            y.append(disease)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Save model
with open('ml_model/model.pkl', 'wb') as f:
    pickle.dump(model, f)

# Save symptoms list
symptoms_df = pd.DataFrame({'symptom': symptoms})
symptoms_df.to_csv('ml_model/symptoms.csv', index=False)

print("Model trained and saved successfully!")