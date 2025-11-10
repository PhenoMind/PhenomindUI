from collections import defaultdict
import statistics
from .recommendation_engine import RecommendationEngine

class AnalyticsService:
    """Service for calculating analytics and insights"""
    
    def __init__(self):
        self.recommendation_engine = RecommendationEngine()
    
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
            
            prev_mood = statistics.mean([d.mood for d in prev_data])
            trends['mood'] = {
                'current': avg_mood,
                'previous': prev_mood,
                'change': avg_mood - prev_mood,
                'percentChange': ((avg_mood - prev_mood) / prev_mood * 100) if prev_mood > 0 else 0
            }
        
        # Generate recommendations using the recommendation engine
        recommendations = self.recommendation_engine.generate_recommendations(
            patient, trends, avg_sleep, avg_hrv, avg_activity
        )
        
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
    
    def _identify_biomarker_drivers(self, patient, trends):
        """Identify primary drivers of risk based on biomarker changes with dynamic weighting"""
        drivers = []
        
        # Calculate the magnitude of change for each biomarker
        sleep_change = abs(trends.get('sleep', {}).get('change', 0)) if trends.get('sleep') else 0
        hrv_change = abs(trends.get('hrv', {}).get('change', 0)) if trends.get('hrv') else 0
        activity_change = abs(trends.get('activity', {}).get('change', 0)) if trends.get('activity') else 0
        
        # Normalize changes to percentage of baseline to make them comparable
        sleep_percent_change = abs(trends.get('sleep', {}).get('percentChange', 0)) if trends.get('sleep') else 0
        hrv_percent_change = abs(trends.get('hrv', {}).get('percentChange', 0)) if trends.get('hrv') else 0
        activity_percent_change = abs(trends.get('activity', {}).get('percentChange', 0)) if trends.get('activity') else 0
        
        # Add severity multipliers for clinically significant changes
        sleep_severity = 1.0
        if sleep_change > 2.0:  # Lost more than 2 hours of sleep
            sleep_severity = 1.5
        elif sleep_change > 1.0:  # Lost more than 1 hour
            sleep_severity = 1.2
        
        hrv_severity = 1.0
        if hrv_change > 10:  # HRV dropped by more than 10ms
            hrv_severity = 1.4
        elif hrv_change > 5:  # HRV dropped by more than 5ms
            hrv_severity = 1.2
        
        activity_severity = 1.0
        if activity_change > 3000:  # Lost more than 3000 steps
            activity_severity = 1.3
        elif activity_change > 1500:  # Lost more than 1500 steps
            activity_severity = 1.15
        
        # Apply severity multipliers to percent changes
        weighted_sleep = sleep_percent_change * sleep_severity
        weighted_hrv = hrv_percent_change * hrv_severity
        weighted_activity = activity_percent_change * activity_severity
        
        # Calculate total weighted change to determine relative importance
        total_weighted_change = weighted_sleep + weighted_hrv + weighted_activity
        
        # Only calculate drivers if there are meaningful changes
        if total_weighted_change > 0:
            # Sleep driver - dynamically weighted based on relative change
            if trends.get('sleep') and trends['sleep']['change'] < -0.5:
                # Importance is proportional to how much this metric changed relative to others
                importance = min((weighted_sleep / total_weighted_change), 0.85)  # Cap at 0.85
                drivers.append({
                    'factor': 'Sleep irregularity',
                    'importance': round(importance, 2),
                    'impact': round(importance, 2),
                    'trend': 'decreasing',
                    'direction': 'decreasing',
                    'change': trends['sleep']['change'],
                    'percentChange': sleep_percent_change
                })
            
            # HRV driver - dynamically weighted
            if trends.get('hrv') and trends['hrv']['change'] < -2:
                importance = min((weighted_hrv / total_weighted_change), 0.85)
                drivers.append({
                    'factor': 'HRV ↓',
                    'importance': round(importance, 2),
                    'impact': round(importance, 2),
                    'trend': 'decreasing',
                    'direction': 'decreasing',
                    'change': trends['hrv']['change'],
                    'percentChange': hrv_percent_change
                })
            
            # Activity driver - dynamically weighted
            if trends.get('activity') and trends['activity']['change'] < -500:
                importance = min((weighted_activity / total_weighted_change), 0.85)
                drivers.append({
                    'factor': 'Mobility ↓',
                    'importance': round(importance, 2),
                    'impact': round(importance, 2),
                    'trend': 'decreasing',
                    'direction': 'decreasing',
                    'change': trends['activity']['change'],
                    'percentChange': activity_percent_change
                })
        else:
            # Fallback to static weights if no trends available
            if trends.get('sleep') and trends['sleep']['change'] < -0.5:
                drivers.append({
                    'factor': 'Sleep irregularity',
                    'importance': 0.38,
                    'impact': 0.38,
                    'trend': 'decreasing',
                    'direction': 'decreasing'
                })
            
            if trends.get('hrv') and trends['hrv']['change'] < -2:
                drivers.append({
                    'factor': 'HRV ↓',
                    'importance': 0.29,
                    'impact': 0.29,
                    'trend': 'decreasing',
                    'direction': 'decreasing'
                })
            
            if trends.get('activity') and trends['activity']['change'] < -500:
                drivers.append({
                    'factor': 'Mobility ↓',
                    'importance': 0.21,
                    'impact': 0.21,
                    'trend': 'decreasing',
                    'direction': 'decreasing'
                })
        
        # Sort by importance (highest first)
        drivers.sort(key=lambda x: x['importance'], reverse=True)
        
        return drivers

