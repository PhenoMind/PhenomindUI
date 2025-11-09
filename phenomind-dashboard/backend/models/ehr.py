from database import db

class EHR(db.Model):
    __tablename__ = 'ehr'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False, unique=True)
    diagnosis = db.Column(db.Text, nullable=False)
    diagnosis_date = db.Column(db.String(50))
    comorbidities = db.Column(db.JSON)  # List of strings
    medications = db.Column(db.JSON)  # List of medication objects
    allergies = db.Column(db.JSON)  # List of strings
    blood_pressure = db.Column(db.String(20))
    bmi = db.Column(db.Float)
    last_lab_work = db.Column(db.String(50))
    notes = db.Column(db.Text)
    
    def to_dict(self):
        return {
            'diagnosis': self.diagnosis,
            'diagnosisDate': self.diagnosis_date,
            'comorbidities': self.comorbidities or [],
            'medications': self.medications or [],
            'allergies': self.allergies or [],
            'bloodPressure': self.blood_pressure,
            'bmi': self.bmi,
            'lastLabWork': self.last_lab_work,
            'notes': self.notes
        }
    
    def __repr__(self):
        return f'<EHR for Patient {self.patient_id}>'

