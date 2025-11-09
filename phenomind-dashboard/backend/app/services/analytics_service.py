from collections import defaultdict
import statistics

class AnalyticsService:
    """Service for calculating analytics and insights"""
    
    def calculate_patient_analytics(self, patient):
        """Calculate comprehensive analytics for a single patient"""
        trend_data = patient.trend_data.all()
        
        if not trend_data:
            return {
                'riskScore': patient.risk_score or 0,
                'trends': {},
                'recommendations': []
            }
        
        # Calculate 7-day averages
        recent_data = list(trend_data[-7:]) if len(trend_data) >= 7 else list(trend_data)
        
        avg_sleep = statistics.mean([d.sleep for d in recent_data]) if recent_data else 0
        avg_hrv = statistics.mean([d.hrv for d in recent_data]) if recent_data else 0
        avg_activity = statistics.mean([d.activity for d in recent_data]) if recent_data else 0
        avg_mood = statistics.mean([d.mood for d in recent_data]) if recent_data else 0
        
        # Calculate trends (comparing last 7 days to previous 7 days)
        trends = {}
        if len(trend_data) >= 14:
            prev_data = list(trend_data[-14:-7])
            curr_data = recent_data
            
            prev_sleep = statistics.mean([d.sleep for d in prev_data])
            trends['sleep'] = {
                'current': avg_sleep,
                'previous': prev_sleep,
                'change': avg_sleep - prev_sleep,
                'percentChange': ((avg_sleep - prev_sleep) / prev_sleep * 100) if prev_sleep > 0 else 0
            }
            
            prev_hrv = statistics.mean([d.hrv for d in prev_data])
            trends['hrv'] = {
                'current': avg_hrv,
                'previous': prev_hrv,
                'change': avg_hrv - prev_hrv,
                'percentChange': ((avg_hrv - prev_hrv) / prev_hrv * 100) if prev_hrv > 0 else 0
            }
            
            prev_activity = statistics.mean([d.activity for d in prev_data])
            trends['activity'] = {
                'current': avg_activity,
                'previous': prev_activity,
                'change': avg_activity - prev_activity,
                'percentChange': ((avg_activity - prev_activity) / prev_activity * 100) if prev_activity > 0 else 0
            }
        
        # Generate recommendations based on data
        recommendations = self._generate_recommendations(patient, trends, avg_sleep, avg_hrv, avg_activity)
        
        return {
            'riskScore': patient.risk_score or 0,
            'averages': {
                'sleep': round(avg_sleep, 1),
                'hrv': round(avg_hrv, 0),
                'activity': round(avg_activity, 0),
                'mood': round(avg_mood, 1)
            },
            'trends': trends,
            'recommendations': recommendations,
            'biomarkerDrivers': self._identify_biomarker_drivers(patient, trends)
        }
    
    def calculate_population_analytics(self, patients):
        """Calculate population-level analytics"""
        if not patients:
            return {}
        
        total_patients = len(patients)
        high_risk = sum(1 for p in patients if p.risk_score and p.risk_score >= 66)
        moderate_risk = sum(1 for p in patients if p.risk_score and 33 <= p.risk_score < 66)
        low_risk = sum(1 for p in patients if p.risk_score and p.risk_score < 33)
        
        avg_risk_score = statistics.mean([p.risk_score for p in patients if p.risk_score]) if any(p.risk_score for p in patients) else 0
        
        return {
            'totalPatients': total_patients,
            'riskDistribution': {
                'high': high_risk,
                'moderate': moderate_risk,
                'low': low_risk
            },
            'averageRiskScore': round(avg_risk_score, 1),
            'highRiskPercentage': round((high_risk / total_patients * 100), 1) if total_patients > 0 else 0
        }
    
    def calculate_risk_distribution(self, patients):
        """Calculate detailed risk score distribution"""
        risk_scores = [p.risk_score for p in patients if p.risk_score is not None]
        
        if not risk_scores:
            return {}
        
        return {
            'min': min(risk_scores),
            'max': max(risk_scores),
            'mean': round(statistics.mean(risk_scores), 1),
            'median': round(statistics.median(risk_scores), 1),
            'stdDev': round(statistics.stdev(risk_scores), 1) if len(risk_scores) > 1 else 0
        }
    
    def calculate_disorder_breakdown(self, patients):
        """Breakdown patients by disorder type"""
        disorder_counts = defaultdict(lambda: {'total': 0, 'highRisk': 0, 'moderateRisk': 0, 'lowRisk': 0})
        
        for patient in patients:
            disorder = patient.disorder_full
            disorder_counts[disorder]['total'] += 1
            
            if patient.risk_score:
                if patient.risk_score >= 66:
                    disorder_counts[disorder]['highRisk'] += 1
                elif patient.risk_score >= 33:
                    disorder_counts[disorder]['moderateRisk'] += 1
                else:
                    disorder_counts[disorder]['lowRisk'] += 1
        
        return {
            'breakdown': [
                {
                    'disorder': disorder,
                    'totalPatients': counts['total'],
                    'highRisk': counts['highRisk'],
                    'moderateRisk': counts['moderateRisk'],
                    'lowRisk': counts['lowRisk']
                }
                for disorder, counts in disorder_counts.items()
            ]
        }
    
    def _generate_recommendations(self, patient, trends, avg_sleep, avg_hrv, avg_activity):
        """Generate personalized recommendations based on patient data"""
        recommendations = []
        
        # Sleep recommendations
        if avg_sleep < 7:
            recommendations.append({
                'type': 'sleep',
                'priority': 'high',
                'message': 'Consider sleep-focused CBT-I referral',
                'reason': f'Average sleep duration ({avg_sleep:.1f}h) is below recommended 7-8 hours'
            })
        
        # HRV recommendations
        if patient.wearable and avg_hrv < patient.wearable.hrv_baseline * 0.9:
            recommendations.append({
                'type': 'hrv',
                'priority': 'medium',
                'message': 'Review HRV and medication timing',
                'reason': f'HRV ({avg_hrv:.0f}ms) is below baseline ({patient.wearable.hrv_baseline}ms)'
            })
        
        # Activity recommendations
        if patient.wearable and avg_activity < patient.wearable.steps_goal * 0.7:
            recommendations.append({
                'type': 'activity',
                'priority': 'medium',
                'message': 'Encourage increased physical activity',
                'reason': f'Activity level ({avg_activity:.0f} steps) is below goal ({patient.wearable.steps_goal} steps)'
            })
        
        # High risk recommendations
        if patient.risk_score and patient.risk_score >= 66:
            recommendations.append({
                'type': 'risk',
                'priority': 'critical',
                'message': 'Schedule immediate follow-up visit',
                'reason': f'High risk score ({patient.risk_score:.0f}%) detected'
            })
        
        return recommendations
    
    def _identify_biomarker_drivers(self, patient, trends):
        """Identify primary drivers of risk based on biomarker changes"""
        drivers = []
        
        if trends.get('sleep') and trends['sleep']['change'] < -0.5:
            drivers.append({
                'factor': 'Sleep irregularity',
                'importance': 0.38,
                'trend': 'decreasing'
            })
        
        if trends.get('hrv') and trends['hrv']['change'] < -2:
            drivers.append({
                'factor': 'HRV ↓',
                'importance': 0.29,
                'trend': 'decreasing'
            })
        
        if trends.get('activity') and trends['activity']['change'] < -500:
            drivers.append({
                'factor': 'Mobility ↓',
                'importance': 0.21,
                'trend': 'decreasing'
            })
        
        return drivers

