"""
Script to migrate patient data from patientData.js to the database
Run this after setting up the database: python migrate_data.py
"""
import sys
import os

# Add parent directory to path to import patientData
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import create_app, db
from app.models import Patient, EHR, Wearable, TimelineEvent, TrendData

# Import the patient data
# Note: This requires the patientData.js to be converted or we'll read it directly
# For now, we'll create a Python version of the data

def generate_trend_data(base_mood, base_sleep, base_hrv, base_activity, mood_trend, sleep_trend, hrv_trend, activity_trend):
    """Generate trend data for a patient (matches JS generateTrendData function)"""
    import math
    from datetime import datetime, timedelta
    
    days = []
    for i in range(30):
        d = datetime.now() - timedelta(days=(29 - i))
        days.append(d.strftime("%b %d"))
    
    trend_data = []
    for i, day in enumerate(days):
        trend_data.append({
            'day': day,
            'mood': max(0, min(100, base_mood + math.sin(i / 4) * 10 + (mood_trend * i / 30))),
            'sleep': max(4, min(10, base_sleep + math.sin(i / 5) * 0.6 + (sleep_trend * i / 30))),
            'hrv': max(20, min(80, base_hrv + math.cos(i / 6) * 8 + (hrv_trend * i / 30))),
            'activity': max(2000, base_activity + math.sin(i / 3) * 1500 + (activity_trend * i / 30))
        })
    
    return trend_data

