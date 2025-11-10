"""
Test script to demonstrate the Clinical Recommendation Engine
Shows disorder-specific, personalized recommendations based on patient biomarkers
"""

from services.recommendation_engine import RecommendationEngine

# Mock patient class for testing
class MockWearable:
    def __init__(self, hrv_baseline, steps_goal):
        self.hrv_baseline = hrv_baseline
        self.steps_goal = steps_goal

class MockEHR:
    def __init__(self, medications):
        self.medications = medications

class MockPatient:
    def __init__(self, name, disorder, disorder_full, risk_score, wearable=None, ehr=None):
        self.name = name
        self.disorder = disorder
        self.disorder_full = disorder_full
        self.risk_score = risk_score
        self.wearable = wearable
        self.ehr = ehr

# Create test scenarios
scenarios = [
    {
        'name': 'Patient A - Bipolar w/ Sleep Crisis',
        'patient': MockPatient(
            name='Sarah Martinez',
            disorder='BD',
            disorder_full='Bipolar I Disorder',
            risk_score=72,
            wearable=MockWearable(hrv_baseline=55, steps_goal=10000),
            ehr=MockEHR(medications=['Lithium', 'Lamotrigine'])
        ),
        'trends': {
            'sleep': {'change': -2.8, 'percentChange': -35, 'current': 5.2, 'previous': 8.0},
            'hrv': {'change': -5, 'percentChange': -10, 'current': 50, 'previous': 55},
            'activity': {'change': 3500, 'percentChange': 45, 'current': 11200, 'previous': 7700},
            'mood': {'change': 15, 'percentChange': 22, 'current': 8.2, 'previous': 6.7}
        },
        'avg_sleep': 5.2,
        'avg_hrv': 50,
        'avg_activity': 11200
    },
    {
        'name': 'Patient B - MDD w/ Low Activity',
        'patient': MockPatient(
            name='John Williams',
            disorder='MDD',
            disorder_full='Major Depressive Disorder',
            risk_score=58,
            wearable=MockWearable(hrv_baseline=48, steps_goal=10000),
            ehr=MockEHR(medications=['Sertraline', 'Bupropion'])
        ),
        'trends': {
            'sleep': {'change': -1.2, 'percentChange': -17, 'current': 5.8, 'previous': 7.0},
            'hrv': {'change': -3, 'percentChange': -6, 'current': 45, 'previous': 48},
            'activity': {'change': -4200, 'percentChange': -42, 'current': 5800, 'previous': 10000},
            'mood': {'change': -8, 'percentChange': -12, 'current': 5.5, 'previous': 6.3}
        },
        'avg_sleep': 5.8,
        'avg_hrv': 45,
        'avg_activity': 5800
    },
    {
        'name': 'Patient C - PTSD w/ Nightmares',
        'patient': MockPatient(
            name='Maria Garcia',
            disorder='PTSD',
            disorder_full='Post-Traumatic Stress Disorder',
            risk_score=65,
            wearable=MockWearable(hrv_baseline=52, steps_goal=8000),
            ehr=MockEHR(medications=['Prazosin', 'Sertraline'])
        ),
        'trends': {
            'sleep': {'change': -2.1, 'percentChange': -30, 'current': 4.9, 'previous': 7.0},
            'hrv': {'change': -15, 'percentChange': -29, 'current': 37, 'previous': 52},
            'activity': {'change': -1200, 'percentChange': -15, 'current': 6800, 'previous': 8000},
            'mood': {'change': -5, 'percentChange': -8, 'current': 5.8, 'previous': 6.3}
        },
        'avg_sleep': 4.9,
        'avg_hrv': 37,
        'avg_activity': 6800
    },
    {
        'name': 'Patient D - Anxiety w/ Good Progress',
        'patient': MockPatient(
            name='Emily Chen',
            disorder='GAD',
            disorder_full='Generalized Anxiety Disorder',
            risk_score=28,
            wearable=MockWearable(hrv_baseline=58, steps_goal=10000),
            ehr=MockEHR(medications=['Escitalopram'])
        ),
        'trends': {
            'sleep': {'change': 0.5, 'percentChange': 7, 'current': 7.5, 'previous': 7.0},
            'hrv': {'change': 2, 'percentChange': 3, 'current': 60, 'previous': 58},
            'activity': {'change': 500, 'percentChange': 5, 'current': 10500, 'previous': 10000},
            'mood': {'change': 3, 'percentChange': 5, 'current': 7.2, 'previous': 6.9}
        },
        'avg_sleep': 7.5,
        'avg_hrv': 60,
        'avg_activity': 10500
    },
    {
        'name': 'Patient E - Schizophrenia w/ Negative Symptoms',
        'patient': MockPatient(
            name='David Johnson',
            disorder='SCZ',
            disorder_full='Schizophrenia',
            risk_score=52,
            wearable=MockWearable(hrv_baseline=45, steps_goal=8000),
            ehr=MockEHR(medications=['Risperidone', 'Benztropine'])
        ),
        'trends': {
            'sleep': {'change': 2.5, 'percentChange': 35, 'current': 9.5, 'previous': 7.0},
            'hrv': {'change': -2, 'percentChange': -4, 'current': 43, 'previous': 45},
            'activity': {'change': -3500, 'percentChange': -44, 'current': 4500, 'previous': 8000},
            'mood': {'change': -2, 'percentChange': -3, 'current': 6.0, 'previous': 6.2}
        },
        'avg_sleep': 9.5,
        'avg_hrv': 43,
        'avg_activity': 4500
    }
]

