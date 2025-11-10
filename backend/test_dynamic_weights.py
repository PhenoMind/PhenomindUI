"""
Test script to demonstrate dynamic biomarker weighting
Shows how different patients get different importance scores based on their data
"""

# Simulate different patient scenarios
scenarios = [
    {
        'name': 'Patient A - Major Sleep Decline',
        'trends': {
            'sleep': {'change': -2.5, 'percentChange': -30},      # Lost 2.5 hours (30% decline)
            'hrv': {'change': -3, 'percentChange': -6},           # Lost 3ms (6% decline)
            'activity': {'change': -800, 'percentChange': -10}   # Lost 800 steps (10% decline)
        }
    },
    {
        'name': 'Patient B - Major HRV Decline',
        'trends': {
            'sleep': {'change': -0.6, 'percentChange': -8},       # Lost 0.6 hours (8% decline)
            'hrv': {'change': -12, 'percentChange': -25},         # Lost 12ms (25% decline) - SEVERE
            'activity': {'change': -600, 'percentChange': -8}    # Lost 600 steps (8% decline)
        }
    },
    {
        'name': 'Patient C - Balanced Decline',
        'trends': {
            'sleep': {'change': -1.2, 'percentChange': -15},      # Lost 1.2 hours (15% decline)
            'hrv': {'change': -6, 'percentChange': -12},          # Lost 6ms (12% decline)
            'activity': {'change': -1800, 'percentChange': -18}  # Lost 1800 steps (18% decline)
        }
    },
    {
        'name': 'Patient D - Major Activity Decline',
        'trends': {
            'sleep': {'change': -0.3, 'percentChange': -4},       # Lost 0.3 hours (4% decline)
            'hrv': {'change': -2, 'percentChange': -4},           # Lost 2ms (4% decline)
            'activity': {'change': -4000, 'percentChange': -40}  # Lost 4000 steps (40% decline) - SEVERE
        }
    }
]

def calculate_dynamic_weights(trends):
    """Calculate dynamic weights (simplified version of the actual function)"""
    
    # Get changes
    sleep_change = abs(trends['sleep']['change'])
    hrv_change = abs(trends['hrv']['change'])
    activity_change = abs(trends['activity']['change'])
    
    # Get percent changes
    sleep_percent = abs(trends['sleep']['percentChange'])
    hrv_percent = abs(trends['hrv']['percentChange'])
    activity_percent = abs(trends['activity']['percentChange'])
    
    # Apply severity multipliers
    sleep_severity = 1.5 if sleep_change > 2.0 else (1.2 if sleep_change > 1.0 else 1.0)
    hrv_severity = 1.4 if hrv_change > 10 else (1.2 if hrv_change > 5 else 1.0)
    activity_severity = 1.3 if activity_change > 3000 else (1.15 if activity_change > 1500 else 1.0)
    
    # Calculate weighted scores
    weighted_sleep = sleep_percent * sleep_severity
    weighted_hrv = hrv_percent * hrv_severity
    weighted_activity = activity_percent * activity_severity
    
    total = weighted_sleep + weighted_hrv + weighted_activity
    
    # Calculate importance (capped at 0.85)
    sleep_importance = min((weighted_sleep / total), 0.85) if total > 0 else 0
    hrv_importance = min((weighted_hrv / total), 0.85) if total > 0 else 0
    activity_importance = min((weighted_activity / total), 0.85) if total > 0 else 0
    
    return {
        'sleep': sleep_importance,
        'hrv': hrv_importance,
        'activity': activity_importance,
        'sleep_severity': sleep_severity,
        'hrv_severity': hrv_severity,
        'activity_severity': activity_severity
    }

# Print results
print("=" * 80)
print("DYNAMIC BIOMARKER WEIGHTING DEMONSTRATION")
print("=" * 80)
print()

for scenario in scenarios:
    print(f"\n{scenario['name']}")
    print("-" * 80)
    
    # Show raw changes
    print("Raw Changes:")
    print(f"  Sleep:    {scenario['trends']['sleep']['change']:+.1f} hours ({scenario['trends']['sleep']['percentChange']:+.0f}%)")
    print(f"  HRV:      {scenario['trends']['hrv']['change']:+.0f} ms ({scenario['trends']['hrv']['percentChange']:+.0f}%)")
    print(f"  Activity: {scenario['trends']['activity']['change']:+.0f} steps ({scenario['trends']['activity']['percentChange']:+.0f}%)")
    print()
    
    # Calculate weights
    weights = calculate_dynamic_weights(scenario['trends'])
    
    # Show severity multipliers
    print("Severity Multipliers Applied:")
    print(f"  Sleep:    {weights['sleep_severity']:.1f}x {'(SEVERE)' if weights['sleep_severity'] > 1.2 else '(Moderate)' if weights['sleep_severity'] > 1.0 else ''}")
    print(f"  HRV:      {weights['hrv_severity']:.1f}x {'(SEVERE)' if weights['hrv_severity'] > 1.2 else '(Moderate)' if weights['hrv_severity'] > 1.0 else ''}")
    print(f"  Activity: {weights['activity_severity']:.1f}x {'(SEVERE)' if weights['activity_severity'] > 1.2 else '(Moderate)' if weights['activity_severity'] > 1.0 else ''}")
    print()
    
    # Show final importance scores
    print("Final Importance Scores (bar chart sizes):")
    
    # Sort by importance to show which is highest
    drivers = [
        ('Sleep', weights['sleep']),
        ('HRV', weights['hrv']),
        ('Activity', weights['activity'])
    ]
    drivers.sort(key=lambda x: x[1], reverse=True)
    
    for i, (name, importance) in enumerate(drivers):
        bar = "█" * int(importance * 50)  # Visual bar
        rank = "🥇" if i == 0 else "🥈" if i == 1 else "🥉"
        print(f"  {rank} {name:8} {importance:5.1%} {bar}")
    
    print()

print("=" * 80)
print("KEY INSIGHTS:")
print("=" * 80)
print("• Each patient's bar chart is PERSONALIZED based on their specific changes")
print("• Larger changes = higher importance scores")
print("• Severe changes get BOOSTED by severity multipliers")
print("• The biggest driver is always shown first (largest bar)")
print()
