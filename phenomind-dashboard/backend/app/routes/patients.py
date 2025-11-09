from flask import Blueprint, jsonify, request
from app import db
from app.models import Patient

patients_bp = Blueprint('patients', __name__)

@patients_bp.route('/patients', methods=['GET'])
def get_patients():
    """Get all patients with optional search filter"""
    try:
        search_query = request.args.get('search', '').lower()
        
        patients = Patient.query.all()
        
        if search_query:
            patients = [
                p for p in patients 
                if search_query in p.name.lower() 
                or search_query in p.disorder.lower()
                or search_query in p.disorder_full.lower()
            ]
        
        return jsonify([patient.to_dict() for patient in patients])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@patients_bp.route('/patients/<int:patient_id>', methods=['GET'])
def get_patient(patient_id):
    """Get a specific patient by ID"""
    patient = Patient.query.get_or_404(patient_id)
    return jsonify(patient.to_dict())

@patients_bp.route('/patients', methods=['POST'])
def create_patient():
    """Create a new patient"""
    data = request.get_json()
    
    patient = Patient(
        name=data['name'],
        age=data['age'],
        gender=data['gender'],
        avatar=data.get('avatar'),
        initials=data.get('initials'),
        disorder=data['disorder'],
        disorder_full=data['disorderFull'],
        medications=data.get('medications', []),
        last_visit=data.get('lastVisit'),
        risk_score=data.get('riskScore')
    )
    
    db.session.add(patient)
    db.session.commit()
    
    return jsonify(patient.to_dict()), 201

@patients_bp.route('/patients/<int:patient_id>', methods=['PUT'])
def update_patient(patient_id):
    """Update a patient"""
    patient = Patient.query.get_or_404(patient_id)
    data = request.get_json()
    
    if 'name' in data:
        patient.name = data['name']
    if 'age' in data:
        patient.age = data['age']
    if 'riskScore' in data:
        patient.risk_score = data['riskScore']
    if 'medications' in data:
        patient.medications = data['medications']
    if 'lastVisit' in data:
        patient.last_visit = data['lastVisit']
    
    db.session.commit()
    
    return jsonify(patient.to_dict())

@patients_bp.route('/patients/<int:patient_id>', methods=['DELETE'])
def delete_patient(patient_id):
    """Delete a patient"""
    patient = Patient.query.get_or_404(patient_id)
    db.session.delete(patient)
    db.session.commit()
    
    return jsonify({'message': 'Patient deleted'}), 200

