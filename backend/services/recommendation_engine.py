"""
Clinical Recommendation Engine
Generates personalized treatment recommendations based on patient biomarkers and disorder type
"""

class RecommendationEngine:
    """Engine for generating disorder-specific clinical recommendations"""
    
    # Configuration for recommendation thresholds
    THRESHOLDS = {
        'sleep': {
            'critical': 6.0,
            'high': 7.0,
            'optimal_min': 7.0,
            'optimal_max': 9.0
        },
        'hrv': {
            'severe': 0.75,  # 25% below baseline
            'moderate': 0.90  # 10% below baseline
        },
        'activity': {
            'severe': 0.50,  # 50% below goal
            'moderate': 0.70,  # 30% below goal
            'hyperactive': 1.30  # 30% above goal (mania warning)
        },
        'risk': {
            'critical': 75,
            'high': 66,
            'moderate': 33
        },
        'mood_variability': {
            'high': 25,  # 25% change
            'moderate': 20
        }
    }
    
    # Disorder-specific clinical configurations
    DISORDER_CONFIG = {
        'BIPOLAR': {
            'sleep_critical': True,
            'monitor_hyperactivity': True,
            'mood_swings_threshold': 20,
            'priority_symptoms': ['sleep', 'activity', 'mood']
        },
        'MDD': {
            'behavioral_activation': True,
            'combined_decline_alert': True,
            'priority_symptoms': ['mood', 'sleep', 'activity']
        },
        'PTSD': {
            'hrv_sensitivity': True,
            'nightmare_monitoring': True,
            'priority_symptoms': ['sleep', 'hrv']
        },
        'ANXIETY': {
            'hrv_biofeedback': True,
            'sleep_anxiety': True,
            'priority_symptoms': ['hrv', 'sleep']
        },
        'PANIC': {
            'hrv_biofeedback': True,
            'autonomic_focus': True,
            'priority_symptoms': ['hrv']
        },
        'OCD': {
            'erp_therapy': True,
            'priority_symptoms': ['mood']
        },
        'SCHIZOPHRENIA': {
            'sleep_monitoring': True,
            'negative_symptoms': True,
            'priority_symptoms': ['sleep', 'activity']
        },
        'BPD': {
            'dbt_focus': True,
            'safety_screening': True,
            'priority_symptoms': ['mood']
        },
        'SUBSTANCE': {
            'relapse_monitoring': True,
            'structure_focus': True,
            'priority_symptoms': ['sleep', 'activity']
        }
    }
    
    def generate_recommendations(self, patient, trends, avg_sleep, avg_hrv, avg_activity):
        """
        Generate comprehensive, personalized recommendations
        
        Args:
            patient: Patient model object
            trends: Dict of biomarker trends
            avg_sleep: Average sleep duration (hours)
            avg_hrv: Average heart rate variability (ms)
            avg_activity: Average daily steps
            
        Returns:
            List of recommendation dicts sorted by priority
        """
        recommendations = []
        
        # Get patient context
        disorder_type = self._get_disorder_type(patient)
        
        # 1. Critical Risk Recommendations (highest priority)
        recommendations.extend(self._get_risk_recommendations(patient))
        
        # 2. Sleep Recommendations
        recommendations.extend(self._get_sleep_recommendations(patient, avg_sleep, disorder_type))
        
        # 3. HRV Recommendations (autonomic nervous system)
        recommendations.extend(self._get_hrv_recommendations(patient, avg_hrv, disorder_type))
        
        # 4. Activity Recommendations
        recommendations.extend(self._get_activity_recommendations(patient, avg_activity, disorder_type))
        
        # 5. Disorder-Specific Recommendations
        recommendations.extend(self._get_disorder_specific_recommendations(
            patient, trends, avg_sleep, avg_hrv, avg_activity, disorder_type
        ))
        
        # 6. Medication Recommendations
        recommendations.extend(self._get_medication_recommendations(patient, trends))
        
        # 7. Positive Reinforcement
        recommendations.extend(self._get_positive_recommendations(patient, avg_sleep, avg_activity))
        
        # Sort by priority and limit to top recommendations
        priority_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        recommendations.sort(key=lambda x: priority_order.get(x['priority'], 4))
        
        return recommendations[:6]  # Return top 6 recommendations
    
    def _get_disorder_type(self, patient):
        """Extract and normalize disorder type"""
        disorder = patient.disorder.upper() if patient.disorder else ''
        disorder_full = patient.disorder_full.upper() if patient.disorder_full else ''
        
        # Map to standardized disorder categories
        if 'BIPOLAR' in disorder_full:
            return 'BIPOLAR'
        elif 'MDD' in disorder or 'DEPRESSIVE' in disorder_full:
            return 'MDD'
        elif 'PTSD' in disorder_full:
            return 'PTSD'
        elif 'ANXIETY' in disorder_full or 'GAD' in disorder:
            return 'ANXIETY'
        elif 'PANIC' in disorder_full:
            return 'PANIC'
        elif 'OCD' in disorder or 'OBSESSIVE' in disorder_full:
            return 'OCD'
        elif 'SCHIZOPHRENIA' in disorder_full:
            return 'SCHIZOPHRENIA'
        elif 'BORDERLINE' in disorder_full or disorder == 'BPD':
            return 'BPD'
        elif 'SUBSTANCE' in disorder_full or 'ALCOHOL' in disorder_full:
            return 'SUBSTANCE'
        elif 'SOCIAL ANXIETY' in disorder_full:
            return 'SOCIAL_ANXIETY'
        elif 'ADHD' in disorder_full:
            return 'ADHD'
        elif 'ANOREXIA' in disorder_full or 'EATING' in disorder_full:
            return 'EATING_DISORDER'
        else:
            return 'OTHER'
    
    # ============================================================================
    # RISK RECOMMENDATIONS
    # ============================================================================
    
    def _get_risk_recommendations(self, patient):
        """Generate risk-based recommendations"""
        recommendations = []
        
        if not patient.risk_score:
            return recommendations
        
        if patient.risk_score >= self.THRESHOLDS['risk']['critical']:
            recommendations.append({
                'type': 'risk',
                'priority': 'critical',
                'message': 'URGENT: Schedule immediate psychiatric evaluation',
                'reason': f'Critical risk score ({patient.risk_score:.0f}%) - immediate intervention required',
                'action': 'urgent_evaluation'
            })
        elif patient.risk_score >= self.THRESHOLDS['risk']['high']:
            recommendations.append({
                'type': 'risk',
                'priority': 'critical',
                'message': 'Schedule same-day follow-up visit',
                'reason': f'High risk score ({patient.risk_score:.0f}%) detected',
                'action': 'same_day_followup'
            })
        
        return recommendations
    
    # ============================================================================
    # SLEEP RECOMMENDATIONS
    # ============================================================================
    
    def _get_sleep_recommendations(self, patient, avg_sleep, disorder_type):
        """Generate sleep-related recommendations"""
        recommendations = []
        
        if avg_sleep < self.THRESHOLDS['sleep']['critical']:
            # Severe sleep deprivation - disorder-specific critical alerts
            if disorder_type == 'BIPOLAR':
                recommendations.append({
                    'type': 'sleep',
                    'priority': 'critical',
                    'message': 'URGENT: Address severe sleep deprivation - manic episode risk',
                    'reason': f'Sleep duration ({avg_sleep:.1f}h) critically low - major trigger for bipolar episodes',
                    'action': 'bipolar_sleep_crisis'
                })
            elif disorder_type == 'PTSD':
                recommendations.append({
                    'type': 'sleep',
                    'priority': 'high',
                    'message': 'Increase Prazosin dosage or add sleep medication',
                    'reason': f'Severe sleep disruption ({avg_sleep:.1f}h) - likely nightmares/hyperarousal',
                    'action': 'ptsd_medication_review'
                })
            else:
                recommendations.append({
                    'type': 'sleep',
                    'priority': 'critical',
                    'message': 'Immediate sleep intervention required',
                    'reason': f'Severe sleep deprivation ({avg_sleep:.1f}h) detected',
                    'action': 'sleep_intervention'
                })
                
        elif avg_sleep < self.THRESHOLDS['sleep']['high']:
            # Moderate sleep issues - disorder-specific interventions
            if disorder_type == 'MDD':
                recommendations.append({
                    'type': 'sleep',
                    'priority': 'high',
                    'message': 'Consider CBT-I referral or sleep hygiene intervention',
                    'reason': f'Sleep duration ({avg_sleep:.1f}h) below optimal - common in depression',
                    'action': 'cbti_referral'
                })
            elif disorder_type in ['ANXIETY', 'PANIC']:
                recommendations.append({
                    'type': 'sleep',
                    'priority': 'high',
                    'message': 'Address anxiety-related sleep disturbance',
                    'reason': f'Sleep duration ({avg_sleep:.1f}h) suggests anxiety interference',
                    'action': 'anxiety_sleep_treatment'
                })
            else:
                recommendations.append({
                    'type': 'sleep',
                    'priority': 'high',
                    'message': 'Consider sleep-focused CBT-I referral',
                    'reason': f'Average sleep duration ({avg_sleep:.1f}h) below recommended 7-8 hours',
                    'action': 'cbti_referral'
                })
        
        return recommendations
    
    # ============================================================================
    # HRV RECOMMENDATIONS
    # ============================================================================
    
    def _get_hrv_recommendations(self, patient, avg_hrv, disorder_type):
        """Generate HRV-related recommendations"""
        recommendations = []
        
        if not patient.wearable:
            return recommendations
        
        hrv_baseline = self._get_wearable_value(patient.wearable, 'hrv', 'baseline', 50)
        
        if avg_hrv < hrv_baseline * self.THRESHOLDS['hrv']['severe']:
            # Severe HRV reduction (>25% below baseline)
            if disorder_type == 'PTSD':
                recommendations.append({
                    'type': 'hrv',
                    'priority': 'high',
                    'message': 'Consider trauma-focused therapy intensification',
                    'reason': f'Very low HRV ({avg_hrv:.0f}ms) indicates high sympathetic activation - PTSD symptom exacerbation',
                    'action': 'trauma_therapy_intensify'
                })
            elif disorder_type in ['ANXIETY', 'PANIC']:
                recommendations.append({
                    'type': 'hrv',
                    'priority': 'high',
                    'message': 'Implement HRV biofeedback or relaxation training',
                    'reason': f'Low HRV ({avg_hrv:.0f}ms) suggests heightened anxiety state',
                    'action': 'hrv_biofeedback'
                })
            else:
                recommendations.append({
                    'type': 'hrv',
                    'priority': 'high',
                    'message': 'Review stress levels and medication timing',
                    'reason': f'HRV ({avg_hrv:.0f}ms) significantly below baseline ({hrv_baseline:.0f}ms) - high stress indicator',
                    'action': 'stress_review'
                })
                
        elif avg_hrv < hrv_baseline * self.THRESHOLDS['hrv']['moderate']:
            # Moderate HRV reduction
            recommendations.append({
                'type': 'hrv',
                'priority': 'medium',
                'message': 'Monitor stress and consider mindfulness interventions',
                'reason': f'HRV ({avg_hrv:.0f}ms) below baseline ({hrv_baseline:.0f}ms)',
                'action': 'mindfulness_intervention'
            })
        
        return recommendations
    
    # ============================================================================
    # ACTIVITY RECOMMENDATIONS
    # ============================================================================
    
    def _get_activity_recommendations(self, patient, avg_activity, disorder_type):
        """Generate activity-related recommendations"""
        recommendations = []
        
        if not patient.wearable:
            return recommendations
        
        steps_goal = self._get_wearable_value(patient.wearable, 'steps', 'goal', 10000)
        
        if avg_activity < steps_goal * self.THRESHOLDS['activity']['severe']:
            # Severe activity reduction
            if disorder_type == 'MDD':
                recommendations.append({
                    'type': 'activity',
                    'priority': 'high',
                    'message': 'Behavioral activation therapy recommended',
                    'reason': f'Severe activity reduction ({avg_activity:.0f} steps, {(avg_activity/steps_goal*100):.0f}% of goal) - key depression indicator',
                    'action': 'behavioral_activation'
                })
            elif disorder_type == 'SCHIZOPHRENIA':
                recommendations.append({
                    'type': 'activity',
                    'priority': 'high',
                    'message': 'Evaluate for negative symptoms and medication side effects',
                    'reason': f'Very low activity ({avg_activity:.0f} steps) may indicate amotivation or sedation',
                    'action': 'negative_symptom_eval'
                })
            else:
                recommendations.append({
                    'type': 'activity',
                    'priority': 'high',
                    'message': 'Urgent: Address severe mobility reduction',
                    'reason': f'Activity level ({avg_activity:.0f} steps) critically low - only {(avg_activity/steps_goal*100):.0f}% of goal',
                    'action': 'mobility_intervention'
                })
                
        elif avg_activity < steps_goal * self.THRESHOLDS['activity']['moderate']:
            # Moderate activity reduction
            recommendations.append({
                'type': 'activity',
                'priority': 'medium',
                'message': 'Encourage increased physical activity and exercise',
                'reason': f'Activity level ({avg_activity:.0f} steps) below goal ({steps_goal} steps)',
                'action': 'activity_increase'
            })
            
        elif disorder_type == 'BIPOLAR' and avg_activity > steps_goal * self.THRESHOLDS['activity']['hyperactive']:
            # Hyperactivity - potential manic episode
            recommendations.append({
                'type': 'activity',
                'priority': 'critical',
                'message': 'URGENT: Evaluate for manic/hypomanic episode',
                'reason': f'Unusually high activity ({avg_activity:.0f} steps, {(avg_activity/steps_goal*100):.0f}% of goal) - possible mania',
                'action': 'mania_evaluation'
            })
        
        return recommendations
    
    # ============================================================================
    # DISORDER-SPECIFIC RECOMMENDATIONS
    # ============================================================================
    
    def _get_disorder_specific_recommendations(self, patient, trends, avg_sleep, avg_hrv, avg_activity, disorder_type):
        """Route to disorder-specific recommendation methods"""
        if disorder_type == 'BIPOLAR':
            return self._bipolar_recommendations(patient, trends, avg_sleep, avg_activity)
        elif disorder_type == 'MDD':
            return self._mdd_recommendations(patient, trends, avg_sleep, avg_activity)
        elif disorder_type == 'PTSD':
            return self._ptsd_recommendations(patient, avg_sleep, avg_hrv)
        elif disorder_type in ['ANXIETY', 'PANIC']:
            return self._anxiety_recommendations(patient, avg_sleep, avg_hrv)
        elif disorder_type == 'OCD':
            return self._ocd_recommendations(patient)
        elif disorder_type == 'SCHIZOPHRENIA':
            return self._schizophrenia_recommendations(patient, avg_sleep, avg_activity)
        elif disorder_type == 'BPD':
            return self._bpd_recommendations(patient, trends)
        elif disorder_type == 'SUBSTANCE':
            return self._substance_recommendations(patient, avg_sleep, avg_activity)
        
        return []
    
    def _bipolar_recommendations(self, patient, trends, avg_sleep, avg_activity):
        """Bipolar disorder specific recommendations"""
        recommendations = []
        steps_goal = self._get_wearable_value(patient.wearable, 'steps', 'goal', 10000) if patient.wearable else 10000
        
        if avg_sleep < 6.5 or avg_activity > steps_goal * 1.2:
            recommendations.append({
                'type': 'disorder',
                'priority': 'high',
                'message': 'Monitor for manic/hypomanic symptoms',
                'reason': 'Sleep reduction and/or activity increase - early manic warning signs',
                'action': 'mania_monitoring'
            })
        
        if trends.get('mood') and abs(trends['mood'].get('percentChange', 0)) > self.THRESHOLDS['mood_variability']['moderate']:
            recommendations.append({
                'type': 'mood',
                'priority': 'high',
                'message': 'Mood stabilizer review recommended',
                'reason': f'Significant mood variability ({abs(trends["mood"]["percentChange"]):.0f}% change)',
                'action': 'mood_stabilizer_review'
            })
        
        return recommendations
    
    def _mdd_recommendations(self, patient, trends, avg_sleep, avg_activity):
        """Major Depressive Disorder specific recommendations"""
        recommendations = []
        steps_goal = self._get_wearable_value(patient.wearable, 'steps', 'goal', 10000) if patient.wearable else 10000
        
        if avg_sleep < 7 and avg_activity < steps_goal * 0.7:
            recommendations.append({
                'type': 'disorder',
                'priority': 'high',
                'message': 'Consider antidepressant adjustment or augmentation',
                'reason': 'Combined sleep and activity decline - treatment response concerns',
                'action': 'medication_adjustment'
            })
        
        if trends.get('mood') and trends['mood'].get('change', 0) < -5:
            recommendations.append({
                'type': 'mood',
                'priority': 'high',
                'message': 'Increase therapy frequency or consider medication change',
                'reason': 'Mood declining despite treatment',
                'action': 'treatment_intensification'
            })
        
        return recommendations
    
    def _ptsd_recommendations(self, patient, avg_sleep, avg_hrv):
        """PTSD specific recommendations"""
        recommendations = []
        
        if avg_sleep < 6.5:
            recommendations.append({
                'type': 'disorder',
                'priority': 'high',
                'message': 'Review nightmare frequency and Prazosin effectiveness',
                'reason': 'Poor sleep common with PTSD nightmares',
                'action': 'nightmare_treatment_review'
            })
        
        if patient.wearable:
            hrv_baseline = self._get_wearable_value(patient.wearable, 'hrv', 'baseline', 50)
            if avg_hrv < hrv_baseline * 0.85:
                recommendations.append({
                    'type': 'disorder',
                    'priority': 'medium',
                    'message': 'Consider EMDR or prolonged exposure therapy',
                    'reason': 'Low HRV suggests high hyperarousal - trauma processing may help',
                    'action': 'trauma_therapy'
                })
        
        return recommendations
    
    def _anxiety_recommendations(self, patient, avg_sleep, avg_hrv):
        """Anxiety/Panic disorder specific recommendations"""
        recommendations = []
        
        if patient.wearable:
            hrv_baseline = self._get_wearable_value(patient.wearable, 'hrv', 'baseline', 50)
            if avg_hrv < hrv_baseline * 0.9:
                recommendations.append({
                    'type': 'disorder',
                    'priority': 'medium',
                    'message': 'Teach diaphragmatic breathing and HRV biofeedback',
                    'reason': 'Low HRV indicates autonomic dysregulation common in anxiety',
                    'action': 'breathing_training'
                })
        
        if avg_sleep < 7:
            recommendations.append({
                'type': 'disorder',
                'priority': 'medium',
                'message': 'Address sleep anxiety with CBT techniques',
                'reason': 'Sleep disturbance perpetuates anxiety cycle',
                'action': 'cbt_sleep_anxiety'
            })
        
        return recommendations
    
    def _ocd_recommendations(self, patient):
        """OCD specific recommendations"""
        recommendations = []
        
        if patient.risk_score and patient.risk_score > 55:
            recommendations.append({
                'type': 'disorder',
                'priority': 'high',
                'message': 'Intensify ERP (Exposure Response Prevention) therapy',
                'reason': 'Elevated risk suggests symptom exacerbation',
                'action': 'erp_intensify'
            })
        
        return recommendations
    
    def _schizophrenia_recommendations(self, patient, avg_sleep, avg_activity):
        """Schizophrenia specific recommendations"""
        recommendations = []
        
        if avg_sleep < 6 or avg_sleep > 10:
            recommendations.append({
                'type': 'disorder',
                'priority': 'high',
                'message': 'Monitor for psychotic symptom changes',
                'reason': 'Sleep irregularity can trigger symptom relapse',
                'action': 'psychotic_symptom_monitoring'
            })
        
        steps_goal = self._get_wearable_value(patient.wearable, 'steps', 'goal', 10000) if patient.wearable else 10000
        if avg_activity < steps_goal * 0.6:
            recommendations.append({
                'type': 'disorder',
                'priority': 'medium',
                'message': 'Assess for negative symptoms and medication side effects',
                'reason': 'Low activity may indicate amotivation or sedation',
                'action': 'negative_symptom_assessment'
            })
        
        return recommendations
    
    def _bpd_recommendations(self, patient, trends):
        """Borderline Personality Disorder specific recommendations"""
        recommendations = []
        
        if patient.risk_score and patient.risk_score > 60:
            recommendations.append({
                'type': 'disorder',
                'priority': 'high',
                'message': 'Check for self-harm ideation and DBT skills use',
                'reason': 'Elevated risk in BPD - safety assessment needed',
                'action': 'safety_assessment'
            })
        
        if trends.get('mood') and abs(trends['mood'].get('percentChange', 0)) > self.THRESHOLDS['mood_variability']['high']:
            recommendations.append({
                'type': 'mood',
                'priority': 'medium',
                'message': 'Review emotion regulation DBT skills',
                'reason': 'High mood variability - core BPD symptom',
                'action': 'dbt_skills_review'
            })
        
        return recommendations
    
    def _substance_recommendations(self, patient, avg_sleep, avg_activity):
        """Substance Use Disorder specific recommendations"""
        recommendations = []
        
        if avg_sleep < 6.5:
            recommendations.append({
                'type': 'disorder',
                'priority': 'high',
                'message': 'Screen for substance use relapse',
                'reason': 'Poor sleep is both trigger and sign of relapse',
                'action': 'relapse_screening'
            })
        
        steps_goal = self._get_wearable_value(patient.wearable, 'steps', 'goal', 10000) if patient.wearable else 10000
        if avg_activity < steps_goal * 0.7:
            recommendations.append({
                'type': 'disorder',
                'priority': 'medium',
                'message': 'Encourage support group attendance and structured activities',
                'reason': 'Low activity increases relapse risk - need structure',
                'action': 'structure_intervention'
            })
        
        return recommendations
    
    # ============================================================================
    # MEDICATION RECOMMENDATIONS
    # ============================================================================
    
    def _get_medication_recommendations(self, patient, trends):
        """Generate medication-related recommendations"""
        recommendations = []
        
        # Get medications
        medications = self._get_patient_medications(patient)
        
        # Check for adherence concerns based on sudden biomarker changes
        if trends.get('sleep') and abs(trends['sleep'].get('percentChange', 0)) > 15:
            recommendations.append({
                'type': 'medication',
                'priority': 'medium',
                'message': 'Verify medication adherence',
                'reason': 'Sudden biomarker changes may indicate missed doses',
                'action': 'adherence_check'
            })
        
        # Lithium-specific monitoring for bipolar
        if any('lithium' in str(med).lower() for med in medications):
            if patient.wearable:
                steps_goal = self._get_wearable_value(patient.wearable, 'steps', 'goal', 10000)
                avg_activity = self._get_wearable_value(patient.wearable, 'steps', 'avg', 0)
                
                if avg_activity > steps_goal * 1.3:
                    recommendations.append({
                        'type': 'medication',
                        'priority': 'high',
                        'message': 'Check lithium levels - possible breakthrough mania',
                        'reason': 'Increased activity despite lithium treatment',
                        'action': 'lithium_level_check'
                    })
        
        return recommendations
    
    # ============================================================================
    # POSITIVE REINFORCEMENT
    # ============================================================================
    
    def _get_positive_recommendations(self, patient, avg_sleep, avg_activity):
        """Generate positive reinforcement recommendations"""
        recommendations = []
        
        sleep_optimal = (self.THRESHOLDS['sleep']['optimal_min'] <= avg_sleep <= 
                        self.THRESHOLDS['sleep']['optimal_max'])
        
        if sleep_optimal and patient.wearable:
            steps_goal = self._get_wearable_value(patient.wearable, 'steps', 'goal', 10000)
            if avg_activity >= steps_goal * 0.9:
                recommendations.append({
                    'type': 'positive',
                    'priority': 'low',
                    'message': 'Excellent sleep and activity patterns - continue current routine',
                    'reason': 'Maintaining healthy behaviors supports mental health stability',
                    'action': 'continue_routine'
                })
        
        return recommendations
    
    # ============================================================================
    # UTILITY METHODS
    # ============================================================================
    
    def _get_wearable_value(self, wearable, category, key, default):
        """Safely get wearable data value"""
        if isinstance(wearable, dict):
            return wearable.get(category, {}).get(key, default)
        else:
            # Handle SQLAlchemy model
            if category == 'hrv':
                return getattr(wearable, 'hrv_baseline', default) if key == 'baseline' else default
            elif category == 'steps':
                return getattr(wearable, 'steps_goal', default) if key == 'goal' else getattr(wearable, 'steps_avg', default)
            return default
    
    def _get_patient_medications(self, patient):
        """Safely get patient medications"""
        if patient.ehr and isinstance(patient.ehr, dict):
            return patient.ehr.get('medications', [])
        elif patient.ehr:
            return getattr(patient.ehr, 'medications', [])
        return []
