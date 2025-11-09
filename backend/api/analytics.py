from flask import Blueprint, jsonify
from models import Patient
from services.analytics_service import AnalyticsService

analytics_bp = Blueprint('analytics', __name__)
analytics_service = AnalyticsService()

@analytics_bp.route('/patients/<int:patient_id>/analytics', methods=['GET'])
def get_patient_analytics(patient_id):
    """Get analytics for a specific patient"""
    try:
        patient = Patient.query.get_or_404(patient_id)
        analytics = analytics_service.calculate_patient_analytics(patient)
        return jsonify(analytics)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@analytics_bp.route('/analytics/population', methods=['GET'])
def get_population_analytics():
    """Get population-level analytics"""
    patients = Patient.query.all()
    
    analytics = analytics_service.calculate_population_analytics(patients)
    
    return jsonify(analytics)

@analytics_bp.route('/analytics/risk-distribution', methods=['GET'])
def get_risk_distribution():
    """Get risk score distribution across all patients"""
    patients = Patient.query.all()
    
    distribution = analytics_service.calculate_risk_distribution(patients)
    
    return jsonify(distribution)

@analytics_bp.route('/analytics/disorder-breakdown', methods=['GET'])
def get_disorder_breakdown():
    """Get breakdown by disorder type"""
    patients = Patient.query.all()
    
    breakdown = analytics_service.calculate_disorder_breakdown(patients)
    
    return jsonify(breakdown)