# Patient data (from patientData.js) - All 12 patients
PATIENTS_DATA = [
    {
        'id': 1, 'name': 'Jane Doe', 'age': 34, 'gender': 'Female',
        'avatar': 'https://i.pravatar.cc/100?img=5', 'initials': 'JD',
        'disorder': 'MDD', 'disorderFull': 'Major Depressive Disorder',
        'medications': ['Sertraline 75mg'], 'lastVisit': '10 days ago', 'riskScore': 58,
        'ehr': {
            'diagnosis': 'Major Depressive Disorder, Recurrent, Moderate',
            'diagnosisDate': '2023-08-15',
            'comorbidities': ['Generalized Anxiety Disorder'],
            'medications': [
                {'name': 'Sertraline', 'dose': '75mg', 'frequency': 'Daily', 'startDate': '2024-01-10'},
                {'name': 'Lorazepam', 'dose': '0.5mg', 'frequency': 'As needed', 'startDate': '2024-02-01'}
            ],
            'allergies': ['Penicillin'],
            'bloodPressure': '118/72', 'bmi': 24.3,
            'lastLabWork': '2024-03-15',
            'notes': 'Patient reports improved mood with current medication regimen. Continue monitoring.'
        },
        'wearables': {
            'device': 'Apple Watch Series 9', 'lastSync': '2 hours ago',
            'heartRate': {'avg': 72, 'resting': 65, 'max': 145},
            'steps': {'avg': 6120, 'goal': 10000},
            'sleep': {'avg': 6.3, 'goal': 8, 'quality': 'Fair'},
            'hrv': {'avg': 42, 'baseline': 50},
            'activity': {'activeMinutes': 45, 'calories': 1850}
        },
        'timeline': [
            {'date': 'Apr 3', 'label': 'Medication dose ↑ (Sertraline 50→75mg)', 'type': 'med'},
            {'date': 'Apr 6', 'label': 'Sleep irregularity detected (avg 5.8h; baseline 7.1h)', 'type': 'alert'},
            {'date': 'Apr 10', 'label': 'PHQ-9 via app: 12 (↑2)', 'type': 'survey'},
            {'date': 'Apr 13', 'label': 'Reduced mobility (−32% steps vs baseline)', 'type': 'alert'},
            {'date': 'Apr 15', 'label': 'Televisit completed; therapy referral placed', 'type': 'visit'}
        ],
        'trendParams': (60, 7, 45, 7000, -6, -0.8, -6, -2200)
    },
    {
        'id': 2, 'name': 'Michael Chen', 'age': 28, 'gender': 'Male',
        'avatar': 'https://i.pravatar.cc/100?img=12', 'initials': 'MC',
        'disorder': 'Bipolar I', 'disorderFull': 'Bipolar I Disorder',
        'medications': ['Lithium 900mg', 'Olanzapine 10mg'], 'lastVisit': '5 days ago', 'riskScore': 72,
        'ehr': {
            'diagnosis': 'Bipolar I Disorder, Most Recent Episode Manic',
            'diagnosisDate': '2022-11-20',
            'comorbidities': ['ADHD'],
            'medications': [
                {'name': 'Lithium', 'dose': '900mg', 'frequency': 'Daily', 'startDate': '2022-11-25'},
                {'name': 'Olanzapine', 'dose': '10mg', 'frequency': 'Daily', 'startDate': '2023-03-10'},
                {'name': 'Adderall', 'dose': '20mg', 'frequency': 'Daily', 'startDate': '2023-06-01'}
            ],
            'allergies': ['None known'],
            'bloodPressure': '125/80', 'bmi': 26.1,
            'lastLabWork': '2024-04-01',
            'notes': 'Lithium levels within therapeutic range (0.8 mEq/L). Monitor for manic symptoms.'
        },
        'wearables': {
            'device': 'Fitbit Charge 6', 'lastSync': '30 minutes ago',
            'heartRate': {'avg': 78, 'resting': 70, 'max': 165},
            'steps': {'avg': 12400, 'goal': 10000},
            'sleep': {'avg': 5.2, 'goal': 8, 'quality': 'Poor'},
            'hrv': {'avg': 35, 'baseline': 45},
            'activity': {'activeMinutes': 120, 'calories': 2850}
        },
        'timeline': [
            {'date': 'Apr 1', 'label': 'Lithium level check: 0.8 mEq/L (therapeutic)', 'type': 'med'},
            {'date': 'Apr 4', 'label': 'Sleep duration ↓ (4.8h; baseline 7.5h)', 'type': 'alert'},
            {'date': 'Apr 7', 'label': 'Activity spike detected (+85% steps)', 'type': 'alert'},
            {'date': 'Apr 9', 'label': 'YMRS score: 18 (↑6)', 'type': 'survey'},
            {'date': 'Apr 12', 'label': 'In-person visit: Manic symptoms noted', 'type': 'visit'}
        ],
        'trendParams': (45, 5.2, 35, 12400, 8, -2.3, -10, 3500)
    },
    {
        'id': 3, 'name': 'Sarah Williams', 'age': 41, 'gender': 'Female',
        'avatar': 'https://i.pravatar.cc/100?img=47', 'initials': 'SW',
        'disorder': 'PTSD', 'disorderFull': 'Post-Traumatic Stress Disorder',
        'medications': ['Sertraline 100mg', 'Prazosin 2mg'], 'lastVisit': '14 days ago', 'riskScore': 45,
        'ehr': {
            'diagnosis': 'Post-Traumatic Stress Disorder, Chronic',
            'diagnosisDate': '2021-05-10',
            'comorbidities': ['Insomnia', 'Depression'],
            'medications': [
                {'name': 'Sertraline', 'dose': '100mg', 'frequency': 'Daily', 'startDate': '2021-05-15'},
                {'name': 'Prazosin', 'dose': '2mg', 'frequency': 'At bedtime', 'startDate': '2022-01-20'},
                {'name': 'Trazodone', 'dose': '50mg', 'frequency': 'At bedtime', 'startDate': '2023-08-01'}
            ],
            'allergies': ['Sulfa drugs'],
            'bloodPressure': '122/75', 'bmi': 22.8,
            'lastLabWork': '2024-03-20',
            'notes': 'Patient responding well to trauma-focused therapy. Nightmares reduced with Prazosin.'
        },
        'wearables': {
            'device': 'Garmin Venu 3', 'lastSync': '1 hour ago',
            'heartRate': {'avg': 68, 'resting': 58, 'max': 140},
            'steps': {'avg': 8900, 'goal': 10000},
            'sleep': {'avg': 7.8, 'goal': 8, 'quality': 'Good'},
            'hrv': {'avg': 52, 'baseline': 48},
            'activity': {'activeMinutes': 60, 'calories': 2100}
        },
        'timeline': [
            {'date': 'Mar 28', 'label': 'EMDR therapy session completed', 'type': 'visit'},
            {'date': 'Apr 2', 'label': 'Sleep quality improved (nightmares ↓)', 'type': 'med'},
            {'date': 'Apr 5', 'label': 'PCL-5 score: 28 (↓5 from baseline)', 'type': 'survey'},
            {'date': 'Apr 8', 'label': 'HRV trending upward (+8%)', 'type': 'alert'},
            {'date': 'Apr 11', 'label': 'Regular therapy attendance maintained', 'type': 'visit'}
        ],
        'trendParams': (70, 7.8, 52, 8900, -3, 0.5, 4, -500)
    },
    {
        'id': 4, 'name': 'David Rodriguez', 'age': 52, 'gender': 'Male',
        'avatar': 'https://i.pravatar.cc/100?img=33', 'initials': 'DR',
        'disorder': 'GAD', 'disorderFull': 'Generalized Anxiety Disorder',
        'medications': ['Escitalopram 20mg', 'Buspirone 15mg'], 'lastVisit': '7 days ago', 'riskScore': 38,
        'ehr': {
            'diagnosis': 'Generalized Anxiety Disorder, Severe',
            'diagnosisDate': '2020-09-12',
            'comorbidities': ['Hypertension', 'Type 2 Diabetes'],
            'medications': [
                {'name': 'Escitalopram', 'dose': '20mg', 'frequency': 'Daily', 'startDate': '2020-09-15'},
                {'name': 'Buspirone', 'dose': '15mg', 'frequency': 'Twice daily', 'startDate': '2021-02-10'},
                {'name': 'Metformin', 'dose': '1000mg', 'frequency': 'Twice daily', 'startDate': '2019-03-01'},
                {'name': 'Lisinopril', 'dose': '10mg', 'frequency': 'Daily', 'startDate': '2018-11-05'}
            ],
            'allergies': ['None known'],
            'bloodPressure': '135/88', 'bmi': 29.4,
            'lastLabWork': '2024-04-05',
            'notes': 'Anxiety well-controlled. Continue current medications. Monitor blood pressure.'
        },
        'wearables': {
            'device': 'Samsung Galaxy Watch 6', 'lastSync': '15 minutes ago',
            'heartRate': {'avg': 75, 'resting': 68, 'max': 150},
            'steps': {'avg': 7200, 'goal': 8000},
            'sleep': {'avg': 6.8, 'goal': 8, 'quality': 'Fair'},
            'hrv': {'avg': 48, 'baseline': 50},
            'activity': {'activeMinutes': 35, 'calories': 1950}
        },
        'timeline': [
            {'date': 'Mar 30', 'label': 'GAD-7 score: 8 (↓3)', 'type': 'survey'},
            {'date': 'Apr 3', 'label': 'Blood pressure check: 135/88', 'type': 'med'},
            {'date': 'Apr 6', 'label': 'Sleep duration stable (6.8h)', 'type': 'alert'},
            {'date': 'Apr 9', 'label': 'Therapy session: CBT techniques reviewed', 'type': 'visit'},
            {'date': 'Apr 12', 'label': 'Activity level maintained', 'type': 'alert'}
        ],
        'trendParams': (75, 6.8, 48, 7200, -2, -0.2, -2, -300)
    },
    {
        'id': 5, 'name': 'Emily Thompson', 'age': 29, 'gender': 'Female',
        'avatar': 'https://i.pravatar.cc/100?img=20', 'initials': 'ET',
        'disorder': 'OCD', 'disorderFull': 'Obsessive-Compulsive Disorder',
        'medications': ['Fluoxetine 40mg', 'Clomipramine 75mg'], 'lastVisit': '3 days ago', 'riskScore': 52,
        'ehr': {
            'diagnosis': 'Obsessive-Compulsive Disorder, Severe',
            'diagnosisDate': '2022-03-18',
            'comorbidities': ['Depression'],
            'medications': [
                {'name': 'Fluoxetine', 'dose': '40mg', 'frequency': 'Daily', 'startDate': '2022-03-25'},
                {'name': 'Clomipramine', 'dose': '75mg', 'frequency': 'Daily', 'startDate': '2023-01-15'},
                {'name': 'Risperidone', 'dose': '1mg', 'frequency': 'Daily', 'startDate': '2023-09-10'}
            ],
            'allergies': ['None known'],
            'bloodPressure': '115/70', 'bmi': 23.1,
            'lastLabWork': '2024-03-28',
            'notes': 'Patient showing improvement with ERP therapy. Medication compliance good.'
        },
        'wearables': {
            'device': 'Oura Ring Gen 3', 'lastSync': '45 minutes ago',
            'heartRate': {'avg': 70, 'resting': 62, 'max': 135},
            'steps': {'avg': 8500, 'goal': 8000},
            'sleep': {'avg': 7.2, 'goal': 8, 'quality': 'Good'},
            'hrv': {'avg': 46, 'baseline': 44},
            'activity': {'activeMinutes': 55, 'calories': 2000}
        },
        'timeline': [
            {'date': 'Mar 25', 'label': 'Y-BOCS score: 18 (↓4)', 'type': 'survey'},
            {'date': 'Mar 28', 'label': 'ERP therapy session completed', 'type': 'visit'},
            {'date': 'Apr 1', 'label': 'Sleep quality improved', 'type': 'alert'},
            {'date': 'Apr 5', 'label': 'Medication compliance: 100%', 'type': 'med'},
            {'date': 'Apr 8', 'label': 'Follow-up visit scheduled', 'type': 'visit'}
        ],
        'trendParams': (65, 7.2, 46, 8500, -3, 0.3, 2, 200)
    },
    {
        'id': 6, 'name': 'James Wilson', 'age': 35, 'gender': 'Male',
        'avatar': 'https://i.pravatar.cc/100?img=15', 'initials': 'JW',
        'disorder': 'Schizophrenia', 'disorderFull': 'Schizophrenia, Paranoid Type',
        'medications': ['Risperidone 4mg', 'Aripiprazole 15mg'], 'lastVisit': '2 days ago', 'riskScore': 68,
        'ehr': {
            'diagnosis': 'Schizophrenia, Paranoid Type',
            'diagnosisDate': '2020-06-22',
            'comorbidities': ['Substance Use Disorder (in remission)'],
            'medications': [
                {'name': 'Risperidone', 'dose': '4mg', 'frequency': 'Daily', 'startDate': '2020-06-25'},
                {'name': 'Aripiprazole', 'dose': '15mg', 'frequency': 'Daily', 'startDate': '2023-05-12'},
                {'name': 'Benztropine', 'dose': '1mg', 'frequency': 'Twice daily', 'startDate': '2020-07-01'}
            ],
            'allergies': ['None known'],
            'bloodPressure': '128/82', 'bmi': 27.8,
            'lastLabWork': '2024-04-02',
            'notes': 'Patient stable on current medications. No recent psychotic episodes. Monitor for extrapyramidal symptoms.'
        },
        'wearables': {
            'device': 'Fitbit Sense 2', 'lastSync': '1 hour ago',
            'heartRate': {'avg': 76, 'resting': 68, 'max': 155},
            'steps': {'avg': 6800, 'goal': 7000},
            'sleep': {'avg': 6.5, 'goal': 8, 'quality': 'Fair'},
            'hrv': {'avg': 38, 'baseline': 42},
            'activity': {'activeMinutes': 40, 'calories': 1750}
        },
        'timeline': [
            {'date': 'Mar 29', 'label': 'PANSS score: 42 (stable)', 'type': 'survey'},
            {'date': 'Apr 2', 'label': 'Medication compliance check: Good', 'type': 'med'},
            {'date': 'Apr 5', 'label': 'Sleep duration ↓ (6.2h)', 'type': 'alert'},
            {'date': 'Apr 8', 'label': 'Case management visit completed', 'type': 'visit'},
            {'date': 'Apr 10', 'label': 'No positive symptoms reported', 'type': 'alert'}
        ],
        'trendParams': (50, 6.5, 38, 6800, 2, -0.5, -4, -500)
    },
    {
        'id': 7, 'name': 'Olivia Martinez', 'age': 26, 'gender': 'Female',
        'avatar': 'https://i.pravatar.cc/100?img=32', 'initials': 'OM',
        'disorder': 'BPD', 'disorderFull': 'Borderline Personality Disorder',
        'medications': ['Lamotrigine 100mg', 'Quetiapine 50mg'], 'lastVisit': '6 days ago', 'riskScore': 65,
        'ehr': {
            'diagnosis': 'Borderline Personality Disorder',
            'diagnosisDate': '2021-11-08',
            'comorbidities': ['Depression', 'Substance Use Disorder'],
            'medications': [
                {'name': 'Lamotrigine', 'dose': '100mg', 'frequency': 'Twice daily', 'startDate': '2021-11-15'},
                {'name': 'Quetiapine', 'dose': '50mg', 'frequency': 'At bedtime', 'startDate': '2022-04-20'},
                {'name': 'Naltrexone', 'dose': '50mg', 'frequency': 'Daily', 'startDate': '2023-02-10'}
            ],
            'allergies': ['Sulfa drugs'],
            'bloodPressure': '120/75', 'bmi': 21.5,
            'lastLabWork': '2024-03-25',
            'notes': 'Patient engaged in DBT therapy. Emotional regulation improving. Monitor for self-harm behaviors.'
        },
        'wearables': {
            'device': 'Whoop 4.0', 'lastSync': '20 minutes ago',
            'heartRate': {'avg': 74, 'resting': 66, 'max': 160},
            'steps': {'avg': 9200, 'goal': 10000},
            'sleep': {'avg': 6.8, 'goal': 8, 'quality': 'Fair'},
            'hrv': {'avg': 44, 'baseline': 46},
            'activity': {'activeMinutes': 65, 'calories': 2150}
        },
        'timeline': [
            {'date': 'Mar 27', 'label': 'DBT skills group attended', 'type': 'visit'},
            {'date': 'Mar 30', 'label': 'Emotional regulation improved', 'type': 'alert'},
            {'date': 'Apr 3', 'label': 'Sleep quality variable', 'type': 'alert'},
            {'date': 'Apr 6', 'label': 'Individual therapy session', 'type': 'visit'},
            {'date': 'Apr 9', 'label': 'No self-harm incidents (30 days)', 'type': 'med'}
        ],
        'trendParams': (55, 6.8, 44, 9200, 1, -0.1, -2, 300)
    },
    {
        'id': 8, 'name': 'Robert Kim', 'age': 38, 'gender': 'Male',
        'avatar': 'https://i.pravatar.cc/100?img=25', 'initials': 'RK',
        'disorder': 'Panic Disorder', 'disorderFull': 'Panic Disorder with Agoraphobia',
        'medications': ['Paroxetine 30mg', 'Alprazolam 0.5mg'], 'lastVisit': '4 days ago', 'riskScore': 48,
        'ehr': {
            'diagnosis': 'Panic Disorder with Agoraphobia',
            'diagnosisDate': '2023-02-14',
            'comorbidities': ['Depression'],
            'medications': [
                {'name': 'Paroxetine', 'dose': '30mg', 'frequency': 'Daily', 'startDate': '2023-02-20'},
                {'name': 'Alprazolam', 'dose': '0.5mg', 'frequency': 'As needed', 'startDate': '2023-03-05'},
                {'name': 'Propranolol', 'dose': '20mg', 'frequency': 'As needed', 'startDate': '2023-06-10'}
            ],
            'allergies': ['None known'],
            'bloodPressure': '122/78', 'bmi': 25.6,
            'lastLabWork': '2024-03-30',
            'notes': 'Panic attacks reduced from daily to 1-2 per week. Gradual exposure therapy progressing well.'
        },
        'wearables': {
            'device': 'Polar Vantage V3', 'lastSync': '30 minutes ago',
            'heartRate': {'avg': 73, 'resting': 65, 'max': 148},
            'steps': {'avg': 7800, 'goal': 8000},
            'sleep': {'avg': 7.5, 'goal': 8, 'quality': 'Good'},
            'hrv': {'avg': 50, 'baseline': 48},
            'activity': {'activeMinutes': 50, 'calories': 1900}
        },
        'timeline': [
            {'date': 'Mar 28', 'label': 'Panic attacks: 2 this week (↓)', 'type': 'alert'},
            {'date': 'Apr 1', 'label': 'Exposure therapy session completed', 'type': 'visit'},
            {'date': 'Apr 4', 'label': 'HRV improved (+4%)', 'type': 'alert'},
            {'date': 'Apr 7', 'label': 'PDSS score: 8 (↓3)', 'type': 'survey'},
            {'date': 'Apr 10', 'label': 'Medication compliance: Excellent', 'type': 'med'}
        ],
        'trendParams': (70, 7.5, 50, 7800, -2, 0.2, 2, -100)
    },
    {
        'id': 9, 'name': 'Sophia Anderson', 'age': 31, 'gender': 'Female',
        'avatar': 'https://i.pravatar.cc/100?img=38', 'initials': 'SA',
        'disorder': 'Social Anxiety', 'disorderFull': 'Social Anxiety Disorder',
        'medications': ['Sertraline 100mg', 'Propranolol 40mg'], 'lastVisit': '8 days ago', 'riskScore': 42,
        'ehr': {
            'diagnosis': 'Social Anxiety Disorder, Generalized',
            'diagnosisDate': '2022-09-05',
            'comorbidities': ['Depression'],
            'medications': [
                {'name': 'Sertraline', 'dose': '100mg', 'frequency': 'Daily', 'startDate': '2022-09-12'},
                {'name': 'Propranolol', 'dose': '40mg', 'frequency': 'As needed', 'startDate': '2023-01-20'}
            ],
            'allergies': ['None known'],
            'bloodPressure': '118/72', 'bmi': 23.8,
            'lastLabWork': '2024-03-22',
            'notes': 'Patient making progress in social situations. CBT techniques being applied effectively.'
        },
        'wearables': {
            'device': 'Garmin Forerunner 965', 'lastSync': '1 hour ago',
            'heartRate': {'avg': 69, 'resting': 60, 'max': 142},
            'steps': {'avg': 10200, 'goal': 10000},
            'sleep': {'avg': 7.9, 'goal': 8, 'quality': 'Excellent'},
            'hrv': {'avg': 54, 'baseline': 52},
            'activity': {'activeMinutes': 75, 'calories': 2250}
        },
        'timeline': [
            {'date': 'Mar 26', 'label': 'LSAS score: 42 (↓8)', 'type': 'survey'},
            {'date': 'Mar 29', 'label': 'Social exposure exercise completed', 'type': 'visit'},
            {'date': 'Apr 2', 'label': 'Sleep quality excellent', 'type': 'alert'},
            {'date': 'Apr 5', 'label': 'Activity level increased', 'type': 'alert'},
            {'date': 'Apr 8', 'label': 'Therapy session: Progress noted', 'type': 'visit'}
        ],
        'trendParams': (75, 7.9, 54, 10200, -1, 0.1, 2, 500)
    },
    {
        'id': 10, 'name': 'Christopher Lee', 'age': 24, 'gender': 'Male',
        'avatar': 'https://i.pravatar.cc/100?img=18', 'initials': 'CL',
        'disorder': 'ADHD', 'disorderFull': 'Attention-Deficit/Hyperactivity Disorder',
        'medications': ['Methylphenidate 36mg', 'Atomoxetine 40mg'], 'lastVisit': '1 day ago', 'riskScore': 35,
        'ehr': {
            'diagnosis': 'ADHD, Combined Type',
            'diagnosisDate': '2021-04-12',
            'comorbidities': ['Anxiety'],
            'medications': [
                {'name': 'Methylphenidate', 'dose': '36mg', 'frequency': 'Daily', 'startDate': '2021-04-20'},
                {'name': 'Atomoxetine', 'dose': '40mg', 'frequency': 'Daily', 'startDate': '2023-08-15'},
                {'name': 'Guanfacine', 'dose': '2mg', 'frequency': 'At bedtime', 'startDate': '2023-11-01'}
            ],
            'allergies': ['None known'],
            'bloodPressure': '116/70', 'bmi': 22.4,
            'lastLabWork': '2024-04-08',
            'notes': 'Patient responding well to medication. Focus and attention improved. Continue current regimen.'
        },
        'wearables': {
            'device': 'Apple Watch Ultra 2', 'lastSync': '10 minutes ago',
            'heartRate': {'avg': 71, 'resting': 63, 'max': 152},
            'steps': {'avg': 11500, 'goal': 10000},
            'sleep': {'avg': 7.0, 'goal': 8, 'quality': 'Fair'},
            'hrv': {'avg': 49, 'baseline': 47},
            'activity': {'activeMinutes': 90, 'calories': 2400}
        },
        'timeline': [
            {'date': 'Apr 1', 'label': 'ASRS score: 12 (↓5)', 'type': 'survey'},
            {'date': 'Apr 4', 'label': 'Medication compliance: 100%', 'type': 'med'},
            {'date': 'Apr 7', 'label': 'Activity level high', 'type': 'alert'},
            {'date': 'Apr 9', 'label': 'Sleep duration stable', 'type': 'alert'},
            {'date': 'Apr 11', 'label': 'Follow-up visit: Doing well', 'type': 'visit'}
        ],
        'trendParams': (80, 7.0, 49, 11500, -1, -0.1, 2, 800)
    },
    {
        'id': 11, 'name': 'Isabella Garcia', 'age': 19, 'gender': 'Female',
        'avatar': 'https://i.pravatar.cc/100?img=45', 'initials': 'IG',
        'disorder': 'Anorexia', 'disorderFull': 'Anorexia Nervosa',
        'medications': ['Fluoxetine 60mg', 'Olanzapine 5mg'], 'lastVisit': '9 days ago', 'riskScore': 55,
        'ehr': {
            'diagnosis': 'Anorexia Nervosa, Restricting Type',
            'diagnosisDate': '2023-07-20',
            'comorbidities': ['Depression', 'Anxiety'],
            'medications': [
                {'name': 'Fluoxetine', 'dose': '60mg', 'frequency': 'Daily', 'startDate': '2023-07-25'},
                {'name': 'Olanzapine', 'dose': '5mg', 'frequency': 'Daily', 'startDate': '2023-10-15'},
                {'name': 'Multivitamin', 'dose': '1 tablet', 'frequency': 'Daily', 'startDate': '2023-08-01'}
            ],
            'allergies': ['None known'],
            'bloodPressure': '105/65', 'bmi': 18.2,
            'lastLabWork': '2024-04-01',
            'notes': 'Weight stabilizing. Nutritional counseling ongoing. Monitor for refeeding syndrome.'
        },
        'wearables': {
            'device': 'Fitbit Luxe', 'lastSync': '2 hours ago',
            'heartRate': {'avg': 58, 'resting': 52, 'max': 125},
            'steps': {'avg': 15200, 'goal': 10000},
            'sleep': {'avg': 6.5, 'goal': 8, 'quality': 'Poor'},
            'hrv': {'avg': 32, 'baseline': 35},
            'activity': {'activeMinutes': 150, 'calories': 1200}
        },
        'timeline': [
            {'date': 'Mar 27', 'label': 'Weight: 105 lbs (stable)', 'type': 'med'},
            {'date': 'Mar 30', 'label': 'EDE-Q score: 3.2 (↓0.5)', 'type': 'survey'},
            {'date': 'Apr 2', 'label': 'Activity level very high', 'type': 'alert'},
            {'date': 'Apr 5', 'label': 'Nutritional counseling session', 'type': 'visit'},
            {'date': 'Apr 8', 'label': 'HRV low, monitor closely', 'type': 'alert'}
        ],
        'trendParams': (50, 6.5, 32, 15200, 3, -0.3, -3, 2000)
    },
    {
        'id': 12, 'name': 'Daniel Brown', 'age': 43, 'gender': 'Male',
        'avatar': 'https://i.pravatar.cc/100?img=28', 'initials': 'DB',
        'disorder': 'Substance Use', 'disorderFull': 'Substance Use Disorder (Alcohol)',
        'medications': ['Naltrexone 50mg', 'Acamprosate 666mg'], 'lastVisit': '12 days ago', 'riskScore': 60,
        'ehr': {
            'diagnosis': 'Alcohol Use Disorder, Moderate, In Early Remission',
            'diagnosisDate': '2022-01-10',
            'comorbidities': ['Depression', 'Anxiety'],
            'medications': [
                {'name': 'Naltrexone', 'dose': '50mg', 'frequency': 'Daily', 'startDate': '2022-01-15'},
                {'name': 'Acamprosate', 'dose': '666mg', 'frequency': 'Three times daily', 'startDate': '2022-02-01'},
                {'name': 'Sertraline', 'dose': '100mg', 'frequency': 'Daily', 'startDate': '2022-03-10'}
            ],
            'allergies': ['None known'],
            'bloodPressure': '130/85', 'bmi': 28.5,
            'lastLabWork': '2024-03-18',
            'notes': 'Patient in early remission. 45 days sober. Continue support groups and medication.'
        },
        'wearables': {
            'device': 'Garmin Instinct 2', 'lastSync': '3 hours ago',
            'heartRate': {'avg': 77, 'resting': 69, 'max': 158},
            'steps': {'avg': 9500, 'goal': 8000},
            'sleep': {'avg': 6.2, 'goal': 8, 'quality': 'Poor'},
            'hrv': {'avg': 40, 'baseline': 38},
            'activity': {'activeMinutes': 70, 'calories': 2200}
        },
        'timeline': [
            {'date': 'Mar 25', 'label': '45 days sober (milestone)', 'type': 'med'},
            {'date': 'Mar 28', 'label': 'Support group attendance: Regular', 'type': 'visit'},
            {'date': 'Apr 1', 'label': 'Sleep quality improving', 'type': 'alert'},
            {'date': 'Apr 4', 'label': 'AUDIT score: 6 (↓12)', 'type': 'survey'},
            {'date': 'Apr 7', 'label': 'Medication compliance: Good', 'type': 'med'}
        ],
        'trendParams': (65, 6.2, 40, 9500, -2, 0.4, 2, 600)
    }
]