def print_recommendations(scenario):
    """Print formatted recommendations for a scenario"""
    engine = RecommendationEngine()
    
    print(f"\n{'='*80}")
    print(f"🏥 {scenario['name']}")
    print(f"{'='*80}")
    print(f"Disorder: {scenario['patient'].disorder_full}")
    print(f"Risk Score: {scenario['patient'].risk_score}%")
    print()
    
    # Print biomarker summary
    print("📊 Biomarker Summary:")
    print(f"  Sleep:    {scenario['avg_sleep']:.1f}h (Δ {scenario['trends']['sleep']['change']:+.1f}h, {scenario['trends']['sleep']['percentChange']:+.0f}%)")
    print(f"  HRV:      {scenario['avg_hrv']:.0f}ms (Δ {scenario['trends']['hrv']['change']:+.0f}ms, {scenario['trends']['hrv']['percentChange']:+.0f}%)")
    print(f"  Activity: {scenario['avg_activity']:.0f} steps (Δ {scenario['trends']['activity']['change']:+.0f} steps, {scenario['trends']['activity']['percentChange']:+.0f}%)")
    print()
    
    # Generate recommendations
    recommendations = engine.generate_recommendations(
        scenario['patient'],
        scenario['trends'],
        scenario['avg_sleep'],
        scenario['avg_hrv'],
        scenario['avg_activity']
    )
    
    # Print recommendations
    print(f"💡 Clinical Recommendations ({len(recommendations)} total):")
    print()
    
    priority_icons = {
        'critical': '🚨',
        'high': '⚠️',
        'medium': '📋',
        'low': '✅'
    }
    
    for i, rec in enumerate(recommendations, 1):
        icon = priority_icons.get(rec['priority'], '•')
        print(f"{i}. {icon} [{rec['priority'].upper()}] {rec['type'].upper()}")
        print(f"   Message: {rec['message']}")
        print(f"   Reason:  {rec['reason']}")
        if 'action' in rec:
            print(f"   Action:  {rec['action']}")
        print()

# Run tests
print("\n" + "="*80)
print("🧠 PHENOMIND CLINICAL RECOMMENDATION ENGINE - DEMONSTRATION")
print("="*80)
print("Showing personalized, disorder-specific recommendations")
print()

for scenario in scenarios:
    print_recommendations(scenario)

print("="*80)
print("✅ DEMONSTRATION COMPLETE")
print("="*80)
print()
print("Key Features Demonstrated:")
print("  ✓ Disorder-specific recommendations")
print("  ✓ Dynamic risk-based prioritization")
print("  ✓ Biomarker trend analysis")
print("  ✓ Medication monitoring (e.g., lithium levels)")
print("  ✓ Positive reinforcement for good adherence")
print("  ✓ Clinical action codes for workflow integration")
print()