def migrate_patients():
    """Migrate all patient data to database"""
    app = create_app()
    
    with app.app_context():
        # Drop and recreate tables (for development only!)
        db.drop_all()
        db.create_all()
        
        print("Migrating patient data...")
        
        # Migrate all 12 patients
        for patient_data in PATIENTS_DATA:
            # Create patient
            patient = Patient(
                name=patient_data['name'],
                age=patient_data['age'],
                gender=patient_data['gender'],
                avatar=patient_data['avatar'],
                initials=patient_data['initials'],
                disorder=patient_data['disorder'],
                disorder_full=patient_data['disorderFull'],
                medications=patient_data['medications'],
                last_visit=patient_data['lastVisit'],
                risk_score=patient_data['riskScore']
            )
            db.session.add(patient)
            db.session.flush()  # Get the patient ID
            
            # Create EHR
            ehr_data = patient_data['ehr']
            ehr = EHR(
                patient_id=patient.id,
                diagnosis=ehr_data['diagnosis'],
                diagnosis_date=ehr_data['diagnosisDate'],
                comorbidities=ehr_data['comorbidities'],
                medications=ehr_data['medications'],
                allergies=ehr_data['allergies'],
                blood_pressure=ehr_data['bloodPressure'],
                bmi=ehr_data['bmi'],
                last_lab_work=ehr_data['lastLabWork'],
                notes=ehr_data['notes']
            )
            db.session.add(ehr)
            
            # Create Wearable
            wear_data = patient_data['wearables']
            wearable = Wearable(
                patient_id=patient.id,
                device=wear_data['device'],
                last_sync=wear_data['lastSync'],
                heart_rate_avg=wear_data['heartRate']['avg'],
                heart_rate_resting=wear_data['heartRate']['resting'],
                heart_rate_max=wear_data['heartRate']['max'],
                steps_avg=wear_data['steps']['avg'],
                steps_goal=wear_data['steps']['goal'],
                sleep_avg=wear_data['sleep']['avg'],
                sleep_goal=wear_data['sleep']['goal'],
                sleep_quality=wear_data['sleep']['quality'],
                hrv_avg=wear_data['hrv']['avg'],
                hrv_baseline=wear_data['hrv']['baseline'],
                active_minutes=wear_data['activity']['activeMinutes'],
                calories=wear_data['activity']['calories']
            )
            db.session.add(wearable)
            
            # Create Timeline Events
            for event_data in patient_data['timeline']:
                event = TimelineEvent(
                    patient_id=patient.id,
                    date=event_data['date'],
                    label=event_data['label'],
                    type=event_data['type']
                )
                db.session.add(event)
            
            # Create Trend Data
            trend_params = patient_data['trendParams']
            trend_data_list = generate_trend_data(*trend_params)
            for data in trend_data_list:
                trend = TrendData(
                    patient_id=patient.id,
                    day=data['day'],
                    mood=data['mood'],
                    sleep=data['sleep'],
                    hrv=data['hrv'],
                    activity=data['activity']
                )
                db.session.add(trend)
        
        db.session.commit()
        print(f"Successfully migrated {len(PATIENTS_DATA)} patient(s) to database!")

if __name__ == '__main__':
    migrate_patients()

